import type { FormEvent } from 'react'
import { useEffect, useMemo, useState } from 'react'
import { Show, SignInButton, SignUpButton, UserButton, useAuth, useUser } from '@clerk/react'
import './App.css'

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL ?? 'http://127.0.0.1:8000'
const API_TIMEOUT_MS = 6000

type Role = 'Admin' | 'Fraud Analyst' | 'Manager' | 'Auditor'

type Session = {
  username: string
  role: Role
  token: string
}

type PredictionRow = {
  transaction_id?: string
  prediction?: string
  fraud_probability?: number
  risk_score?: number
  risk_tier?: string
  Latency_ms?: number
  created_at?: string
}

type ChartPoint = {
  label: string
  count: number
}

type ModelMetadata = {
  model_name?: string
  preprocessor?: string
  model_file?: string
  model_path?: string
  feature_count?: number
  features?: string[]
  status?: string
}

type DashboardSummary = {
  kpis?: {
    transactions?: number
    predictions?: number
    fraud_cases?: number
    alerts?: number
    critical_alerts?: number
    average_risk?: number
    features_used?: number
    models_loaded?: number
  }
  risk_tiers?: ChartPoint[]
  prediction_distribution?: ChartPoint[]
  recent_predictions?: PredictionRow[]
  model?: ModelMetadata
  features?: string[]
}

type PredictionResult = {
  transaction_id?: string
  prediction?: {
    Prediction?: string
    Fraud_Probability?: number
    Risk_Score?: number
    Risk_Tier?: string
    Latency_ms?: number
  }
  risk_analysis?: Record<string, unknown>
  model?: ModelMetadata
  features_used?: Record<string, number>
  status?: string
  message?: string
}

type View =
  | 'overview'
  | 'predict'
  | 'alerts'
  | 'cases'
  | 'reports'
  | 'analytics'
  | 'feedback'
  | 'settings'

const navItems: Array<{ id: View; label: string; roles: Role[] }> = [
  { id: 'overview', label: 'Overview', roles: ['Admin', 'Fraud Analyst', 'Manager', 'Auditor'] },
  { id: 'predict', label: 'Predict', roles: ['Admin', 'Fraud Analyst'] },
  { id: 'alerts', label: 'Alerts', roles: ['Admin', 'Fraud Analyst', 'Manager', 'Auditor'] },
  { id: 'cases', label: 'Cases', roles: ['Admin', 'Fraud Analyst', 'Manager'] },
  { id: 'reports', label: 'AI Reports', roles: ['Admin', 'Fraud Analyst', 'Manager'] },
  { id: 'analytics', label: 'Analytics', roles: ['Admin', 'Manager'] },
  { id: 'feedback', label: 'Feedback', roles: ['Admin', 'Fraud Analyst', 'Manager'] },
  { id: 'settings', label: 'Settings', roles: ['Admin'] },
]

const emptyFeatures = Object.fromEntries(
  ['Time', 'Amount', ...Array.from({ length: 28 }, (_, index) => `V${index + 1}`)].map((field) => [
    field,
    field === 'Amount' ? '150' : '0',
  ]),
) as Record<string, string>

async function fetchWithTimeout(input: RequestInfo | URL, init?: RequestInit) {
  const controller = new AbortController()
  const timeoutId = window.setTimeout(() => controller.abort(), API_TIMEOUT_MS)

  try {
    return await fetch(input, { ...init, signal: controller.signal })
  } finally {
    window.clearTimeout(timeoutId)
  }
}

function App() {
  const [health, setHealth] = useState('Checking')

  useEffect(() => {
    fetchWithTimeout(`${API_BASE_URL}/health`)
      .then((response) => (response.ok ? setHealth('Online') : setHealth('Degraded')))
      .catch(() => setHealth('Offline'))
  }, [])

  return (
    <>
      <Show when="signed-out">
        <AuthScreen apiHealth={health} />
      </Show>
      <Show when="signed-in">
        <AuthenticatedDashboard health={health} />
      </Show>
    </>
  )
}

