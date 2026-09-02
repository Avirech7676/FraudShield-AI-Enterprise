import type { ChangeEvent, FormEvent } from 'react'
import { useEffect, useMemo, useState } from 'react'
import { Show, SignInButton, SignUpButton, UserButton, useAuth, useUser } from '@clerk/react'
import {
  Shield,
  ShieldCheck,
  ShieldWarning,
  Pulse,
  TrendUp,
  Brain,
  Lightning,
  FileText,
  Sliders,
  Bell,
  Briefcase,
  ChartLineUp,
  ChatText,
  Gear,
  ArrowRight,
  ArrowsClockwise,
  UploadSimple,
  WarningCircle,
  Clock,
  Cpu,
  TerminalWindow,
  LockKey
} from '@phosphor-icons/react'
import { motion, AnimatePresence } from 'motion/react'
import './App.css'

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL ?? 'http://127.0.0.1:8000'
const API_TIMEOUT_MS = 20000
const DATASET_PREVIEW_BYTES = 2 * 1024 * 1024
const DATASET_ROW_LIMIT = 25

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
  fraud_probability?: number
  risk_score?: number
  tier?: string
  top_factors?: string[]
  llm_explanation?: string
  status?: string
  message?: string
}

type BatchPredictionResult = {
  status?: string
  total_records?: number
  submitted_records?: number
  skipped_records?: number
  results?: PredictionResult[]
  errors?: Array<{
    row: number
    message: string
  }>
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

const navItems: Array<{ id: View; label: string; icon: React.ElementType; roles: Role[] }> = [
  { id: 'overview', label: 'Overview', icon: Pulse, roles: ['Admin', 'Fraud Analyst', 'Manager', 'Auditor'] },
  { id: 'predict', label: 'Predict', icon: Lightning, roles: ['Admin', 'Fraud Analyst'] },
  { id: 'alerts', label: 'Alerts', icon: Bell, roles: ['Admin', 'Fraud Analyst', 'Manager', 'Auditor'] },
  { id: 'cases', label: 'Cases', icon: Briefcase, roles: ['Admin', 'Fraud Analyst', 'Manager'] },
  { id: 'reports', label: 'AI Reports', icon: FileText, roles: ['Admin', 'Fraud Analyst', 'Manager'] },
  { id: 'analytics', label: 'Analytics', icon: ChartLineUp, roles: ['Admin', 'Manager'] },
  { id: 'feedback', label: 'Feedback', icon: ChatText, roles: ['Admin', 'Fraud Analyst', 'Manager'] },
  { id: 'settings', label: 'Settings', icon: Gear, roles: ['Admin'] },
]

const emptyFeatures = Object.fromEntries(
  ['Time', 'Amount', ...Array.from({ length: 28 }, (_, index) => `V${index + 1}`)].map((field) => [
    field,
    field === 'Amount' ? '150' : '0',
  ]),
) as Record<string, string>

const transactionDefaults = {
  Amount: '150',
  Currency: 'USD',
  Merchant: 'Amazon',
  Merchant_Category: 'Retail',
  Payment_Type: 'Credit',
  Country: 'US',
  Card_Present: 'false',
  International: 'false',
  Device_Trust_Score: '80',
  IP_Reputation: '20',
  VPN_Detection: 'false',
  TOR_Detection: 'false',
  Transactions_Last_Hour: '0',
  Transactions_Last_Day: '1',
  Velocity: '150',
  Location_Jump: 'false',
  Device_Change: 'false',
  Login_Failure_Count: '0',
  Merchant_Risk: '20',
  Previous_Fraud: '0',
} as Record<string, string>

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
        <div className="brand-header">
          <div className="brand-mark">
            <Shield weight="fill" size={22} />
          </div>
          <div className="brand-titles">
            <h1>FraudShield</h1>
            <p>AI Enterprise</p>
          </div>
        </div>

        <nav aria-label="Main navigation">
          {allowedNav.map((item) => {
            const Icon = item.icon
            const isActive = view === item.id
            return (
              <button
                className={isActive ? 'active' : ''}
                key={item.id}
                type="button"
                onClick={() => setView(item.id)}
              >
                <Icon weight={isActive ? 'fill' : 'regular'} size={18} />
                <span>{item.label}</span>
              </button>
            )
          })}
        </nav>

        <div className="sidebar-footer">
          <div className="user-info">
            <UserButton />
            <div className="user-details">
              <span className="user-name">{session.username}</span>
              <span className="user-role-badge">{session.role}</span>
            </div>
          </div>
        </div>
      </aside>

      <main className="workspace">
        <header className="topbar">
          <div>
            <span className="eyebrow">Enterprise Fraud Console</span>
            <h2>{navItems.find((item) => item.id === view)?.label ?? 'Overview'}</h2>
          </div>
          <div className="topbar-actions">
            <div className={`status ${health.toLowerCase()}`}>
              <span className="status-dot" />
              API {health}
            </div>
          </div>
        </header>

        <AnimatePresence mode="wait">
          {notice && (
            <motion.div
              initial={{ opacity: 0, y: -10 }}
              animate={{ opacity: 1, y: 0 }}
              exit={{ opacity: 0, y: -10 }}
              className="notice"
            >
              <div className="notice-content">
                <WarningCircle size={18} weight="fill" />
                <span>{notice}</span>
              </div>
              <button type="button" onClick={() => setNotice('')}>
                Dismiss
              </button>
            </motion.div>
          )}
        </AnimatePresence>

        <AnimatePresence mode="wait">
          <motion.div
            key={view}
            initial={{ opacity: 0, y: 8 }}
            animate={{ opacity: 1, y: 0 }}
            exit={{ opacity: 0, y: -8 }}
            transition={{ duration: 0.15, ease: 'easeOut' }}
          >
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
              <Predict
                token={session.token}
                onResult={(message) => {
                  setNotice(message)
                  refreshDashboard()
                }}
              />
            )}
            {view === 'alerts' && <Alerts predictions={predictions} />}
            {view === 'cases' && <Cases predictions={predictions} />}
            {view === 'reports' && <Reports predictions={predictions} />}
            {view === 'analytics' && <Analytics predictions={predictions} summary={summary} />}
            {view === 'feedback' && <Feedback />}
            {view === 'settings' && <Settings apiHealth={health} summary={summary} />}
          </motion.div>
        </AnimatePresence>
      </main>
    </div>
  )
}

