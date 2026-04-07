from openenv.core.env_client import EnvClient
from openenv.core.client_types import StepResult
from core.models import EmailAction, EmailObservation, EmailState

class EmailEnvClient(EnvClient):

    def _step_payload(self, action):
        return {"action_type": action.action_type, "content": action.content}

    def _parse_result(self, payload):
        obs = payload["observation"]
        return StepResult(
            observation=EmailObservation(
                done=payload["done"],
                reward=payload["reward"],
                email_text=obs["email_text"],
                sender=obs["sender"],
                subject=obs["subject"],
                history=obs["history"],
                message=obs["message"]
            ),
            reward=payload["reward"],
            done=payload["done"]
        )

    def _parse_state(self, payload):
        return EmailState(**payload)