function AuthenticatedDashboard({ health }: { health: string }) {
  const { getToken } = useAuth()
  const { user } = useUser()
  const [view, setView] = useState<View>('overview')
  const [predictions, setPredictions] = useState<PredictionRow[]>([])
  const [summary, setSummary] = useState<DashboardSummary | null>(null)
  const [loading, setLoading] = useState(false)
  const [notice, setNotice] = useState('')
  const [apiToken, setApiToken] = useState('')

  const role = useMemo<Role>(() => {
    const metadataRole = user?.publicMetadata?.role
    return isRole(metadataRole) ? metadataRole : 'Admin'
  }, [user?.publicMetadata?.role])

  const session = useMemo<Session>(
    () => ({
      username: user?.fullName ?? user?.primaryEmailAddress?.emailAddress ?? 'Clerk user',
      role,
      token: apiToken,
    }),
    [apiToken, role, user?.fullName, user?.primaryEmailAddress?.emailAddress],
  )

  useEffect(() => {
    getToken()
      .then((token) => setApiToken(token ?? ''))
      .catch(() => setApiToken(''))
  }, [getToken])

  useEffect(() => {
    refreshDashboard()
  }, [])

  const metrics = useMemo(() => {
    if (summary?.kpis) {
      return {
        transactions: summary.kpis.transactions ?? predictions.length,
        predictions: summary.kpis.predictions ?? predictions.length,
        frauds: summary.kpis.fraud_cases ?? 0,
        alerts: summary.kpis.alerts ?? 0,
        critical: summary.kpis.critical_alerts ?? 0,
        avgRisk: Math.round(summary.kpis.average_risk ?? 0),
        features: summary.kpis.features_used ?? 30,
        models: summary.kpis.models_loaded ?? 0,
      }
    }

    const frauds = predictions.filter((item) => item.prediction === 'Fraud').length
    const riskTotal = predictions.reduce((sum, item) => sum + Number(item.risk_score ?? 0), 0)
    const avgRisk = predictions.length ? Math.round(riskTotal / predictions.length) : 0
    const critical = predictions.filter((item) => Number(item.risk_score ?? 0) >= 80).length
    return {
      transactions: predictions.length,
      predictions: predictions.length,
      frauds,
      alerts: critical,
      critical,
      avgRisk,
      features: 30,
      models: 0,
    }
  }, [predictions, summary])

  async function refreshDashboard() {
    setLoading(true)
    try {
      const response = await fetchWithTimeout(`${API_BASE_URL}/dashboard/summary`)
      if (!response.ok) throw new Error('Unable to load dashboard summary')
      const data = (await response.json()) as DashboardSummary
      setSummary(data)
      setPredictions(data.recent_predictions ?? [])
    } catch {
      await refreshPredictions()
    } finally {
      setLoading(false)
    }
  }

  async function refreshPredictions() {
    setLoading(true)
    try {
      const response = await fetchWithTimeout(`${API_BASE_URL}/predictions`)
      if (!response.ok) throw new Error('Unable to load predictions')
      setPredictions(await response.json())
    } catch {
      setPredictions([])
    } finally {
      setLoading(false)
    }
  }

  const allowedNav = navItems.filter((item) => item.roles.includes(session.role))

  return (
    <div className="app-shell">
      <aside className="sidebar">
        <div>
          <div className="brand-mark">FS</div>
          <h1>FraudShield AI</h1>
          <p>Enterprise Console</p>
        </div>

        <nav aria-label="Main navigation">
          {allowedNav.map((item) => (
            <button
              className={view === item.id ? 'active' : ''}
              key={item.id}
              type="button"
              onClick={() => setView(item.id)}
            >
              {item.label}
            </button>
          ))}
        </nav>

        <div className="sidebar-footer">
          <span>{session.username}</span>
          <strong>{session.role}</strong>
          <UserButton />
        </div>
      </aside>

      <main className="workspace">
        <header className="topbar">
          <div>
            <span className="eyebrow">Fraud operations</span>
            <h2>{navItems.find((item) => item.id === view)?.label ?? 'Overview'}</h2>
          </div>
          <div className={`status ${health.toLowerCase()}`}>API {health}</div>
        </header>

        {notice && (
          <div className="notice">
            <span>{notice}</span>
            <button type="button" onClick={() => setNotice('')}>
              Dismiss
            </button>
          </div>
        )}

        {view === 'overview' && (
          <Overview
            predictions={predictions}
            metrics={metrics}
            summary={summary}
            loading={loading}
            onRefresh={refreshDashboard}
          />
        )}
        {view === 'predict' && (
          <Predict token={session.token} onResult={(message) => {
            setNotice(message)
            refreshDashboard()
          }} />
        )}
        {view === 'alerts' && <Alerts predictions={predictions} />}
        {view === 'cases' && <Cases predictions={predictions} />}
        {view === 'reports' && <Reports predictions={predictions} />}
        {view === 'analytics' && <Analytics predictions={predictions} summary={summary} />}
        {view === 'feedback' && <Feedback />}
        {view === 'settings' && <Settings apiHealth={health} summary={summary} />}
      </main>
    </div>
  )
}

