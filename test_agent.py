import torch
import asyncio

from client import EmailEnvClient
from core.models import EmailAction
from train_agent import PolicyNet, encode_state, ACTIONS


# ---------- LOAD MODEL ----------

model = PolicyNet()
model.load_state_dict(torch.load("email_agent.pth"))
model.eval()


def predict(obs):
    state = encode_state(obs)
    probs = model(state)
    action = ACTIONS[probs.argmax().item()]
    return action


# ---------- TEST 1: ENVIRONMENT ----------

async def test_environment():

    print("\n===== TESTING ON ENVIRONMENT =====\n")

    env = EmailEnvClient(base_url="http://localhost:8000")
    await env.__aenter__()

    try:
        result = await env.reset(task="medium")

        step = 0
        total_reward = 0

        while True:
            step += 1

            email = result.observation.email_text
            action = predict(result.observation)

            result = await env.step(
                EmailAction(action_type="classify", content=action)
            )

            reward = result.reward or 0.0
            total_reward += reward

            print(f"""
STEP {step}
Email: {email}
Predicted: {action}
Reward: {reward:.2f}
--------------------------
""")

            if result.done:
                break

        print(f"\n✅ TOTAL REWARD: {total_reward:.2f}")

    finally:
        await env.__aexit__(None, None, None)


# ---------- TEST 2: CUSTOM EXAMPLES ----------

def test_custom_examples():

    print("\n===== TESTING CUSTOM EMAILS =====\n")

    class DummyObs:
        def __init__(self, text):
            self.email_text = text

    samples = [
        "Win a free iPhone now!!!",
        "Meeting at 5pm today",
        "Fix the server ASAP, urgent issue",
        "Client feedback received, please review",
        "Limited time offer, click now!!!"
    ]

    for text in samples:
        obs = DummyObs(text)
        action = predict(obs)

        print(f"""
Email: {text}
Predicted Label: {action}
--------------------------
""")


# ---------- MAIN ----------

async def main():
    await test_environment()
    test_custom_examples()


if __name__ == "__main__":
    asyncio.run(main())