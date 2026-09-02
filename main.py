import uvicorn
import os
from dotenv import load_dotenv

load_dotenv()

if __name__ == "__main__":
    port = int(os.getenv("PORT", 8000))
    print(f"Starting FraudShield AI Enterprise Server on port {port}...")
    uvicorn.run("app.api.main:app", host="0.0.0.0", port=port, reload=False)