function AuthScreen({ apiHealth }: { apiHealth: string }) {
  return (
    <main className="login-page">
      <section className="login-hero">
        <span className="eyebrow">Enterprise fraud operations</span>
        <h1>FraudShield AI Enterprise</h1>
        <p>
          A React console for transaction scoring, alert triage, case work, AI reports, and model monitoring.
        </p>
        <div className="hero-grid">
          <div>
            <strong>Real-time</strong>
            <span>Risk scoring</span>
          </div>
          <div>
            <strong>Role based</strong>
            <span>Access control</span>
          </div>
          <div>
            <strong>AI assisted</strong>
            <span>Investigation summaries</span>
          </div>
        </div>
      </section>

      <section className="login-panel auth-panel">
        <div className="brand-mark">FS</div>
        <h2>Sign in</h2>
        <p>Use your organization account to access FraudShield AI Enterprise.</p>
        <div className="auth-actions">
          <SignInButton mode="modal">
            <button type="button">Sign in</button>
          </SignInButton>
          <SignUpButton mode="modal">
            <button type="button" className="secondary-button">Sign up</button>
          </SignUpButton>
        </div>
        <small>API status: {apiHealth}</small>
      </section>
    </main>
  )
}

function isRole(value: unknown): value is Role {
  return value === 'Admin' || value === 'Fraud Analyst' || value === 'Manager' || value === 'Auditor'
}

function Overview({
  predictions,
  metrics,
  summary,
  loading,
  onRefresh,
}: {
  predictions: PredictionRow[]
  metrics: {
    transactions: number
    predictions: number
    frauds: number
    alerts: number
    critical: number
    avgRisk: number
    features: number
    models: number
  }
  summary: DashboardSummary | null
  loading: boolean
  onRefresh: () => void
}) {
  return (
    <>
      <section className="summary-grid">
        <Metric label="Transactions" value={metrics.transactions} />
        <Metric label="Predictions" value={metrics.predictions} />
        <Metric label="Fraud cases" value={metrics.frauds} />
        <Metric label="Alerts" value={metrics.alerts} />
        <Metric label="Critical alerts" value={metrics.critical} />
        <Metric label="Average risk" value={metrics.avgRisk} />
        <Metric label="Features used" value={metrics.features} />
        <Metric label="Models loaded" value={metrics.models} />
      </section>

      <section className="dashboard-grid">
        <ChartPanel title="Prediction distribution" data={summary?.prediction_distribution ?? distributionFromPredictions(predictions)} />
        <ChartPanel title="Risk tiers" data={summary?.risk_tiers ?? tierDistributionFromPredictions(predictions)} tone="risk" />
        <ModelPanel model={summary?.model} features={summary?.features ?? []} />
      </section>

      <section className="panel">
        <div className="panel-heading">
          <div>
            <h3>Recent predictions</h3>
            <p>Latest transaction scoring results and generated model values.</p>
          </div>
          <button type="button" onClick={onRefresh}>
            {loading ? 'Refreshing...' : 'Refresh'}
          </button>
        </div>
        <PredictionTable predictions={predictions.slice(0, 8)} />
      </section>
    </>
  )
}

