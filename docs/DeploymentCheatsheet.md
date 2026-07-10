# FraudShield AI Enterprise Deployment Cheatsheet

This file is the single deployment map for the current codebase.

## 1. Application Pieces

| Piece | Folder / File | Required for Hosting | Notes |
| --- | --- | --- | --- |
| FastAPI backend | `app/` | Yes | Main API, ML inference, auth, MongoDB, reports, monitoring. |
| Backend entrypoint | `app/api/main.py` | Yes | Run with `uvicorn app.api.main:app`. |
| Frontend dashboard | `frontend/` | Yes, if hosting UI | React + Vite app. Calls FastAPI through `VITE_API_BASE_URL`. |
| ML artifacts | `models/production_model.joblib`, `models/best_model.joblib`, `models/preprocessor.joblib` | Yes | API fails at startup if model/preprocessor are missing. |
| Python dependencies | `requirements.txt` | Yes | Backend install file. Should be cleaned before production if possible. |
| Frontend dependencies | `frontend/package.json`, `frontend/package-lock.json` | Yes | Use `npm ci`, then `npm run build`. |
| Docker backend | `Dockerfile` | Optional | Builds backend API image. |
| Docker frontend | `frontend/Dockerfile` | Optional | Builds static frontend served by Nginx. |
| Compose local full stack | `docker-compose.yml` | Optional | API + frontend + MongoDB. |
| Compose production draft | `deployment/docker-compose.yml` | Optional | API + MongoDB + Nginx reverse proxy. |
| Render config | `render.yaml` | Optional | Backend-only Render deployment draft. |
| Runtime logs | `logs/` | No | Generated at runtime. Do not deploy old logs. |
| Reports | `reports/` | No | Generated/training outputs. Deploy only if you need them. |
| Training data | `data/fraud.csv`, `data/raw/creditcard.csv` | No for inference | Needed for retraining, not normal API hosting. Very large. |
| Training scripts | `train.py`, `app/ml/trainer.py` | No for inference | Needed for model training/retraining only. |
| Tests | `tests/`, `app/**/test_*.py` | No | Use before deploy, do not ship as required runtime files. |
| Docs | `docs/` | No | Reference only. |
| Notebooks | `notebooks/` | No | Development/research only. |
| Duplicate/demo frontend | `clerk-react/` | Usually no | Looks like a second Vite/Clerk sample. Prefer `frontend/`. |
| Streamlit dashboard | `dashboard/app.py` | Usually no | Separate dashboard, not wired into main deployment compose. |

## 2. Backend Runtime Requirements

Minimum backend runtime files:

```text
app/
models/
requirements.txt
.env or platform environment variables
Dockerfile, only if containerizing
deployment/, only if using Gunicorn/Nginx deployment files
```

Important backend command:

```bash
uvicorn app.api.main:app --host 0.0.0.0 --port 8000
```

Production Gunicorn command:

```bash
gunicorn app.api.main:app -c deployment/gunicorn.conf.py
```

Health checks:

```bash
GET /health
GET /version
GET /metrics
```

Main API endpoints:

```text
POST /predict
POST /batch_predict
GET  /predictions
GET  /dashboard/summary
GET  /model/metadata
POST /feedback
POST /login
GET/POST/PUT/DELETE /users
```

## 3. Frontend Runtime Requirements

Minimum frontend runtime files:

```text
frontend/src/
frontend/public/
frontend/index.html
frontend/package.json
frontend/package-lock.json
frontend/tsconfig*.json
frontend/vite.config.ts
frontend/Dockerfile, only if containerizing
```

Frontend build:

```bash
cd frontend
npm ci
npm run build
```

Frontend preview:

```bash
npm run preview
```

Frontend hosting output:

```text
frontend/dist/
```

Deploy `frontend/dist/` to static hosting such as Vercel, Netlify, Render Static Site, S3/CloudFront, or Nginx.

## 4. Required Environment Variables

Backend required or strongly recommended:

```env
MONGODB_URI=mongodb+srv://USER:PASSWORD@CLUSTER/dbname
DATABASE_NAME=FraudShieldDB

JWT_SECRET_KEY=use-a-long-random-secret
JWT_ALGORITHM=HS256
JWT_EXPIRE_MINUTES=60

MODEL_DIRECTORY=models
MODEL_VERSION=2.0
DEFAULT_MODEL_VERSION=2.0

LOG_DIRECTORY=logs
REPORT_DIRECTORY=reports

RATE_LIMIT_PER_MINUTE=60
API_VERSION=v2
```

Backend optional integrations:

```env
GROQ_API_KEY=
API_KEY=
ENCRYPTION_KEY=

SMTP_SERVER=
SMTP_PORT=587
EMAIL_ADDRESS=
EMAIL_PASSWORD=
EMAIL_HOST=
EMAIL_USERNAME=

TELEGRAM_BOT_TOKEN=
TELEGRAM_TOKEN=
TELEGRAM_CHAT_ID=
SLACK_WEBHOOK=
TEAMS_WEBHOOK=
SMS_API_KEY=
SMS_SENDER=FraudShield
WEBHOOK_URL=
```

Frontend required:

```env
VITE_API_BASE_URL=https://your-api-domain.com
VITE_CLERK_PUBLISHABLE_KEY=pk_test_or_pk_live_xxx
```

Current frontend behavior:

- If `VITE_API_BASE_URL` is missing, it calls `http://127.0.0.1:8000`.
- If `VITE_CLERK_PUBLISHABLE_KEY` is missing or does not start with `pk_`, the UI shows "Clerk key required".

## 5. Production Fixes Needed Before Public Hosting

1. Update CORS in `app/api/main.py`.

Current allowed origins are local only:

