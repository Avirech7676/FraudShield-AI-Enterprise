# FraudShield AI Enterprise - Production Deployment Guide

This guide details step-by-step production deployment procedures for FraudShield AI Enterprise using Docker, Nginx, FastAPI (Uvicorn), and MongoDB.

---

## Architecture Overview

```
                        +----------------------------+
                        |   Nginx Reverse Proxy     |
                        |      Port 80 / 443         |
                        +--------------+-------------+
                                       |
                   +-------------------+-------------------+
                   |                                       |
        +----------v----------+                 +----------v----------+
        |  React Frontend SPA |                 |  FastAPI ASGI Engine|
        |  (Nginx Static)     |                 |  (Uvicorn / Port 8000)|
        +---------------------+                 +----------+----------+
                                                           |
                                                +----------v----------+
                                                |   MongoDB Database  |
                                                |   (Port 27017)      |
                                                +---------------------+
```

---

## 1. Prerequisites & Environment Setup

Ensure the target production host has installed:
- **Docker Engine** >= 24.0.0
- **Docker Compose Plugin** >= v2.20.0
- Git & OpenSSL

### 1.1 Environment Variables (.env)

Create or update `.env` in the repository root:

```env
PORT=8000
MONGODB_URI=mongodb://mongodb:27017/FraudShieldDB
DATABASE_NAME=FraudShieldDB
JWT_SECRET_KEY=prod_super_secret_jwt_key_32_chars_min
JWT_ALGORITHM=HS256
JWT_EXPIRE_MINUTES=480
GROQ_API_KEY=your_groq_api_key_here
KAFKA_BOOTSTRAP_SERVERS=kafka:9092
FRONTEND_ORIGINS=http://localhost,http://your-domain.com
LOG_LEVEL=INFO
```

---

## 2. Docker Container Deployment

### 2.1 Building and Launching Services

Execute the following command to build and launch all services in detached background mode:

```bash
docker compose up -d --build
```

### 2.2 Verifying Container Status

Check that all 3 enterprise services are running cleanly:

```bash
docker compose ps
```

Expected Output:
```
NAME               IMAGE                     COMMAND                  SERVICE    CREATED          STATUS          PORTS
fraudshield-api    fraudshield-ai-api        "uvicorn app.api.ma…"   api        10 seconds ago   Up 8 seconds    0.0.0.0:8000->8000/tcp
fraudshield-web    fraudshield-ai-frontend   "/docker-entrypoint.…"   frontend   10 seconds ago   Up 8 seconds    0.0.0.0:80->80/tcp
fraudshield-db     mongo:7                   "docker-entrypoint.s…"   mongodb    10 seconds ago   Up 9 seconds    0.0.0.0:27017->27017/tcp
```

---

## 3. Health Checks & Verification

### 3.1 Backend Healthcheck

```bash
curl -f http://localhost:8000/health
```

Expected Response:
```json
{
  "status": "healthy",
  "database": true,
  "model": {"status": "ok"},
  "predictor": {"status": "ok"},
  "risk_engine": {"status": "ok"},
  "shap": {"status": "ok"},
  "groq": {"status": "ok"},
  "version": "2.0"
}
```

### 3.2 Frontend Access

Open `http://localhost` in your browser. Verify the glassmorphic split-screen login page loads cleanly.

---

## 4. Production Security & SSL Setup (Let's Encrypt / Certbot)

To attach a domain with SSL:

1. Install Certbot:
   ```bash
   sudo apt-get update && sudo apt-get install certbot python3-certbot-nginx
   ```
2. Generate SSL Certificate:
   ```bash
   sudo certbot --nginx -d your-domain.com
   ```
3. Auto-renewal Test:
   ```bash
   sudo certbot renew --dry-run
   ```

---

## 5. Maintenance & Logs

- **View Live Backend Logs**:
  ```bash
  docker compose logs -f api
  ```

- **Hot-Reload Machine Learning Models**:
  ```bash
  curl -X POST http://localhost:8000/settings/reload-model
  ```

- **Graceful Shutdown**:
  ```bash
  docker compose down
  ```