function distributionFromPredictions(predictions: PredictionRow[]) {
  return ['Fraud', 'Genuine', 'Unknown']
    .map((label) => ({
      label,
      count: predictions.filter((item) => (item.prediction ?? 'Unknown') === label).length,
    }))
    .filter((item) => item.count > 0)
}

function tierDistributionFromPredictions(predictions: PredictionRow[]) {
  return ['Very Low', 'Low', 'Medium', 'High', 'Critical']
    .map((label) => ({
      label,
      count: predictions.filter((item) => (item.risk_tier ?? 'Unknown') === label).length,
    }))
    .filter((item) => item.count > 0)
}

function ChartPanel({ title, data, tone = 'default' }: { title: string; data: ChartPoint[]; tone?: 'default' | 'risk' }) {
  const total = data.reduce((sum, item) => sum + item.count, 0)

  return (
    <section className="panel chart-panel">
      <h3>{title}</h3>
      <p>{total ? `${total} records analyzed` : 'Waiting for transaction data.'}</p>
      <div className="chart-bars">
        {data.length ? (
          data.map((item) => {
            const width = total ? Math.max(6, (item.count / total) * 100) : 0
            return (
              <div className="chart-row" key={item.label}>
                <span>{item.label}</span>
                <div className="chart-track">
                  <i className={tone === 'risk' ? `risk-${item.label.toLowerCase().replace(' ', '-')}` : ''} style={{ width: `${width}%` }} />
                </div>
                <strong>{item.count}</strong>
              </div>
            )
          })
        ) : (
          <EmptyState text="No graph data available." />
        )}
      </div>
    </section>
  )
}

function ModelPanel({ model, features }: { model?: ModelMetadata; features: string[] }) {
  const visibleFeatures = features.slice(0, 12)

  return (
    <section className="panel model-panel">
      <h3>Model and features</h3>
      <p>Detected model configuration used for scoring.</p>
      <div className="model-facts">
        <Metric label="Model" value={model?.model_name ?? 'Unavailable'} />
        <Metric label="Preprocessor" value={model?.preprocessor ?? 'Unavailable'} />
        <Metric label="Feature count" value={model?.feature_count ?? (features.length || 30)} />
      </div>
      <div className="feature-chip-list">
        {(visibleFeatures.length ? visibleFeatures : Object.keys(emptyFeatures).slice(0, 12)).map((feature) => (
          <span key={feature}>{feature}</span>
        ))}
      </div>
      <small>{model?.model_file ? `Artifact: ${model.model_file}` : 'Artifact metadata loads from FastAPI.'}</small>
    </section>
  )
}

function Predict({ token, onResult }: { token: string; onResult: (message: string) => void }) {
  const [features, setFeatures] = useState(emptyFeatures)
  const [busy, setBusy] = useState(false)
  const [result, setResult] = useState<PredictionResult | null>(null)

  async function submit(event: FormEvent) {
    event.preventDefault()
    setBusy(true)
    setResult(null)

    const payload = Object.fromEntries(Object.entries(features).map(([key, value]) => [key, Number(value)]))

    try {
      const response = await fetchWithTimeout(`${API_BASE_URL}/predict`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          Authorization: `Bearer ${token}`,
        },
        body: JSON.stringify(payload),
      })
      const data = await response.json()
      setResult(data)
      onResult(response.ok ? 'Prediction generated successfully.' : data.message ?? 'Prediction failed.')
    } catch {
      onResult('Could not reach the prediction API. Start FastAPI on port 8000.')
    } finally {
      setBusy(false)
    }
  }

  return (
    <section className="panel">
      <div className="panel-heading">
        <div>
          <h3>Single transaction prediction</h3>
          <p>Enter PCA features from the credit card fraud dataset.</p>
        </div>
      </div>
      <form className="feature-form" onSubmit={submit}>
        {Object.keys(features).map((field) => (
          <label key={field}>
            {field}
            <input
              inputMode="decimal"
              value={features[field]}
              onChange={(event) => setFeatures((current) => ({ ...current, [field]: event.target.value }))}
            />
          </label>
        ))}
        <button type="submit" disabled={busy}>
          {busy ? 'Scoring...' : 'Run prediction'}
        </button>
      </form>
      {result && (
        <PredictionResultPanel result={result} />
      )}
    </section>
  )
}

