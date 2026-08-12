# Deployment

Recommended deployment:

- FastAPI API: Railway or Render
- React dashboard: static hosting or the included frontend Docker image
- MongoDB: MongoDB Atlas
- Containerization: Docker
- CI/CD: GitHub Actions

Local Docker startup:

```bash
docker compose up --build
```

Production startup assets are stored in `deployment/`:

- `docker-compose.yml` for API, MongoDB, and Nginx.
- `nginx.conf` for reverse proxy readiness.
- `gunicorn.conf.py` for API worker settings.
- `startup.sh` for production container startup.

Before deployment:

- All tests pass.
- Docker image builds.
- `/health` returns HTTP 200.
- `/metrics` returns Prometheus-compatible output.
- MongoDB connection succeeds.
- Production model artifacts exist.
