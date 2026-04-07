from openenv.core.env_server import create_fastapi_app
from server.environment import EmailEnv
from core.models import EmailAction, EmailObservation

app = create_fastapi_app(
    EmailEnv,
    EmailAction,
    EmailObservation
)