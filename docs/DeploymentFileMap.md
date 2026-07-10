# FraudShield Deployment File Map

This guide explains exactly which code goes to which deployment platform.

Recommended beginner setup:

```text
Backend API  -> Render
Frontend UI  -> Vercel
Database     -> MongoDB Atlas
```

## 1. What Goes To Render Backend

Render runs your FastAPI backend.

Send these files/folders to Render:

```text
app/
models/
requirements.txt
Dockerfile
render.yaml
.env.example
README.md
```

Important backend entry file:

```text
app/api/main.py
```

Render start command:

```bash
uvicorn app.api.main:app --host 0.0.0.0 --port 10000
```

Backend code used by Render:

```text
app/api/                  API routes, FastAPI app, login routes
app/ml/                   model training/prediction support
app/inference/            production prediction engine
app/features/             feature engineering before prediction
app/database/             MongoDB connection and repository
app/auth/                 JWT and password handling
app/security/             rate limiting, API key helpers, validation
app/rules/                fraud risk rules
app/monitoring/           health and Prometheus metrics
app/notifications/        email, Slack, Teams, Telegram, SMS alerts
app/case_management/      fraud case handling
app/continuous_learning/  analyst feedback endpoints
app/ai/                   Groq fraud explanation/reporting
app/xai/                  SHAP explanation logic
app/exports/              PDF, Excel, CSV, Word export helpers
app/config/               settings, paths, constants, logging config
app/logging/              app logger
app/utils/                utility loaders
```

Backend model files required:

```text
models/production_model.joblib
models/preprocessor.joblib
```

Optional fallback model:

```text
models/best_model.joblib
```

If these model files are missing, your backend can fail during startup or prediction.

## 2. What Goes To Vercel Frontend

Vercel runs your React dashboard.

Vercel should use only this folder:

```text
frontend/
```

Important frontend files:

```text
frontend/src/App.tsx
frontend/src/main.tsx
frontend/src/index.css
frontend/src/App.css
frontend/public/
frontend/package.json
frontend/package-lock.json
frontend/index.html
frontend/vite.config.ts
frontend/tsconfig.json
frontend/tsconfig.app.json
frontend/tsconfig.node.json
```

Vercel settings:

```text
Root Directory: frontend
Build Command: npm run build
Output Directory: dist
```

Frontend build output:

```text
frontend/dist/
```

You do not manually create `dist/`. Vercel creates it after running the build.

## 3. What Goes To MongoDB Atlas

MongoDB Atlas does not receive your code files.

MongoDB stores runtime data:

```text
users
transactions
predictions
alerts
audit_logs
cases
analyst_feedback
feedback
models
notifications
```

Your backend connects to MongoDB using:

```text
app/database/connection.py
app/database/repository.py
```

MongoDB Atlas environment variables:

```env
MONGODB_URI=mongodb+srv://USERNAME:PASSWORD@cluster.mongodb.net/FraudShieldDB
DATABASE_NAME=FraudShieldDB
```

## 4. Files You Usually Do Not Deploy

Do not send these to production unless you have a specific reason:

```text
.venv/
.pytest_cache/
__pycache__/
catboost_info/
logs/
reports/
notebooks/
tests/
data/
clerk-react/
dashboard/
```

Why:

| File / Folder | Reason |
| --- | --- |
| `.venv/` | Local Python environment only. Server creates its own. |
| `.pytest_cache/` | Test cache only. |
| `__pycache__/` | Generated Python cache. |
| `catboost_info/` | Training artifact, not required for app hosting. |
| `logs/` | Runtime logs; server should create fresh logs. |
| `reports/` | Generated reports/training outputs. |
| `notebooks/` | Research/dev only. |
| `tests/` | Useful before deploy, not required to run app. |
| `data/` | Large training data, not needed for normal prediction hosting. |
| `clerk-react/` | Duplicate/demo frontend. Use `frontend/` instead. |
| `dashboard/` | Separate Streamlit dashboard, not part of main React deployment. |

## 5. Full Platform Mapping

