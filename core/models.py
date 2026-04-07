from openenv.core.env_server import Action, Observation, State
from typing import List, Optional

class EmailAction(Action):
    action_type: str   # classify | prioritize | reply
    content: str

class EmailObservation(Observation):
    email_text: str
    sender: str
    subject: str
    history: List[str]
    message: str

class EmailState(State):
    current_index: int = 0
    total_emails: int = 0
    task_type: str = "easy"
    score: float = 0.0