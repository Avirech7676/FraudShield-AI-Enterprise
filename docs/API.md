# API

Main endpoints:

- `GET /` returns service status.
- `GET /health` returns health status.
- `GET /version` returns API and platform version details.
- `GET /metrics` returns Prometheus-compatible observability metrics.
- `POST /predict` scores a single transaction.
- `POST /batch_predict` scores multiple transactions.
- `GET /predictions` lists saved predictions.

Standard response target:

```json
{
  "success": true,
  "message": "Prediction completed",
  "data": {}
}
```

Authentication is handled through JWT utilities under `app/auth` and API route modules under `app/api`.
