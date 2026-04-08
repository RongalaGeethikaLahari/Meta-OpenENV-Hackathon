from openenv.core.env_server import create_fastapi_app
from server.environment import EmailEnv
from core.models import EmailAction, EmailObservation

import uvicorn

app = create_fastapi_app(
    EmailEnv,
    EmailAction,
    EmailObservation
)

# ✅ REQUIRED ENTRY POINT
def main():
    uvicorn.run(
        "server.app:app",
        host="0.0.0.0",
        port=8000,
        reload=False
    )

# ✅ REQUIRED
if __name__ == "__main__":
    main()