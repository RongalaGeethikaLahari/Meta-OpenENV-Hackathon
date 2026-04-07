import uuid
import random
from openenv.core.env_server import Environment
from core.models import EmailAction, EmailObservation, EmailState
from core.dataset import load_dataset


class EmailEnv(Environment):

    def __init__(self):
        self.state_obj = EmailState()

        # RL STATE
        self.inbox = []
        self.current_email = None
        self.done = False

        self.total_reward = 0.0
        self.missed_urgent = 0
        self.processed = 0

        # dataset cache
        self.dataset = load_dataset()

    # ---------------- RESET ----------------

    def reset(self, **kwargs):
        task = kwargs.get("task", "easy")

        # ---- DATA SPLIT ----
        if task == "easy":
            emails = self.dataset[:100]
        elif task == "medium":
            emails = self.dataset[100:400]
        else:
            emails = self.dataset[400:800]

        emails = emails.copy()
        random.shuffle(emails)

        self.inbox = emails
        self.current_email = self.inbox.pop(0)

        self.done = False
        self.total_reward = 0.0
        self.missed_urgent = 0
        self.processed = 0

        self.state_obj = EmailState(
            episode_id=str(uuid.uuid4()),
            step_count=0,
            current_index=0,
            total_emails=len(emails),
            task_type=task,
            score=0.0
        )

        return self._build_obs(0.0, "Start episode")

    # ---------------- STEP ----------------

    def step(self, action: EmailAction, **kwargs):

        if self.done:
            return self._final_obs(0.0)

        self.state_obj.step_count += 1
        self.processed += 1

        gt = self.current_email.get("label")

        # -------- NEW BALANCED RL REWARD --------
        
        reward = 0.0
        
        # 1. Correct classification
        if action.content == gt:
            reward += 2.0
        else:
            reward -= 0.5
        
        # 2. Urgent handling (important but not destructive)
        if gt == "urgent":
            if action.content == "urgent":
                reward += 1.5
            else:
                reward -= 1.0
                self.missed_urgent += 1
        
        # 3. Small step penalty
        reward -= 0.01
        
        # 4. Progress reward (VERY IMPORTANT)
        progress = 1.0 / (len(self.inbox) + 1)
        reward += progress


        # 6️⃣ Stability bonus (consistent good actions)
        if reward > 0:
            reward += 0.2

        # ---------------------------------

        self.total_reward += reward
        self.state_obj.score = self.total_reward

        # -------- TRANSITION --------

        if len(self.inbox) > 0:
            self.current_email = self.inbox.pop(0)
        else:
            self.done = True

        # -------- TERMINATION --------

        # Too many critical failures
        if self.missed_urgent >= 3:
            self.done = True
            reward -= 5.0

        # Episode completion bonus
        if self.done:
            completion_bonus = 5.0 * (1 - self.missed_urgent / (self.processed + 1))
            reward += completion_bonus
            self.total_reward += completion_bonus

        # ---------------------------------

        return self._build_obs(reward, "Step complete")

    # ---------------- OBS BUILDER ----------------

    def _build_obs(self, reward, msg):

        urgency_ratio = self._urgent_ratio()

        return EmailObservation(
            done=self.done,
            reward=reward,
            email_text=self.current_email["text"] if not self.done else "Inbox Cleared",
            sender="real_user@enron.com",
            subject="Email",
            history=[
                f"processed:{self.processed}",
                f"missed_urgent:{self.missed_urgent}",
                f"total_reward:{self.total_reward:.2f}"
            ],
            message=f"{msg} | inbox:{len(self.inbox)} | urgency_ratio:{urgency_ratio:.2f}"
        )

    # ---------------- HELPERS ----------------

    def _urgent_ratio(self):
        if len(self.inbox) == 0:
            return 0.0
        urgent = sum(1 for e in self.inbox if e.get("label") == "urgent")
        return urgent / len(self.inbox)

    def _final_obs(self, reward):
        return EmailObservation(
            done=True,
            reward=reward,
            email_text="Episode finished",
            sender="system",
            subject="Done",
            history=[],
            message="All emails processed"
        )

    # ---------------- STATE ----------------

    @property
    def state(self):
        return self.state_obj