```python
http://localhost:5173
http://127.0.0.1:5173
http://localhost:4173
http://127.0.0.1:4173
```

Add your real frontend URL, for example:

```python
https://fraudshield.yourdomain.com
```

2. Use a hosted MongoDB connection.

For cloud hosting, do not use:

```env
MONGODB_URI=mongodb://localhost:27017
```

Use MongoDB Atlas or a managed database URI.

3. Make model artifacts available in production.

The backend loads:

```text
models/production_model.joblib
models/best_model.joblib
models/preprocessor.joblib
```

Because `.gitignore` excludes `models/`, your hosting platform will not receive these files from Git unless you upload them separately, store them in object storage, or change the deployment process.

4. Do not deploy local secrets.

Never commit or upload the real `.env` publicly. Use platform environment variables.

5. Seed users before relying on `/login`.

The `/login` endpoint checks MongoDB collection `users`. Demo users in `app/auth/users.py` are not automatically inserted into MongoDB by the current API startup.

6. Clean `requirements.txt`.

The current file has pinned packages and repeated unpinned package names. It works locally only if all versions are available, but production builds are safer with one clean dependency list.

7. Decide where logs go.

The app writes to `logs/system.log`. On many platforms, local disk is temporary. Prefer console logs for production observability.

## 6. Recommended Hosting Architecture

Simple cloud deployment:

```text
Frontend: Vercel / Netlify / Render Static Site
Backend: Render Web Service / Railway / Fly.io / VPS Docker
Database: MongoDB Atlas
Model artifacts: bundled in backend image or downloaded during deploy
```

Production URLs example:

```text
Frontend URL: https://fraudshield-ui.example.com
Backend URL:  https://fraudshield-api.example.com
MongoDB:      MongoDB Atlas private/secured cluster
```

Environment link:

```text
frontend VITE_API_BASE_URL = backend public URL
backend CORS allow_origins = frontend public URL
```

## 7. Local Development Commands

Backend:

```bash
python -m venv .venv
.\.venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.api.main:app --host 0.0.0.0 --port 8000
```

Frontend:

```bash
cd frontend
npm ci
npm run dev
```

Full local Docker stack:

```bash
docker compose up --build
```

Local URLs:

```text
Backend:  http://127.0.0.1:8000
Docs:     http://127.0.0.1:8000/docs
Frontend: http://127.0.0.1:5173
MongoDB:  mongodb://localhost:27017
```

## 8. Docker Deployment

Backend image:

```bash
docker build -t fraudshield-api .
docker run --env-file .env -p 8000:8000 fraudshield-api
```

Frontend image:

```bash
cd frontend
docker build --build-arg VITE_API_BASE_URL=https://your-api-domain.com -t fraudshield-frontend .
docker run -p 8080:80 fraudshield-frontend
```

Full stack:

```bash
docker compose up --build
```

Production compose draft:

```bash
cd deployment
docker compose up --build
```

Note: `deployment/docker-compose.yml` serves only the API through Nginx. It does not serve the React frontend.

## 9. Render Deployment

Backend using `render.yaml`:

```text
Build command: pip install -r requirements.txt
Start command: uvicorn app.api.main:app --host 0.0.0.0 --port 10000
```

Set these Render environment variables:

```env
MONGODB_URI=
DATABASE_NAME=
JWT_SECRET_KEY=
GROQ_API_KEY=
MODEL_DIRECTORY=models
RATE_LIMIT_PER_MINUTE=60
```

Important: Render must also receive the `models/` artifacts. Git will ignore them unless deployment is adjusted.

Frontend on Render Static Site:

```text
Root directory: frontend
Build command: npm ci && npm run build
Publish directory: dist
Environment:
  VITE_API_BASE_URL=https://your-render-api.onrender.com
  VITE_CLERK_PUBLISHABLE_KEY=pk_xxx
```

## 10. Deployment Verification Checklist

Before deploy:

```bash
pytest
cd frontend
npm run build
```

After deploy:

```bash
curl https://your-api-domain.com/health
curl https://your-api-domain.com/version
curl https://your-api-domain.com/model/metadata
curl https://your-api-domain.com/metrics
```

Verify in browser:

```text
Frontend loads without "Clerk key required"
API status shows online
Dashboard summary loads
Prediction form can call /predict
Recent predictions appear after a prediction
MongoDB collections receive documents
```

## 11. Files to Keep Out of Production Builds

Usually exclude:

```text
.venv/
.pytest_cache/
__pycache__/
catboost_info/
data/fraud.csv
data/raw/creditcard.csv
logs/
reports/
notebooks/
tests/
clerk-react/
dashboard/
```

Keep for inference production:

```text
app/
models/
frontend/ or frontend/dist/
requirements.txt
Dockerfile
frontend/Dockerfile
deployment/
.env.example
README.md
```

## 12. Common Failure Points

| Symptom | Likely Cause | Fix |
| --- | --- | --- |
| API crashes on startup | Missing `models/production_model.joblib` or `models/preprocessor.joblib` | Upload model artifacts or bake them into image. |
| Frontend says API offline | Wrong `VITE_API_BASE_URL` or backend unavailable | Set frontend env and redeploy frontend. |
| Browser CORS error | Production frontend URL not in backend CORS list | Update `allow_origins` in `app/api/main.py`. |
| Login fails | No users in MongoDB | Create users through `/users` or seed MongoDB. |
| Dashboard empty | MongoDB has no predictions yet | Run a prediction first. |
| Groq explanation is simulated | `GROQ_API_KEY` missing | Set key if real LLM explanations are required. |
| Build fails on dependencies | Messy `requirements.txt` or unavailable versions | Clean and pin one dependency list. |
| Logs disappear | Ephemeral host disk | Use platform log drains / stdout logging. |

