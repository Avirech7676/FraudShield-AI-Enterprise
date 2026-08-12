# Database

MongoDB is the operational database for FraudShield AI Enterprise.

Primary collections:

- `users`
- `transactions`
- `predictions`
- `alerts`
- `cases`
- `analyst_feedback`
- `audit_logs`
- `models`
- `notifications`

Access should flow through `FraudRepository` in `app/database/repository.py`. This keeps collection names, timestamps, and persistence behavior centralized.
