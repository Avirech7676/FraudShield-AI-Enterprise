# FraudShield AI Enterprise - Complete Project Report & Technical Manual

---

## Copyright Notice

```
Copyright (c) 2026 Avinash Reddy Ch
All Rights Reserved.

FraudShield AI Enterprise is proprietary software developed and owned by
Avinash Reddy Ch. No part of this software - including source code, model
artifacts, documentation, UI/UX design, training pipelines, or data schemas -
may be reproduced, distributed, modified, or used in any commercial or
non-commercial product without explicit written permission from the owner.

Project:    FraudShield AI Enterprise
Version:    2.0 Production Release
Author:     Avinash Reddy Ch
Contact:    avinashreddych7@gmail.com
GitHub:     github.com/Avirech7676/FraudShield-AI-Enterprise
Year:       2026
License:    Proprietary - All Rights Reserved
```

---

## Table of Contents

1. [Project Overview](#1-project-overview)
2. [System Architecture](#2-system-architecture)
3. [Technology Stack](#3-technology-stack)
4. [Machine Learning Model](#4-machine-learning-model)
5. [Feature Engineering Pipeline](#5-feature-engineering-pipeline)
6. [Risk Engine](#6-enterprise-risk-engine)
7. [SHAP Explainability](#7-shap-explainability-xai)
8. [API Reference](#8-api-reference)
9. [Frontend Pages and Features](#9-frontend-pages-and-features)
10. [Project Directory Structure](#10-project-directory-structure)
11. [Local Setup and Run Guide](#11-local-setup-and-run-guide)
12. [Model Verification and Health Checks](#12-model-verification-and-health-checks)
13. [Deployment Guide](#13-deployment-guide)
14. [Security and Authentication](#14-security-and-authentication)
15. [Database Schema](#15-database-schema)

---

## 1. Project Overview

**FraudShield AI Enterprise** is an enterprise-grade, real-time fraud detection platform powered by an ensemble machine learning model, explainable AI (SHAP), a hybrid rule-based risk engine, Groq LLM-powered analysis, and a full-stack web application for fraud monitoring and investigation.

### What It Does

- Detects fraud transactions in real time using a trained CatBoost Stacking Ensemble model
- Scores every transaction through an 8-component hybrid Risk Engine producing a 0-100 Enterprise Risk Score
- Explains every decision using SHAP (SHapley Additive exPlanations) feature attribution
- Generates AI briefs using Groq LLaMA LLM for human-readable fraud narratives
- Provides a complete SOC dashboard - alerts, cases, analytics, audit logs, user management
- Supports live streaming predictions through a Kafka-ready pipeline

### Key Capabilities

| Capability | Description |
|---|---|
| Real-Time Prediction | Sub-500ms inference per transaction |
| Fraud Score | Enterprise Risk Score 0-100 with 6 risk tiers |
| XAI | SHAP feature waterfall with top-10 factor attribution |
| AI Reports | LLM-generated natural language threat briefs |
| Case Management | Create, assign, and resolve fraud investigation cases |
| Threat Alerts | Auto-generated alerts with priority ranking (P1-P5) |
| Audit Logs | Full transaction history with downloadable reports |
| Analytics | Real-time charts - risk distribution, velocity, prediction trends |
| Model Registry | Model version management and live hot-swap |
| User Management | Role-based access control (Admin, Analyst, Viewer) |

---

## 2. System Architecture

```
CLIENT LAYER: React 18 + TypeScript SPA (Vite / Nginx) - Port 5173 (dev) / 80 (prod)
                                    |
                             REST API (JWT Auth)
                                    |
BACKEND LAYER: FastAPI ASGI Engine (Uvicorn) - Port 8000
 - ML Model (CatBoost Stacking)
 - Risk Engine (8-Weight Hybrid Scoring)
 - SHAP XAI Explainer
 - Groq LLM Reports
 - Auth JWT RBAC
 - Feature Pipeline (48 Features)
                                    |
                             PyMongo / Motor
                                    |
DATA LAYER: MongoDB Atlas - FraudShieldDB
 Collections: predictions, users, cases, alerts, audit_logs, model_registry
```

### Request Flow

```
Transaction Input
   -> Feature Engineering Pipeline (48 features)
   -> CatBoost Stacking Ensemble -> Fraud Probability (0-1)
   -> Enterprise Risk Engine (8 weighted components) -> Risk Score (0-100)
   -> SHAP Explainer -> Top 10 Feature Attributions
   -> Groq LLM -> Natural Language Threat Brief
   -> MongoDB -> Persist result
   -> API Response -> Frontend Dashboard
```

---

## 3. Technology Stack

### Backend
| Technology | Version | Purpose |
|---|---|---|
| Python | 3.12 | Core runtime |
| FastAPI | 0.115.6 | ASGI web framework |
| Uvicorn | 0.34.0 | ASGI server |
| Pydantic | 2.10.4 | Data validation and settings |

### Machine Learning
| Technology | Version | Purpose |
|---|---|---|
| CatBoost | 1.2.7 | Primary fraud detection model |
| XGBoost | 2.1.3 | Ensemble stacking base learner |
| LightGBM | 4.5.0 | Ensemble stacking base learner |
| scikit-learn | 1.5.2 | Preprocessing and stacking |
| imbalanced-learn | 0.12.4 | SMOTE class balancing |
| SHAP | 0.46.0 | Explainable AI (feature attribution) |
| NumPy | 1.26.4 | Numerical computing |
| pandas | 2.2.3 | Data manipulation |
| joblib | 1.4.2 | Model artifact serialization |

### AI / LLM
| Technology | Version | Purpose |
|---|---|---|
| Groq | 0.13.1 | LLaMA 3.1 LLM API for threat narratives |

### Database
| Technology | Version | Purpose |
|---|---|---|
| MongoDB Atlas | Cloud | Primary database (hosted) |
| PyMongo | 4.10.1 | Synchronous MongoDB driver |
| Motor | 3.7.1 | Async MongoDB driver |

### Authentication and Security
| Technology | Version | Purpose |
|---|---|---|
| python-jose | 3.3.0 | JWT token encoding/decoding |
| bcrypt | 4.2.1 | Password hashing |
| passlib | 1.7.4 | Password utilities |

### Frontend
| Technology | Version | Purpose |
|---|---|---|
| React | 18 | UI framework |
| TypeScript | 5 | Type-safe JavaScript |
| Vite | 6.4.3 | Build tool and dev server |
| React Router | 6 | SPA routing |
| Axios | Latest | HTTP client |
| Recharts | Latest | Data visualization charts |
| Lucide React | Latest | Icon library |
| Nginx | 1.27-alpine | Production static file serving |

### Infrastructure
| Technology | Purpose |
|---|---|
| Docker | Container build |
| Docker Compose | Multi-service orchestration |
| Render.com | Cloud PaaS hosting |
| Vercel | Frontend hosting option |
| MongoDB Atlas | Managed cloud database |

---

## 4. Machine Learning Model

### Model Architecture: Enterprise CatBoost Stacking Ensemble v2.0

The model uses a stacking ensemble strategy where multiple base learners contribute predictions that a meta-learner combines for the final fraud probability.

```
STACKING ENSEMBLE:

Layer 1 - Base Learners (trained on k-fold CV):
  CatBoost Classifier  |  XGBoost Classifier  |  LightGBM Classifier

Layer 2 - Meta-Learner:
  Logistic Regression (Final Fraud Probability 0-1)
```

### Training Pipeline Steps

1. Data Loading - CSV dataset (data/raw/creditcard.csv)
2. Feature Engineering - 48 features generated from raw transaction fields
3. Preprocessing - OrdinalEncoder + StandardScaler column transformations
4. Class Balancing - SMOTE oversampling (corrects class imbalance)
5. Train/Test Split - 80/20 stratified split
6. Model Training - CatBoost + XGBoost + LightGBM -> Logistic Regression meta-learner
7. Evaluation - Accuracy, Precision, Recall, F1, ROC-AUC
8. Serialization - joblib.dump() to models/production_model.joblib

### Model Performance Metrics

| Metric | Score |
|---|---|
| Accuracy | 99.94% |
| Precision | 86.75% |
| Recall | 75.79% |
| F1 Score | 80.90% |
| ROC-AUC | 93.41% |
| Inference Latency | ~350 ms per transaction |

### Model Artifacts

| File | Size | Description |
|---|---|---|
| models/production_model.joblib | 10.7 MB | Trained stacking ensemble |
| models/best_model.joblib | 10.7 MB | Best checkpoint |
| models/preprocessor.joblib | 3.9 KB | Feature preprocessing pipeline |
| models/feature_names.joblib | 1.8 KB | 44 ML feature names |
| models/model_metadata.json | 327 B | Version and metric metadata |

### Train a New Model

```bash
# Place creditcard.csv in data/raw/
python train.py
```

---

## 5. Feature Engineering Pipeline

The pipeline processes raw transaction fields into 48 engineered features across 6 categories.

### Input Fields (Raw)

| Field | Type | Description |
|---|---|---|
| Amount | float | Transaction amount in USD |
| Merchant | string | Merchant name |
| Country | string | Transaction country code |
| VPN_Detection | bool | VPN detected at time of transaction |
| TOR_Detection | bool | TOR exit node detected |
| Device_Trust_Score | float | Device trust score 0-100 |
| IP_Reputation | float | IP reputation score 0-100 |
| Location_Jump | bool | Impossible velocity location change |
| Device_Change | bool | New device detected |
| Emulator_Detection | bool | Android/iOS emulator detected |
| Rooted_Device | bool | Jailbroken or rooted device |
| Login_Failure_Count | int | Failed login attempts |
| Password_Reset | bool | Password reset in session |
| Transactions_Last_Hour | int | Velocity - transactions per hour |
| Transactions_Last_Day | int | Daily transaction count |
| Previous_Fraud | int | Historical fraud incident count |

### 6 Feature Groups (48 Total Features)

**Group 1 - Amount Features:**
Log_Amount, High_Amount, Amount_Bucket

**Group 2 - Device and Network Features:**
Browser, Operating_System, Emulator_Detection, Rooted_Device, Jailbreak_Detection, Device_Fingerprint

**Group 3 - Geo and Network Features:**
City, ISP, ASN, TOR_Detection, International, IP_Reputation, Geo_Risk

**Group 4 - Merchant Features:**
Merchant_Category, Merchant_Risk, Merchant_Chargeback_Rate, Merchant_Country, High_Risk_Merchant, Merchant_Age_Months

**Group 5 - Behavioral Features:**
Transactions_Last_Hour, Transactions_Last_Day, Velocity_Score, Login_Failure_Count, Password_Reset, Device_Change, Location_Jump, Merchant_Diversity, Time_Since_Last_Transaction, Behavior_Score, Previous_Fraud_Count

**Group 6 - Rolling / Historical Features:**
Previous_Transactions, Rolling_Avg_Amount, Rolling_Max_Amount, Rolling_Min_Amount, Rolling_Std_Amount, Rolling_Total_Amount, Average_Daily_Spend, Spending_Trend, High_Spending_Flag, Spending_Volatility

---

## 6. Enterprise Risk Engine

The Risk Engine combines 8 weighted scoring components into a single Enterprise Risk Score (0-100).

### Risk Score Formula

```
Enterprise Risk Score =
  (ML Probability x 100) x 0.35   <- 35% weight
  + Rule Score            x 0.15   <- 15% weight
  + Behavior Score        x 0.15   <- 15% weight
  + Anomaly Score         x 0.10   <- 10% weight
  + (100 - Device Trust)  x 0.10   <- 10% weight
  + Geo Risk              x 0.05   <-  5% weight
  + Merchant Risk         x 0.05   <-  5% weight
  + Fraud History         x 0.05   <-  5% weight
```

### Risk Tiers

| Score Range | Risk Tier | Recommended Action |
|---|---|---|
| 0-20 | Very Low | Approve |
| 20-40 | Low | Approve and Monitor |
| 40-55 | Medium | Enhanced Monitoring |
| 55-70 | High | Trigger MFA |
| 70-85 | Critical | Block and Investigate |
| 85-100 | Extreme | Block and Escalate |

---

## 7. SHAP Explainability (XAI)

FraudShield uses SHAP (SHapley Additive exPlanations) to explain every prediction.

### How It Works

1. The trained model prediction is run through shap.TreeExplainer
2. SHAP values are computed for each of the 44 ML features
3. Features are ranked by absolute SHAP value (impact magnitude)
4. Top 10 factors are returned with positive/negative attribution
5. Frontend renders a feature waterfall bar chart

### Sample SHAP Output

```json
{
  "shap_values": [
    { "feature": "Device_Trust_Score", "impact": 0.42 },
    { "feature": "VPN_Detection",      "impact": 0.38 },
    { "feature": "Location_Jump",      "impact": 0.31 },
    { "feature": "IP_Reputation",      "impact": 0.28 },
    { "feature": "Amount",             "impact": 0.15 }
  ],
  "counterfactual": {
    "Increase Device Trust Score above 75": "Reduces risk score by -38.5 points",
    "Disable VPN and Connect via Residential IP": "Reduces risk score by -24.2 points"
  }
}
```

---

## 8. API Reference

**Base URL**: http://localhost:8000
**Authentication**: Authorization: Bearer {JWT_TOKEN}

| Method | Endpoint | Description |
|---|---|---|
| POST | /login | Obtain JWT token |
| POST | /register | Create new account |
| GET | /me | Current user info |
| POST | /predict | Run fraud prediction |
| GET | /predictions | List stored predictions |
| GET | /explanation/{transaction_id} | SHAP explanation for transaction |
| POST | /explanation | SHAP for custom features |
| GET | /analytics/summary | Dashboard KPI metrics |
| GET | /analytics/risk-distribution | Risk tier chart data |
| GET | /cases | List fraud investigation cases |
| POST | /cases | Create new case |
| GET | /alerts | List threat alerts |
| GET | /users | List platform users (Admin) |
| GET | /settings | Platform configuration |
| POST | /settings/reload-model | Hot-reload ML model |
| GET | /health | System health status |
| GET | /docs | Swagger API documentation |

### Sample Prediction Request

```bash
curl -X POST http://localhost:8000/predict \
  -H "Authorization: Bearer YOUR_JWT_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "Amount": 42000.00,
    "Merchant": "DarkWeb Exchange Ltd",
    "Country": "RU",
    "VPN_Detection": true,
    "TOR_Detection": true,
    "Device_Trust_Score": 5,
    "IP_Reputation": 98,
    "Location_Jump": true
  }'
```

---

## 9. Frontend Pages and Features

| Route | Page | Description |
|---|---|---|
| /login | Login | JWT authentication |
| /register | Register | New account creation |
| /dashboard | Dashboard | Live KPI metrics, charts |
| /prediction | Prediction | Interactive fraud form |
| /explanation/:id | SHAP Explainer | Feature attribution waterfall |
| /history | Audit Logs | Full transaction history |
| /alerts | Threat Alerts | Priority-ranked alerts |
| /analytics | Analytics | Risk distribution charts |
| /cases | Case Management | Fraud investigation cases |
| /reports | AI Reports | LLM-generated threat reports |
| /model | Model Registry | Model versioning and hot-swap |
| /users | User Management | User CRUD (Admin only) |
| /settings | Settings | Platform configuration |

---

## 10. Project Directory Structure

```
FraudShield-AI-Enterprise/
├── app/                          <- FastAPI backend application
│   ├── api/
│   │   ├── main.py               <- FastAPI app entry point
│   │   └── routes.py             <- All API endpoint definitions
│   ├── auth/jwt_handler.py       <- JWT encode/decode/verify
│   ├── config/
│   │   ├── settings.py           <- Pydantic settings (env vars)
│   │   └── logging_config.py     <- Structured logging
│   ├── database/repository.py    <- MongoDB CRUD operations
│   ├── features/
│   │   ├── feature_engineering.py <- Main pipeline controller
│   │   └── feature_pipeline.py   <- Feature group definitions
│   ├── inference/predictor.py    <- EnterpriseFraudPredictor class
│   ├── ml/
│   │   ├── preprocessing.py      <- DataPreprocessor
│   │   └── trainer.py            <- EnterpriseFraudTrainer
│   ├── rules/risk_engine.py      <- EnterpriseRiskEngine class
│   ├── services/prediction_service.py <- Async prediction orchestrator
│   └── xai/shap_explainer.py    <- SHAP feature attribution
│
├── frontend/                     <- React TypeScript frontend
│   ├── src/
│   │   ├── apiClient.ts          <- Axios instance with interceptors
│   │   ├── components/           <- Reusable UI components
│   │   ├── pages/                <- Route-level page components
│   │   ├── services/             <- API service functions
│   │   └── types/                <- TypeScript interfaces
│   ├── Dockerfile                <- nginx:1.27-alpine container
│   └── nginx.conf                <- Nginx SPA routing config
│
├── models/                       <- ML model artifacts
│   ├── production_model.joblib   <- Active production model (10.7 MB)
│   ├── preprocessor.joblib       <- Feature preprocessing pipeline
│   ├── feature_names.joblib      <- Ordered feature list
│   └── model_metadata.json       <- Version and performance metrics
│
├── data/raw/                     <- Raw training datasets (gitignored)
├── tests/                        <- Pytest test suite
├── reports/                      <- Generated PDF/Excel reports
├── logs/                         <- Application logs
├── main.py                       <- Uvicorn launcher entry point
├── train.py                      <- Model training CLI script
├── predict.py                    <- CLI inference script
├── Dockerfile                    <- Backend Docker image
├── docker-compose.yml            <- 3-service orchestration
├── render.yaml                   <- Render.com deployment config
├── requirements.txt              <- Python dependencies
├── .env                          <- Local environment variables
└── DEPLOYMENT.md                 <- Deployment guide
```

---

## 11. Local Setup and Run Guide

### Prerequisites

- Python 3.12+
- Node.js 22+
- MongoDB Atlas account (or local MongoDB 7)
- Git

### Step 1 - Clone Repository

```bash
git clone https://github.com/Avirech7676/FraudShield-AI-Enterprise.git
cd FraudShield-AI-Enterprise
```

### Step 2 - Backend Setup

```bash
# Create virtual environment
python -m venv .venv

# Activate (Windows):
.venv\Scripts\activate

# Activate (macOS/Linux):
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### Step 3 - Configure Environment

```bash
cp .env.example .env
# Edit .env with your values (MongoDB URI, JWT secret, Groq API key)
```

Required .env values:
```
MONGODB_URI=mongodb+srv://USER:PASS@cluster0.xxxxx.mongodb.net/
DATABASE_NAME=FraudShieldDB
JWT_SECRET_KEY=your_strong_32char_secret_here
GROQ_API_KEY=your_groq_api_key_here
FRONTEND_ORIGINS=http://localhost:5173
MODEL_DIRECTORY=models
MODEL_VERSION=2.0
```

### Step 4 - Start Backend

```bash
python main.py
# Backend: http://localhost:8000
# API Docs: http://localhost:8000/docs
```

### Step 5 - Start Frontend

```bash
cd frontend
npm install
npm run dev
# Frontend: http://localhost:5173
```

### Step 6 - CLI Prediction Test

```bash
# Default payload (Genuine transaction test)
python predict.py

# Fraud payload test
python predict.py "{\"Amount\": 42000, \"Merchant\": \"DarkWeb Exchange\", \"Country\": \"RU\", \"VPN_Detection\": true, \"TOR_Detection\": true, \"Device_Trust_Score\": 5}"
```

### Default Login Credentials

| Field | Value |
|---|---|
| Username | admin |
| Password | admin123 |
| Role | Admin |

---

## 12. Model Verification and Health Checks

### Backend Health Check

```bash
curl http://localhost:8000/health
```

Expected:
```json
{ "status": "healthy", "database": true, "model": {"status": "ok"}, "version": "2.0" }
```

### Model Test Cases

**Genuine Transaction (Should get Very Low / Low Risk):**
```bash
python predict.py "{\"Amount\": 45, \"Merchant\": \"Starbucks\", \"Country\": \"US\", \"VPN_Detection\": false, \"Device_Trust_Score\": 95}"
# Expected: Genuine, Very Low risk, Approve
```

**Fraud Transaction (Should get High / Critical / Extreme Risk):**
```bash
python predict.py "{\"Amount\": 42000, \"Merchant\": \"DarkWeb Exchange\", \"Country\": \"RU\", \"VPN_Detection\": true, \"TOR_Detection\": true, \"Device_Trust_Score\": 5, \"IP_Reputation\": 98, \"Location_Jump\": true}"
# Expected: Risk Score >= 60, High/Critical tier, Block/MFA action
```

### Frontend Verification Checklist

| Page | Test Action | Expected Result |
|---|---|---|
| /login | Login with admin / admin123 | Redirect to /dashboard |
| /dashboard | Load page | KPI cards with live data, charts render |
| /prediction | Submit transaction form | Risk score and prediction result shown |
| /history | Click Details button | Modal opens with transaction details |
| /history | Click SHAP button | SHAP explanation page with feature bars |
| /alerts | Load page | Alert list with priority badges |
| /analytics | Load page | Pie and bar charts render |
| /model | Load page | Model metrics: 99.94% accuracy |

---

## 13. Deployment Guide

### Docker Compose (VPS / Server)

```bash
docker compose up -d --build
docker compose ps
curl http://localhost:8000/health
```

### Render.com (Cloud)

1. Push code to GitHub
2. Connect repo at render.com (auto-detects render.yaml)
3. Set secret env vars: MONGODB_URI, JWT_SECRET_KEY, GROQ_API_KEY, FRONTEND_ORIGINS
4. Deploy

### SSL / HTTPS (Ubuntu VPS)

```bash
sudo apt-get install certbot python3-certbot-nginx
sudo certbot --nginx -d yourdomain.com
sudo certbot renew --dry-run
```

---

## 14. Security and Authentication

### JWT Flow

```
User provides username + password
   -> /login -> bcrypt verify password hash
   -> Generate JWT (HS256)
   -> Client stores token
   -> Every API request: Authorization: Bearer {token}
   -> JWTHandler.verify_token() validates
   -> Protected endpoint executes
```

### Role-Based Access Control (RBAC)

| Role | Permissions |
|---|---|
| Admin | Full access - users, settings, model management |
| Analyst | Predictions, cases, alerts, analytics, reports |
| Viewer | Read-only dashboard and audit logs |

### Security Measures

- Passwords hashed with bcrypt (salt rounds 12)
- JWT tokens expire after 60 minutes (configurable)
- CORS restricted to FRONTEND_ORIGINS whitelist
- Rate limiting via RATE_LIMIT_PER_MINUTE env var
- All secrets read from .env - never hardcoded

---

## 15. Database Schema

### predictions Collection

```json
{
  "transaction_id": "UUID",
  "prediction": "Fraud | Genuine",
  "fraud_probability": 0.94,
  "risk_score": 0.87,
  "enterprise_risk_score": 87.3,
  "enterprise_risk_tier": "Extreme",
  "Latency_ms": 351.4,
  "merchant": "DarkWeb Exchange Ltd",
  "country": "RU",
  "amount": 42000,
  "llm_explanation": "Transaction flagged due to...",
  "shap": { "top_factors": [...] },
  "created_at": "2026-08-12T07:00:00Z"
}
```

### users Collection

```json
{
  "username": "admin",
  "email": "admin@fraudshield.ai",
  "hashed_password": "$2b$12$...",
  "role": "Admin",
  "created_at": "2026-08-01T00:00:00Z",
  "is_active": true
}
```

### cases Collection

```json
{
  "case_id": "CASE-2026-001",
  "transaction_id": "UUID",
  "title": "High-value fraud syndicate transaction",
  "status": "open | investigating | resolved | closed",
  "priority": "P1",
  "assigned_to": "analyst@fraudshield.ai",
  "created_at": "...",
  "updated_at": "..."
}
```

---

## Quick Reference Card

```
FRAUDSHIELD AI ENTERPRISE v2.0 - Quick Reference
================================================
BACKEND   : http://localhost:8000
FRONTEND  : http://localhost:5173
API DOCS  : http://localhost:8000/docs
HEALTH    : http://localhost:8000/health

LOGIN     : admin / admin123
DB        : MongoDB Atlas - FraudShieldDB

MODEL     : CatBoost Stacking Ensemble v2.0
ACCURACY  : 99.94%   ROC-AUC : 93.41%
FEATURES  : 48 engineered | 44 ML-ready
LATENCY   : ~350ms per prediction

START BACKEND  : python main.py
START FRONTEND : cd frontend && npm run dev
TRAIN MODEL    : python train.py
CLI PREDICT    : python predict.py
DOCKER DEPLOY  : docker compose up -d --build
================================================
```

---

*FraudShield AI Enterprise - Copyright (c) 2026 Avinash Reddy Ch. All Rights Reserved.*
