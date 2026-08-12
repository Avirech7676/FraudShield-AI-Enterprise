# Developer Guide

Development workflow:

1. Create a virtual environment.
2. Install `requirements.txt`.
3. Copy `.env.example` to `.env` and fill local values.
4. Run the API with Uvicorn.
5. Run tests with Pytest.
6. Build Docker before deployment.

Useful commands:

```bash
python -m pip install --upgrade pip
pip install -r requirements.txt
pytest --cov=app --cov-report=html
uvicorn app.api.main:app --host 0.0.0.0 --port 8000
docker compose up --build
```

Contribution guidelines:

- Keep one implementation per responsibility.
- Route MongoDB access through `FraudRepository`.
- Use centralized settings for runtime configuration.
- Replace console prints with structured logging.
- Add tests for API, ML, repository, authentication, feature engineering, and monitoring changes.
