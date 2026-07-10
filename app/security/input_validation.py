import re


class InputValidator:
    BLOCKED_PATTERNS = [
        re.compile(pattern, re.IGNORECASE)
        for pattern in [
            r"<script",
            r"javascript:",
            r"drop\s+table",
            r"insert\s+into",
            r"delete\s+from",
        ]
    ]

    @classmethod
    def sanitize_string(cls, value):
        cleaned = value.strip()
        for pattern in cls.BLOCKED_PATTERNS:
            cleaned = pattern.sub("", cleaned)
        return cleaned

    @classmethod
    def sanitize_payload(cls, payload):
        if isinstance(payload, dict):
            return {
                key: cls.sanitize_payload(value)
                for key, value in payload.items()
            }
        if isinstance(payload, list):
            return [cls.sanitize_payload(value) for value in payload]
        if isinstance(payload, str):
            return cls.sanitize_string(payload)
        return payload
