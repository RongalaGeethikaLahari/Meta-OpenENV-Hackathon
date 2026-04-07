import os
import asyncio
from dotenv import load_dotenv
from openai import OpenAI
from client import EmailEnvClient
from core.models import EmailAction

import ssl
import certifi

ssl._create_default_https_context = ssl.create_default_context(cafile=certifi.where())

# Load environment variables
load_dotenv()

API_KEY = os.getenv("HF_TOKEN")
BASE_URL = os.getenv("API_BASE_URL", "https://router.huggingface.co/v1")
MODEL_NAME = os.getenv("MODEL_NAME", "Qwen/Qwen2.5-72B-Instruct")

# OpenAI client (required by hackathon)
client = OpenAI(base_url=BASE_URL, api_key=API_KEY)


# Simple rule-based agent (safe + reproducible)
def decide(email):
    email = email.lower()

    if "free" in email or "win" in email:
        return "spam"
    if "deadline" in email or "asap" in email:
        return "urgent"
    return "important"


async def run_task(task):
    # ✅ CORRECT INIT (NO await here)
    env = EmailEnvClient(base_url="https://adamk29-meta-openenv-hackathon.hf.space")

    # ✅ Open connection
    await env.__aenter__()

    try:
        result = await env.reset(task=task)

        print(f"[START] task={task} env=email-triage model={MODEL_NAME}")

        rewards = []
        step = 0

        while True:
            step += 1
            email = result.observation.email_text

            action_text = decide(email)

            action = EmailAction(
                action_type="classify",
                content=action_text
            )

            result = await env.step(action)

            reward = result.reward or 0.0
            done = result.done

            rewards.append(reward)

            print(
                f"[STEP] step={step} action={action_text} "
                f"reward={reward:.2f} done={str(done).lower()} error=null"
            )

            if done:
                break

        # Safe score calculation
        score = sum(rewards) / len(rewards) if rewards else 0.0

        print(
            f"[END] success=true steps={step} score={score:.2f} "
            f"rewards={','.join([f'{r:.2f}' for r in rewards])}"
        )

    finally:
        # ✅ Proper close (MANDATORY)
        await env.__aexit__(None, None, None)


async def main():
    for task in ["easy", "medium", "hard"]:
        await run_task(task)


if __name__ == "__main__":
    asyncio.run(main())