function PredictionResultPanel({ result }: { result: PredictionResult }) {
  const prediction = result.prediction
  const featureEntries = Object.entries(result.features_used ?? {}).slice(0, 12)

  return (
    <div className="result-box">
      <div className="panel-heading compact">
        <div>
          <h3>Generated model values</h3>
          <p>Transaction {result.transaction_id ?? 'pending'}</p>
        </div>
        <strong className={`pill ${(prediction?.Prediction ?? '').toLowerCase()}`}>{prediction?.Prediction ?? result.status ?? 'Unknown'}</strong>
      </div>
      <section className="summary-grid result-metrics">
        <Metric label="Fraud probability" value={`${Math.round(Number(prediction?.Fraud_Probability ?? 0) * 100)}%`} />
        <Metric label="Risk score" value={prediction?.Risk_Score ?? 0} />
        <Metric label="Risk tier" value={prediction?.Risk_Tier ?? 'Unavailable'} />
        <Metric label="Latency" value={`${prediction?.Latency_ms ?? 0} ms`} />
      </section>
      <div className="model-strip">
        <span>Model</span>
        <strong>{result.model?.model_name ?? 'Unavailable'}</strong>
        <span>Features used</span>
        <strong>{Object.keys(result.features_used ?? {}).length}</strong>
      </div>
      {featureEntries.length > 0 && (
        <div className="feature-value-grid">
          {featureEntries.map(([feature, value]) => (
            <div key={feature}>
              <span>{feature}</span>
              <strong>{value}</strong>
            </div>
          ))}
        </div>
      )}
    </div>
  )
}

function Alerts({ predictions }: { predictions: PredictionRow[] }) {
  const alerts = predictions.filter((item) => Number(item.risk_score ?? 0) >= 70)
  return (
    <section className="panel">
      <h3>Alert queue</h3>
      <p>Transactions with elevated risk scores are surfaced here for triage.</p>
      <PredictionTable predictions={alerts} emptyText="No active alerts found." />
    </section>
  )
}

function Cases({ predictions }: { predictions: PredictionRow[] }) {
  const cases = predictions.filter((item) => item.prediction === 'Fraud' || Number(item.risk_score ?? 0) >= 80)
  return (
    <section className="panel">
      <h3>Case management</h3>
      <p>High risk fraud outcomes are prepared as investigation cases.</p>
      <PredictionTable predictions={cases} emptyText="No cases are waiting for review." />
    </section>
  )
}

function Reports({ predictions }: { predictions: PredictionRow[] }) {
  const [selected, setSelected] = useState('')
  const item = predictions.find((prediction) => prediction.transaction_id === selected) ?? predictions[0]
  return (
    <section className="panel">
      <h3>AI investigation report</h3>
      <p>Generate a concise investigation draft from the selected prediction.</p>
      <select value={item?.transaction_id ?? ''} onChange={(event) => setSelected(event.target.value)}>
        {predictions.map((prediction) => (
          <option key={prediction.transaction_id} value={prediction.transaction_id}>
            {prediction.transaction_id}
          </option>
        ))}
      </select>
      {item ? (
        <div className="report">
          <h4>Transaction {item.transaction_id}</h4>
          <p>
            The transaction is classified as {item.prediction ?? 'Unknown'} with a risk score of{' '}
            {item.risk_score ?? 0}. The fraud probability is{' '}
            {Math.round(Number(item.fraud_probability ?? 0) * 100)} percent and the risk tier is{' '}
            {item.risk_tier ?? 'Unavailable'}.
          </p>
          <p>
            Recommended action: {Number(item.risk_score ?? 0) >= 80 ? 'hold and escalate' : 'review using standard controls'}.
          </p>
        </div>
      ) : (
        <EmptyState text="No predictions available for report generation." />
      )}
    </section>
  )
}

