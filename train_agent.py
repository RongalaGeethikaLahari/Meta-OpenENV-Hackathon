import torch
import torch.nn as nn
import torch.optim as optim
import asyncio

from client import EmailEnvClient
from core.models import EmailAction

import ssl
import certifi

ssl._create_default_https_context = ssl._create_unverified_context

# ---------- ACTION SPACE ----------

ACTIONS = ["spam", "important", "urgent"]


# ---------- POLICY NETWORK ----------

class PolicyNet(nn.Module):
    def __init__(self):
        super().__init__()

        self.fc = nn.Sequential(
            nn.Linear(10, 64),
            nn.ReLU(),
            nn.Linear(64, 32),
            nn.ReLU(),
            nn.Linear(32, len(ACTIONS)),
            nn.Softmax(dim=-1)
        )

    def forward(self, x):
        return self.fc(x)


# ---------- STATE ENCODER ----------

def encode_state(obs):
    text = obs.email_text.lower()

    features = [
        int("free" in text),
        int("win" in text),
        int("urgent" in text),
        int("asap" in text),
        int("deadline" in text),
        int("meeting" in text),
        int("offer" in text),
        int("client" in text),
        int("server" in text),
        int("issue" in text),
    ]

    return torch.tensor(features, dtype=torch.float32)


# ---------- TRAIN LOOP ----------

async def train():

    env = EmailEnvClient(base_url="https://adamk29-meta-openenv-hackathon.hf.space")
    await env.__aenter__()

    model = PolicyNet()
    optimizer = optim.Adam(model.parameters(), lr=0.003)

    EPISODES = 50
    GAMMA = 0.99
    ENTROPY_BETA = 0.01

    for episode in range(EPISODES):

        result = await env.reset(task="medium")

        log_probs = []
        rewards = []
        entropies = []

        while True:

            state = encode_state(result.observation)

            probs = model(state)

            # Add exploration noise
            probs = probs + 1e-6
            probs = probs / probs.sum()

            dist = torch.distributions.Categorical(probs)

            action_idx = dist.sample()
            action = ACTIONS[action_idx.item()]

            result = await env.step(
                EmailAction(action_type="classify", content=action)
            )

            reward = result.reward or 0.0

            log_probs.append(dist.log_prob(action_idx))
            rewards.append(reward)
            entropies.append(dist.entropy())

            if result.done:
                break

        # ---------- COMPUTE DISCOUNTED RETURNS ----------

        returns = []
        G = 0

        for r in reversed(rewards):
            G = r + GAMMA * G
            returns.insert(0, G)

        returns = torch.tensor(returns)

        # Normalize returns (VERY IMPORTANT)
        returns = (returns - returns.mean()) / (returns.std() + 1e-8)

        # ---------- LOSS ----------

        policy_loss = []
        entropy_loss = []

        for log_prob, R, entropy in zip(log_probs, returns, entropies):
            policy_loss.append(-log_prob * R)
            entropy_loss.append(-ENTROPY_BETA * entropy)

        loss = torch.stack(policy_loss).sum() + torch.stack(entropy_loss).sum()

        optimizer.zero_grad()
        loss.backward()
        optimizer.step()

        total_reward = sum(rewards)

        print(f"Episode {episode} | Reward: {total_reward:.2f}")

    # ---------- SAVE MODEL ----------

    torch.save(model.state_dict(), "email_agent.pth")
    print("✅ Model saved as email_agent.pth")

    await env.__aexit__(None, None, None)


if __name__ == "__main__":
    asyncio.run(train())