function AuthScreen({ apiHealth }: { apiHealth: string }) {
  return (
    <main className="login-page">
      <div className="login-bg-grid" />
      <section className="login-hero">
        <div className="hero-badge">
          <Shield weight="fill" size={14} />
          <span>FraudShield Autonomous Risk Engine</span>
        </div>
        <h1>Autonomous Fraud Detection for Enterprise scale</h1>
        <p>
          Sub-millisecond ML risk scoring, real-time transaction streaming, automated case triage, and explainable AI audit trails.
        </p>
        <div className="hero-grid">
          <div className="hero-card">
            <div className="hero-card-icon"><Lightning size={20} weight="fill" /></div>
            <strong>Sub-20ms</strong>
            <span>Inference Latency</span>
          </div>
          <div className="hero-card">
            <div className="hero-card-icon"><LockKey size={20} weight="fill" /></div>
            <strong>Role-Based</strong>
            <span>Enterprise Triage</span>
          </div>
          <div className="hero-card">
            <div className="hero-card-icon"><Brain size={20} weight="fill" /></div>
            <strong>Explainable</strong>
            <span>XAI Risk Factors</span>
          </div>
        </div>
      </section>

      <section className="login-panel auth-panel">
        <div className="auth-card">
          <div className="brand-mark">
            <Shield weight="fill" size={24} />
          </div>
          <h2>Enterprise Console Access</h2>
          <p>Sign in with your organization credentials to manage fraud rules and triage alerts.</p>
          
          <div className="auth-actions">
            <SignInButton mode="modal">
              <button type="button" className="primary-button">
                <span>Sign in with SSO</span>
                <ArrowRight size={16} weight="bold" />
              </button>
            </SignInButton>
            <SignUpButton mode="modal">
              <button type="button" className="secondary-button">
                Request Access / Register
              </button>
            </SignUpButton>
          </div>

          <div className="auth-footer">
            <div className={`status ${apiHealth.toLowerCase()}`}>
              <span className="status-dot" />
              API Service: {apiHealth}
            </div>
          </div>
        </div>
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
        <Metric label="Transactions" value={metrics.transactions} icon={Pulse} />
        <Metric label="Predictions" value={metrics.predictions} icon={Lightning} />
        <Metric label="Fraud Cases" value={metrics.frauds} icon={ShieldWarning} tone="danger" />
        <Metric label="Alerts" value={metrics.alerts} icon={Bell} tone="warning" />
        <Metric label="Critical Risk" value={metrics.critical} icon={WarningCircle} tone="danger" />
        <Metric label="Average Risk Score" value={metrics.avgRisk} icon={TrendUp} />
        <Metric label="Features active" value={metrics.features} icon={Sliders} />
        <Metric label="Models loaded" value={metrics.models} icon={Cpu} />
      </section>

      <section className="dashboard-grid">
        <ChartPanel title="Prediction Distribution" data={summary?.prediction_distribution ?? distributionFromPredictions(predictions)} />
        <ChartPanel title="Risk Tiers Breakdown" data={summary?.risk_tiers ?? tierDistributionFromPredictions(predictions)} tone="risk" />
        <ModelPanel model={summary?.model} features={summary?.features ?? []} />
      </section>

      <section className="panel">
        <div className="panel-heading">
          <div>
            <h3>Recent Transactions & Scoring Logs</h3>
            <p>Real-time stream of model predictions and generated risk telemetry.</p>
          </div>
          <button type="button" className="secondary-button" onClick={onRefresh} disabled={loading}>
            <ArrowsClockwise size={16} className={loading ? 'animate-spin' : ''} />
            <span>{loading ? 'Refreshing...' : 'Refresh Logs'}</span>
          </button>
        </div>
        <PredictionTable predictions={predictions.slice(0, 8)} exportFilename="scoring_logs.csv" />
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
      <p>{total ? `${total} records evaluated` : 'Waiting for telemetry stream.'}</p>
      <div className="chart-bars">
        {data.length ? (
          data.map((item) => {
            const width = total ? Math.max(6, (item.count / total) * 100) : 0
            return (
              <div className="chart-row" key={item.label}>
                <span className="chart-label">{item.label}</span>
                <div className="chart-track">
                  <motion.i
                    initial={{ width: 0 }}
                    animate={{ width: `${width}%` }}
                    transition={{ duration: 0.5, ease: 'easeOut' }}
                    className={tone === 'risk' ? `risk-${item.label.toLowerCase().replace(' ', '-')}` : ''}
                  />
                </div>
                <strong className="chart-value">{item.count}</strong>
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
      <h3>Model & Preprocessor Specs</h3>
      <p>Active machine learning artifacts serving live endpoints.</p>
      <div className="model-facts">
        <Metric label="Model Engine" value={model?.model_name ?? 'XGBoost / CatBoost'} />
        <Metric label="Preprocessor" value={model?.preprocessor ?? 'StandardScaler'} />
        <Metric label="Feature Dimension" value={model?.feature_count ?? (features.length || 30)} />
      </div>
      <div className="feature-chip-title">Scored Input Dimensions:</div>
      <div className="feature-chip-list">
        {(visibleFeatures.length ? visibleFeatures : Object.keys(emptyFeatures).slice(0, 12)).map((feature) => (
          <span key={feature} className="feature-chip">{feature}</span>
        ))}
      </div>
      <small className="model-artifact">{model?.model_file ? `Artifact: ${model.model_file}` : 'Loaded via FastAPI Registry'}</small>
    </section>
  )
}

function Predict({ token, onResult }: { token: string; onResult: (message: string) => void }) {
  const [mode, setMode] = useState<'details' | 'features' | 'dataset'>('details')
  const [features, setFeatures] = useState(emptyFeatures)
  const [transaction, setTransaction] = useState(transactionDefaults)
  const [busy, setBusy] = useState(false)
  const [result, setResult] = useState<PredictionResult | null>(null)
  const [batchResult, setBatchResult] = useState<BatchPredictionResult | null>(null)
  const [datasetName, setDatasetName] = useState('')

  async function submit(event: FormEvent) {
    event.preventDefault()
    setBusy(true)
    setResult(null)
    setBatchResult(null)

    const payload =
      mode === 'features'
        ? Object.fromEntries(Object.entries(features).map(([key, value]) => [key, Number(value)]))
        : normalizeTransactionPayload(transaction)

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
      onResult(response.ok && data.status !== 'error' ? 'Prediction generated successfully.' : data.message ?? 'Prediction failed.')
    } catch {
      onResult('Could not reach the prediction API. Start FastAPI on port 8000.')
    } finally {
      setBusy(false)
    }
  }

  async function uploadDataset(event: ChangeEvent<HTMLInputElement>) {
    const file = event.target.files?.[0]
    if (!file) return

    setBusy(true)
    setResult(null)
    setBatchResult(null)
    setDatasetName(file.name)

    try {
      const text = await file.slice(0, DATASET_PREVIEW_BYTES).text()
      const rows = parseCsv(text).slice(0, DATASET_ROW_LIMIT)
      if (!rows.length) throw new Error('No rows found in CSV.')

      const payload = rows.map((row) => normalizeTransactionPayload(row))
      const response = await fetchWithTimeout(`${API_BASE_URL}/batch_predict`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          Authorization: `Bearer ${token}`,
        },
        body: JSON.stringify(payload),
      })
      const data = (await response.json()) as BatchPredictionResult
      setBatchResult(data)
      const errors = data.errors?.length ?? 0
      onResult(
        response.ok && data.status !== 'error'
          ? `Scored ${data.total_records ?? 0} rows${errors ? ` with ${errors} row errors` : ''}.`
          : data.message ?? 'Dataset scoring failed.',
      )
    } catch (error) {
      onResult(error instanceof Error ? error.message : 'Dataset upload could not be processed.')
    } finally {
      setBusy(false)
      event.target.value = ''
    }
  }

  return (
    <section className="panel">
      <div className="panel-heading">
        <div>
          <h3>Transaction Risk Scoring</h3>
          <p>Run real-time ML inference on raw parameters, PCA vectors, or bulk CSV uploads.</p>
        </div>
      </div>

      <div className="mode-tabs" role="tablist" aria-label="Prediction input mode">
        <button className={mode === 'details' ? 'active' : ''} type="button" onClick={() => setMode('details')}>
          <Briefcase size={16} />
          <span>Business Fields</span>
        </button>
        <button className={mode === 'features' ? 'active' : ''} type="button" onClick={() => setMode('features')}>
          <Sliders size={16} />
          <span>PCA Features (V1-V28)</span>
        </button>
        <button className={mode === 'dataset' ? 'active' : ''} type="button" onClick={() => setMode('dataset')}>
          <UploadSimple size={16} />
          <span>Batch CSV Upload</span>
        </button>
      </div>

      {mode === 'dataset' ? (
        <div className="upload-panel">
          <label className="file-drop-zone">
            <UploadSimple size={32} weight="duotone" />
            <span>Click or drag CSV dataset here</span>
            <input accept=".csv,text/csv" type="file" onChange={uploadDataset} />
          </label>
          <div className="upload-info">
            <strong>Dataset Requirements:</strong>
            <p>
              {datasetName
                ? `${datasetName} - previewing up to ${DATASET_ROW_LIMIT} rows for fast scoring.`
                : 'CSV headers should include Amount, Time, V1-V28, and risk metadata fields.'}
            </p>
          </div>
        </div>
      ) : (
        <form className="feature-form" onSubmit={submit}>
          {mode === 'details'
            ? Object.keys(transaction).map((field) => (
                <label key={field}>
                  <span>{field.replaceAll('_', ' ')}</span>
                  {isBooleanField(field) ? (
                    <select
                      value={transaction[field]}
                      onChange={(event) => setTransaction((current) => ({ ...current, [field]: event.target.value }))}
                    >
                      <option value="false">False / No</option>
                      <option value="true">True / Yes</option>
                    </select>
                  ) : (
                    <input
                      inputMode={isNumericField(field) ? 'decimal' : 'text'}
                      value={transaction[field]}
                      onChange={(event) => setTransaction((current) => ({ ...current, [field]: event.target.value }))}
                    />
                  )}
                </label>
              ))
            : Object.keys(features).map((field) => (
                <label key={field}>
                  <span>{field}</span>
                  <input
                    inputMode="decimal"
                    value={features[field]}
                    onChange={(event) => setFeatures((current) => ({ ...current, [field]: event.target.value }))}
                  />
                </label>
              ))}
          <div className="form-actions">
            <button type="submit" disabled={busy} className="primary-button">
              <Lightning size={16} weight="fill" />
              <span>{busy ? 'Running Inference...' : 'Evaluate Transaction Risk'}</span>
            </button>
          </div>
        </form>
      )}

      {result && <PredictionResultPanel result={result} />}
      {batchResult ? <BatchResultPanel result={batchResult} /> : null}
    </section>
  )
}

function normalizeTransactionPayload(values: Record<string, string>) {
  return Object.fromEntries(
    Object.entries(values).map(([key, value]) => {
      if (isBooleanField(key)) return [key, parseBoolean(value)]
      if (isNumericField(key) || key === 'Time' || /^V\d+$/.test(key)) return [key, Number(value || 0)]
      return [key, value]
    }),
  )
}

function isBooleanField(field: string) {
  return [
    'Card_Present',
    'Chip_Used',
    'Contactless',
    'International',
    'Emulator_Detection',
    'Rooted_Device',
    'Jailbreak_Detection',
    'VPN_Detection',
    'TOR_Detection',
    'Location_Jump',
    'Device_Change',
    'Password_Reset',
  ].includes(field)
}

function isNumericField(field: string) {
  return [
    'Amount',
    'Customer_Age',
    'Customer_Lifetime',
    'Avg_Spend',
    'Monthly_Spend',
    'Credit_Limit',
    'Device_Trust_Score',
    'IP_Reputation',
    'Transactions_Last_Hour',
    'Transactions_Last_Day',
    'Velocity',
    'Time_Since_Last_Transaction',
    'Merchant_Diversity',
    'Login_Failure_Count',
    'Merchant_Risk',
    'Merchant_Chargeback_Rate',
    'Previous_Fraud',
  ].includes(field)
}

function parseBoolean(value: string) {
  return ['true', '1', 'yes', 'y'].includes(String(value).trim().toLowerCase())
}

function parseCsv(text: string) {
  const lines = text.split(/\r?\n/).filter((line) => line.trim())
  if (lines.length < 2) return []

  const headers = splitCsvLine(lines[0]).map((header) => header.trim())
  return lines.slice(1).map((line) => {
    const values = splitCsvLine(line)
    return Object.fromEntries(headers.map((header, index) => [header, values[index] ?? '']))
  })
}

function splitCsvLine(line: string) {
  const values: string[] = []
  let current = ''
  let quoted = false

  for (const character of line) {
    if (character === '"') {
      quoted = !quoted
    } else if (character === ',' && !quoted) {
      values.push(current.trim())
      current = ''
    } else {
      current += character
    }
  }

  values.push(current.trim())
  return values
}

function PredictionResultPanel({ result }: { result: PredictionResult }) {
  const prediction = normalizePredictionResult(result)
  const featureEntries = Object.entries(result.features_used ?? {}).slice(0, 12)

  return (
    <motion.div
      initial={{ opacity: 0, scale: 0.98 }}
      animate={{ opacity: 1, scale: 1 }}
      className="result-box"
    >
      <div className="panel-heading compact">
        <div>
          <h3>Scoring Result & Inference Telemetry</h3>
          <p>Transaction ID: {result.transaction_id ?? 'TX-GENERATE-NEW'}</p>
        </div>
        <div className={`pill-badge ${prediction.Prediction.toLowerCase()}`}>
          {prediction.Prediction === 'Fraud' ? <ShieldWarning size={14} weight="fill" /> : <ShieldCheck size={14} weight="fill" />}
          <span>{prediction.Prediction}</span>
        </div>
      </div>
      <section className="summary-grid result-metrics">
        <Metric label="Fraud Probability" value={`${Math.round(Number(prediction.Fraud_Probability ?? 0) * 100)}%`} icon={TrendUp} />
        <Metric label="Risk Score" value={prediction.Risk_Score ?? 0} icon={Pulse} />
        <Metric label="Risk Tier" value={prediction.Risk_Tier ?? 'Unavailable'} icon={Shield} />
        <Metric label="Latency" value={`${prediction.Latency_ms ?? 0} ms`} icon={Clock} />
      </section>
      
      {result.llm_explanation && (
        <div className="llm-explanation-box">
          <div className="explanation-header">
            <Brain size={18} weight="fill" />
            <strong>AI Agent Explanation & Triage Notes</strong>
          </div>
          <p>{result.llm_explanation}</p>
        </div>
      )}

      <div className="model-strip">
        <span>Model Version</span>
        <strong>{result.model?.model_name ?? 'Default ML Ensemble'}</strong>
        <span>Scored Features</span>
        <strong>{Object.keys(result.features_used ?? {}).length} Dimensions</strong>
      </div>
      {featureEntries.length > 0 && (
        <div className="feature-value-grid">
          {featureEntries.map(([feature, value]) => (
            <div key={feature}>
              <span>{feature}</span>
              <strong>{typeof value === 'number' ? value.toFixed(4) : value}</strong>
            </div>
          ))}
        </div>
      )}
    </motion.div>
  )
}

function normalizePredictionResult(result: PredictionResult) {
  return {
    Prediction: result.prediction?.Prediction ?? result.status ?? 'Unknown',
    Fraud_Probability: result.prediction?.Fraud_Probability ?? result.fraud_probability ?? 0,
    Risk_Score: result.prediction?.Risk_Score ?? result.risk_score ?? 0,
    Risk_Tier: result.prediction?.Risk_Tier ?? result.tier ?? 'Unavailable',
    Latency_ms: result.prediction?.Latency_ms ?? 0,
  }
}

function BatchResultPanel({ result }: { result: BatchPredictionResult }) {
  const rows = result.results ?? []
  const errors = result.errors ?? []

  return (
    <div className="result-box">
      <div className="panel-heading compact">
        <div>
          <h3>Dataset Batch Scoring Results</h3>
          <p>
            {result.total_records ?? rows.length} transactions scored
            {result.skipped_records ? `, ${result.skipped_records} rows skipped by preview limit` : ''}
          </p>
        </div>
      </div>
      {rows.length ? (
        <div className="table-wrap">
          <table>
            <thead>
              <tr>
                <th>Transaction ID</th>
                <th>Prediction</th>
                <th>Fraud Probability</th>
                <th>Risk Score</th>
                <th>Risk Tier</th>
              </tr>
            </thead>
            <tbody>
              {rows.slice(0, 20).map((item, index) => {
                const prediction = normalizePredictionResult(item)
                return (
                  <tr key={item.transaction_id ?? index}>
                    <td><span className="mono-text">{item.transaction_id ?? `ROW-${index + 1}`}</span></td>
                    <td>
                      <span className={`status-pill ${prediction.Prediction.toLowerCase()}`}>
                        {prediction.Prediction}
                      </span>
                    </td>
                    <td>{Math.round(Number(prediction.Fraud_Probability ?? 0) * 100)}%</td>
                    <td><strong>{prediction.Risk_Score}</strong></td>
                    <td><span className="tier-badge">{prediction.Risk_Tier}</span></td>
                  </tr>
                )
              })}
            </tbody>
          </table>
        </div>
      ) : (
        <EmptyState text="No rows were scored. Check the CSV columns and try again." />
      )}
      {errors.length ? (
        <div className="batch-errors">
          {errors.slice(0, 5).map((error) => (
            <div key={error.row}>
              <strong>Row {error.row} Error</strong>
              <span>{error.message}</span>
            </div>
          ))}
        </div>
      ) : null}
    </div>
  )
}

function Alerts({ predictions }: { predictions: PredictionRow[] }) {
  const alerts = predictions.filter((item) => Number(item.risk_score ?? 0) >= 70)
  return (
    <section className="panel">
      <div className="panel-heading">
        <div>
          <h3>High Risk Alert Queue</h3>
          <p>Real-time transactions exceeding critical risk thresholds (Score ≥ 70).</p>
        </div>
      </div>
      <PredictionTable predictions={alerts} emptyText="No active high-risk alerts found." exportFilename="high_risk_alerts.csv" />
    </section>
  )
}

function Cases({ predictions }: { predictions: PredictionRow[] }) {
  const cases = predictions.filter((item) => item.prediction === 'Fraud' || Number(item.risk_score ?? 0) >= 80)
  return (
    <section className="panel">
      <div className="panel-heading">
        <div>
          <h3>Fraud Case Management</h3>
          <p>Escalated fraud events requiring analyst review, evidence collection, and workflow resolution.</p>
        </div>
      </div>
      <PredictionTable predictions={cases} emptyText="No cases are waiting for analyst review." />
    </section>
  )
}

function Reports({ predictions }: { predictions: PredictionRow[] }) {
  const [selected, setSelected] = useState('')
  const item = predictions.find((prediction) => prediction.transaction_id === selected) ?? predictions[0]
  return (
    <section className="panel">
      <div className="panel-heading">
        <div>
          <h3>AI Investigation & Summary Report</h3>
          <p>Generate explainable AI risk assessments and executive briefs for flagged transactions.</p>
        </div>
      </div>
      <div className="report-selector">
        <label>Select Target Transaction:</label>
        <select value={item?.transaction_id ?? ''} onChange={(event) => setSelected(event.target.value)}>
          {predictions.map((prediction) => (
            <option key={prediction.transaction_id} value={prediction.transaction_id}>
              {prediction.transaction_id} (Score: {prediction.risk_score})
            </option>
          ))}
        </select>
      </div>
      {item ? (
        <div className="report-card">
          <div className="report-header">
            <Brain size={24} weight="fill" className="text-accent" />
            <div>
              <h4>Investigation Brief: {item.transaction_id}</h4>
              <p>Generated by FraudShield AI Explanation Agent</p>
            </div>
          </div>
          <div className="report-body">
            <p>
              Transaction <strong>{item.transaction_id}</strong> was processed and classified as{' '}
              <span className={`status-pill ${item.prediction?.toLowerCase()}`}>{item.prediction ?? 'Unknown'}</span>{' '}
              with an overall Risk Score of <strong>{item.risk_score ?? 0} / 100</strong>.
            </p>
            <p>
              The calculated fraud probability is{' '}
              <strong>{Math.round(Number(item.fraud_probability ?? 0) * 100)}%</strong>, categorizing this event into the{' '}
              <span className="tier-badge">{item.risk_tier ?? 'Unavailable'}</span> risk tier.
            </p>
            <div className="recommendation-box">
              <strong>Recommended Operational Action:</strong>
              <p>
                {Number(item.risk_score ?? 0) >= 80
                  ? 'CRITICAL RISK: Immediately freeze transaction, block merchant token, and escalate to Senior Fraud Analyst.'
                  : 'MODERATE RISK: Apply step-up 2FA authentication or hold for manual customer verification.'}
              </p>
            </div>
          </div>
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
      <ChartPanel title="Prediction Classification Mix" data={distribution} />
      <ChartPanel title="Risk Level Distribution" data={tiers} tone="risk" />
      <ModelPanel model={summary?.model} features={summary?.features ?? []} />
    </div>
  )
}

function Feedback() {
  const [form, setForm] = useState({
    transaction_id: 'TX-94812',
    analyst: 'A. Vance',
    prediction: 'Fraud',
    actual_label: 'Fraud',
    comments: 'Confirmed card testing pattern with high velocity on international IP.',
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
      setStatus(response.ok ? 'Feedback submitted to retraining loop.' : 'Feedback submission failed.')
    } catch {
      setStatus('Could not reach feedback API.')
    }
  }

  return (
    <section className="panel">
      <div className="panel-heading">
        <div>
          <h3>Analyst Ground Truth Feedback</h3>
          <p>Submit verified ground-truth labels to continuously train and calibrate ML model weights.</p>
        </div>
      </div>
      <form className="feedback-form" onSubmit={submit}>
        {Object.entries(form).map(([field, value]) => (
          <label key={field}>
            <span>{field.replace('_', ' ')}</span>
            <input value={value} onChange={(event) => setForm((current) => ({ ...current, [field]: event.target.value }))} />
          </label>
        ))}
        <div className="form-actions">
          <button type="submit" className="primary-button">Submit Ground Truth Label</button>
        </div>
      </form>
      {status && <div className="notice inline">{status}</div>}
    </section>
  )
}

function Settings({ apiHealth, summary }: { apiHealth: string; summary: DashboardSummary | null }) {
  return (
    <>
      <section className="panel settings-grid">
        <div className="settings-item">
          <h3>FastAPI Backend Gateway</h3>
          <p>Target Environment Endpoint URL:</p>
          <code className="mono-code">{API_BASE_URL}</code>
        </div>
        <Metric label="API Health" value={apiHealth} icon={Pulse} />
        <Metric label="Console Tech" value="React 19 + Vite" icon={TerminalWindow} />
      </section>
      <ModelPanel model={summary?.model} features={summary?.features ?? []} />
    </>
  )
}

function Metric({
  label,
  value,
  icon: Icon,
  tone = 'default'
}: {
  label: string
  value: string | number
  icon?: React.ElementType
  tone?: 'default' | 'danger' | 'warning'
}) {
  return (
    <div className={`metric-card ${tone !== 'default' ? `tone-${tone}` : ''}`}>
      <div className="metric-header">
        <span>{label}</span>
        {Icon && <Icon size={18} className="metric-icon" />}
      </div>
      <strong>{value}</strong>
    </div>
  )
}

function downloadCsv(data: PredictionRow[], filename: string) {
  if (!data.length) return
  const headers = ['transaction_id', 'prediction', 'fraud_probability', 'risk_score', 'risk_tier', 'created_at']
  const csvRows = [
    headers.join(','),
    ...data.map((row) =>
      headers
        .map((field) => {
          const val = row[field as keyof PredictionRow] ?? ''
          return `"${String(val).replaceAll('"', '""')}"`
        })
        .join(','),
    ),
  ]
  const blob = new Blob([csvRows.join('\n')], { type: 'text/csv;charset=utf-8;' })
  const url = URL.createObjectURL(blob)
  const link = document.createElement('a')
  link.href = url
  link.setAttribute('download', filename)
  document.body.appendChild(link)
  link.click()
  document.body.removeChild(link)
}

function PredictionTable({
  predictions,
  emptyText = 'No prediction data available.',
  exportFilename,
}: {
  predictions: PredictionRow[]
  emptyText?: string
  exportFilename?: string
}) {
  if (!predictions.length) return <EmptyState text={emptyText} />

  return (
    <div>
      {exportFilename && (
        <div style={{ display: 'flex', justifyContent: 'flex-end', marginBottom: '12px' }}>
          <button
            type="button"
            className="secondary-button"
            style={{ width: 'auto', padding: '6px 12px', fontSize: '11px' }}
            onClick={() => downloadCsv(predictions, exportFilename)}
          >
            <UploadSimple size={14} style={{ transform: 'rotate(180deg)' }} />
            <span>Export CSV</span>
          </button>
        </div>
      )}
      <div className="table-wrap">
        <table>
          <thead>
            <tr>
              <th>Transaction ID</th>
              <th>Prediction</th>
              <th>Fraud Probability</th>
              <th>Risk Score</th>
              <th>Risk Tier</th>
              <th>Latency</th>
            </tr>
          </thead>
          <tbody>
            {predictions.map((item, index) => (
              <tr key={item.transaction_id ?? index}>
                <td><span className="mono-text">{item.transaction_id ?? 'Pending'}</span></td>
                <td>
                  <span className={`status-pill ${(item.prediction ?? 'Unknown').toLowerCase()}`}>
                    {item.prediction ?? 'Unknown'}
                  </span>
                </td>
                <td>{Math.round(Number(item.fraud_probability ?? 0) * 100)}%</td>
                <td><strong>{item.risk_score ?? 0}</strong></td>
                <td><span className="tier-badge">{item.risk_tier ?? 'Unavailable'}</span></td>
                <td><span className="latency-text">{item.Latency_ms ? `${item.Latency_ms} ms` : 'n/a'}</span></td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  )
}

function EmptyState({ text }: { text: string }) {
  return (
    <div className="empty-state">
      <ShieldWarning size={28} weight="duotone" />
      <span>{text}</span>
    </div>
  )
}

export default App