function Analytics({ predictions, summary }: { predictions: PredictionRow[]; summary: DashboardSummary | null }) {
  const tiers = summary?.risk_tiers?.length ? summary.risk_tiers : tierDistributionFromPredictions(predictions)
  const distribution = summary?.prediction_distribution?.length
    ? summary.prediction_distribution
    : distributionFromPredictions(predictions)

  return (
    <div className="dashboard-grid two">
      <ChartPanel title="Prediction mix" data={distribution} />
      <ChartPanel title="Risk distribution" data={tiers} tone="risk" />
      <ModelPanel model={summary?.model} features={summary?.features ?? []} />
    </div>
  )
}

function Feedback() {
  const [form, setForm] = useState({
    transaction_id: '',
    analyst: '',
    prediction: 'Fraud',
    actual_label: 'Fraud',
    comments: '',
  })
  const [status, setStatus] = useState('')

  async function submit(event: FormEvent) {
    event.preventDefault()
    try {
      const response = await fetchWithTimeout(`${API_BASE_URL}/feedback`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(form),
      })
      setStatus(response.ok ? 'Feedback saved.' : 'Feedback could not be saved.')
    } catch {
      setStatus('Could not reach feedback API.')
    }
  }

  return (
    <section className="panel">
      <h3>Analyst feedback</h3>
      <form className="feedback-form" onSubmit={submit}>
        {Object.entries(form).map(([field, value]) => (
          <label key={field}>
            {field.replace('_', ' ')}
            <input value={value} onChange={(event) => setForm((current) => ({ ...current, [field]: event.target.value }))} />
          </label>
        ))}
        <button type="submit">Submit feedback</button>
      </form>
      {status && <div className="notice inline">{status}</div>}
    </section>
  )
}

function Settings({ apiHealth, summary }: { apiHealth: string; summary: DashboardSummary | null }) {
  return (
    <>
      <section className="panel settings-grid">
        <div>
          <h3>Frontend settings</h3>
          <p>React app is connected to:</p>
          <code>{API_BASE_URL}</code>
        </div>
        <Metric label="API health" value={apiHealth} />
        <Metric label="Frontend" value="React + Vite" />
      </section>
      <ModelPanel model={summary?.model} features={summary?.features ?? []} />
    </>
  )
}

function Metric({ label, value }: { label: string; value: string | number }) {
  return (
    <div className="metric-card">
      <span>{label}</span>
      <strong>{value}</strong>
    </div>
  )
}

function PredictionTable({
  predictions,
  emptyText = 'No prediction data available.',
}: {
  predictions: PredictionRow[]
  emptyText?: string
}) {
  if (!predictions.length) return <EmptyState text={emptyText} />

  return (
    <div className="table-wrap">
      <table>
        <thead>
          <tr>
            <th>Transaction</th>
            <th>Prediction</th>
            <th>Fraud probability</th>
            <th>Risk score</th>
            <th>Risk tier</th>
            <th>Latency</th>
          </tr>
        </thead>
        <tbody>
          {predictions.map((item, index) => (
            <tr key={item.transaction_id ?? index}>
              <td>{item.transaction_id ?? 'Pending'}</td>
              <td>{item.prediction ?? 'Unknown'}</td>
              <td>{Math.round(Number(item.fraud_probability ?? 0) * 100)}%</td>
              <td>{item.risk_score ?? 0}</td>
              <td>{item.risk_tier ?? 'Unavailable'}</td>
              <td>{item.Latency_ms ? `${item.Latency_ms} ms` : 'n/a'}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  )
}

function EmptyState({ text }: { text: string }) {
  return <div className="empty-state">{text}</div>
}

export default App