| Code / Folder | Deploy To | Required? |
| --- | --- | --- |
| `app/` | Render | Yes |
| `app/api/main.py` | Render | Yes |
| `app/api/routes.py` | Render | Yes |
| `app/api/auth_routes.py` | Render | Yes if using login |
| `app/database/` | Render | Yes |
| `app/inference/` | Render | Yes |
| `app/features/` | Render | Yes |
| `app/rules/` | Render | Yes |
| `app/monitoring/` | Render | Yes for health/metrics |
| `app/notifications/` | Render | Optional but safe to include |
| `app/case_management/` | Render | Optional but used by high-risk alerts |
| `app/continuous_learning/` | Render | Optional but used by feedback |
| `app/ai/` | Render | Optional; Groq explanation support |
| `app/xai/` | Render | Optional but currently imported by prediction route |
| `models/` | Render | Yes |
| `requirements.txt` | Render | Yes |
| `Dockerfile` | Render or Docker host | Optional |
| `render.yaml` | Render | Optional |
| `frontend/` | Vercel | Yes for UI |
| `frontend/src/` | Vercel | Yes |
| `frontend/package.json` | Vercel | Yes |
| `frontend/public/` | Vercel | Yes |
| `frontend/Dockerfile` | Docker frontend host | Optional |
| `deployment/` | VPS/Docker/Nginx host | Optional |
| `docker-compose.yml` | Local/VPS Docker host | Optional |
| `data/` | Not needed for normal hosting | No |
| `tests/` | CI/testing only | No |
| `logs/` | Do not deploy | No |
| `reports/` | Do not deploy | No |
| `dashboard/` | Streamlit only | No |
| `clerk-react/` | Not main app | No |

## 6. Backend Environment Variables For Render

Add these in Render dashboard:

```env
MONGODB_URI=
DATABASE_NAME=FraudShieldDB

JWT_SECRET_KEY=
JWT_ALGORITHM=HS256
JWT_EXPIRE_MINUTES=60

MODEL_DIRECTORY=models
MODEL_VERSION=2.0
DEFAULT_MODEL_VERSION=2.0

LOG_DIRECTORY=logs
REPORT_DIRECTORY=reports

RATE_LIMIT_PER_MINUTE=60
API_VERSION=v2
GROQ_API_KEY=
```

Optional notification envs:

```env
SMTP_SERVER=
SMTP_PORT=587
EMAIL_ADDRESS=
EMAIL_PASSWORD=
TELEGRAM_BOT_TOKEN=
TELEGRAM_CHAT_ID=
SLACK_WEBHOOK=
TEAMS_WEBHOOK=
SMS_API_KEY=
WEBHOOK_URL=
```

## 7. Frontend Environment Variables For Vercel

Add these in Vercel dashboard:

```env
VITE_API_BASE_URL=https://your-render-backend-url.onrender.com
VITE_CLERK_PUBLISHABLE_KEY=your-clerk-publishable-key
```

Example:

```env
VITE_API_BASE_URL=https://fraudshield-api.onrender.com
VITE_CLERK_PUBLISHABLE_KEY=pk_test_xxxxxxxxx
```

## 8. One Important Code Change Before Hosting

Open:

```text
app/api/main.py
```

Find the CORS section:

```python
allow_origins=[
    "http://localhost:5173",
    "http://127.0.0.1:5173",
    "http://localhost:4173",
    "http://127.0.0.1:4173",
]
```

Add your Vercel frontend URL:

```python
allow_origins=[
    "http://localhost:5173",
    "http://127.0.0.1:5173",
    "http://localhost:4173",
    "http://127.0.0.1:4173",
    "https://your-frontend.vercel.app",
]
```

Without this, the frontend may deploy successfully but fail to call the backend.

## 9. Simplest Deployment Order

Follow this exact order:

```text
1. Push backend + frontend code to GitHub.
2. Create MongoDB Atlas database.
3. Deploy backend on Render.
4. Add Render backend env variables.
5. Make sure models/ files are available to backend.
6. Test Render backend /health.
7. Deploy frontend on Vercel using frontend/ as root.
8. Add Vercel frontend env variables.
9. Copy Vercel URL.
10. Add Vercel URL to backend CORS in app/api/main.py.
11. Redeploy backend.
12. Open frontend and test prediction.
```

## 10. Final Simple View

```text
Render needs:
  app/
  models/
  requirements.txt
  env variables

Vercel needs:
  frontend/
  VITE_API_BASE_URL
  VITE_CLERK_PUBLISHABLE_KEY

MongoDB Atlas needs:
  no code
  only database connection string
```

