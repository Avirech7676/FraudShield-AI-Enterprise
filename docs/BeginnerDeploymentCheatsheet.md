# FraudShield AI Enterprise: Beginner Deployment Cheatsheet

Use this if you want the simplest path to host the project.

## What You Are Hosting

Your app has 3 main parts:

```text
1. Backend API       -> FastAPI app in app/
2. Frontend website  -> React app in frontend/
3. Database          -> MongoDB
```

You also need the ML model files:

```text
models/production_model.joblib
models/preprocessor.joblib
```

Without these model files, the backend will not start correctly.

## Recommended Beginner Platforms

Use this setup:

| App Part | Platform |
| --- | --- |
| Frontend React app | Vercel |
| Backend FastAPI API | Render |
| Database | MongoDB Atlas |

Simple final architecture:

```text
User opens Vercel frontend
        |
        v
Frontend calls Render backend API
        |
        v
Backend saves data in MongoDB Atlas
        |
        v
Backend loads ML model from models/
```

## Step 1: Create MongoDB Atlas Database

1. Go to MongoDB Atlas.
2. Create a free cluster.
3. Create a database user.
4. Allow network access.
5. Copy your MongoDB connection string.

It will look like this:

```env
mongodb+srv://USERNAME:PASSWORD@cluster.mongodb.net/FraudShieldDB
```

You will use it as:

```env
MONGODB_URI=mongodb+srv://USERNAME:PASSWORD@cluster.mongodb.net/FraudShieldDB
DATABASE_NAME=FraudShieldDB
```

## Step 2: Host Backend on Render

Create a new Render Web Service.

Use these settings:

```text
Root Directory: leave empty
Build Command: pip install -r requirements.txt
Start Command: uvicorn app.api.main:app --host 0.0.0.0 --port 10000
```

Add these environment variables in Render:

```env
MONGODB_URI=your-mongodb-atlas-uri
DATABASE_NAME=FraudShieldDB

JWT_SECRET_KEY=your-long-random-secret
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

Optional environment variables:

```env
GROQ_API_KEY=
API_KEY=
ENCRYPTION_KEY=

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

After deploy, Render gives you a backend URL like:

```text
https://fraudshield-api.onrender.com
```

Test it:

```text
https://fraudshield-api.onrender.com/health
```

You should see:

```json
{
  "status": "healthy"
}
```

## Step 3: Host Frontend on Vercel

Create a new Vercel project.

Use these settings:

```text
Root Directory: frontend
Build Command: npm run build
Output Directory: dist
```

Add these environment variables in Vercel:

```env
VITE_API_BASE_URL=https://your-render-backend-url.onrender.com
VITE_CLERK_PUBLISHABLE_KEY=your-clerk-publishable-key
```

Example:

```env
VITE_API_BASE_URL=https://fraudshield-api.onrender.com
VITE_CLERK_PUBLISHABLE_KEY=pk_test_xxxxxxxxx
```

Important:

If `VITE_CLERK_PUBLISHABLE_KEY` is missing, your frontend will show:

```text
Clerk key required
```

## Step 4: Update Backend CORS

After Vercel deploys, it gives you a frontend URL like:

```text
https://fraudshield.vercel.app
```

Open:

```text
app/api/main.py
```

Find:

```python
allow_origins=[
    "http://localhost:5173",
    "http://127.0.0.1:5173",
    "http://localhost:4173",
    "http://127.0.0.1:4173",
]
```

Add your Vercel URL:

```python
allow_origins=[
    "http://localhost:5173",
    "http://127.0.0.1:5173",
    "http://localhost:4173",
    "http://127.0.0.1:4173",
    "https://fraudshield.vercel.app",
]
```

Then redeploy the backend on Render.

## Step 5: Make Sure Model Files Are Deployed

The backend needs:

```text
models/production_model.joblib
models/preprocessor.joblib
```

Your `.gitignore` currently ignores model files, so they may not upload automatically.

Beginner options:

```text
Option 1: Upload model files manually to your deployment environment.
Option 2: Temporarily allow model files in Git if your repo is private.
Option 3: Store models in cloud storage and download them during deploy.
```

For a beginner private project, the easiest option is usually:

```text
Keep models/ inside the deployed backend project.
```

Do not expose model files publicly if the model is private.

## Step 6: Final Environment Variable List

Backend envs for Render:

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

Frontend envs for Vercel:

```env
VITE_API_BASE_URL=
VITE_CLERK_PUBLISHABLE_KEY=
```

## Step 7: Test After Deployment

Test backend:

```text
https://your-backend-url/health
https://your-backend-url/version
https://your-backend-url/model/metadata
```

Test frontend:

```text
Open your Vercel URL
Check API status
Run one prediction
Check recent predictions
```

## Simple Deployment Checklist

```text
[ ] MongoDB Atlas database created
[ ] Backend deployed on Render
[ ] Backend env variables added
[ ] Model files available in backend deployment
[ ] Backend /health works
[ ] Frontend deployed on Vercel
[ ] Frontend env variables added
[ ] Vercel URL added to backend CORS
[ ] Backend redeployed after CORS update
[ ] Frontend can call backend
[ ] Prediction works
```

## Common Beginner Errors

| Problem | Reason | Fix |
| --- | --- | --- |
| Frontend says API offline | Wrong `VITE_API_BASE_URL` | Put Render backend URL in Vercel envs. |
| Browser shows CORS error | Vercel URL not allowed by backend | Add Vercel URL in `app/api/main.py`. |
| Backend crashes | Missing model files | Deploy `models/production_model.joblib` and `models/preprocessor.joblib`. |
| Login fails | No users in MongoDB | Add users through API or seed MongoDB. |
| Frontend says Clerk key required | Missing Clerk env | Add `VITE_CLERK_PUBLISHABLE_KEY` in Vercel. |
| Dashboard is empty | No predictions yet | Run one prediction first. |

