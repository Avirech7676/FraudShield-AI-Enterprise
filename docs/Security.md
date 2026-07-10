# Security

Security controls:

- JWT authentication for protected API workflows.
- Optional API key validation through `X-API-Key`.
- In-memory rate limiting helper for API protection.
- Request payload sanitization helpers.
- Encryption helpers for sensitive values.
- Security audit logging.

Runtime secrets belong in `.env` or the deployment platform secret store. Commit `.env.example`, not `.env`.

Important environment variables:

- `JWT_SECRET_KEY`
- `JWT_ALGORITHM`
- `JWT_EXPIRE_MINUTES`
- `API_KEY`
- `ENCRYPTION_KEY`
- `MONGODB_URI`
- `GROQ_API_KEY`
- Notification provider credentials
