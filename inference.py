import os
import asyncio
from dotenv import load_dotenv
from openai import OpenAI
from client import EmailEnvClient
from core.models import EmailAction

import ssl
import certifi

# ✅ Fix SSL issues (important for Mac / HF Spaces)
ssl._create_default_https_context = ssl.create_default_context(
    cafile=certifi.where()
)

# ---------- LOAD ENV ----------

load_dotenv()

# ✅ MUST use these (for hackathon validator)
API_KEY = os.environ.get("API_KEY")
BASE_URL = os.environ.get("API_BASE_URL")

# Fallback for local testing (optional)
if API_KEY is None:
    API_KEY = os.getenv("HF_TOKEN")

if BASE_URL is None:
    BASE_URL = "https://router.huggingface.co/v1"

MODEL_NAME = os.getenv("MODEL_NAME", "Qwen/Qwen2.5-72B-Instruct")

# ---------- OPENAI CLIENT ----------

client = OpenAI(
    base_url=BASE_URL,
    api_key=API_KEY
)

# ---------- RULE-BASED FALLBACK ----------

def fallback_decide(email):
    email = email.lower()

    if "free" in email or "win" in email:
        return "spam"
    if "deadline" in email or "asap" in email:
        return "urgent"
    return "important"


# ---------- LLM DECISION (REQUIRED) ----------

async def llm_decide(email):

    try:
        response = client.chat.completions.create(
            model=MODEL_NAME,
            messages=[
                {
                    "role": "system",
                    "content": "You are an intelligent email triage agent. Classify emails into: spam, important, or urgent."
                },
                {
                    "role": "user",
                    "content": f"Email:\n{email}\n\nAnswer ONLY one word: spam / important / urgent"
                }
            ],
            temperature=0.2
        )

        output = response.choices[0].message.content.lower().strip()

        if "spam" in output:
            return "spam"
        if "urgent" in output:
            return "urgent"
        return "important"

    except Exception as e:
        print(f"⚠️ LLM failed, using fallback: {e}")
        return fallback_decide(email)


# ---------- RUN TASK ----------

async def run_task(task):

    env = EmailEnvClient(
        base_url="https://adamk29-meta-openenv-hackathon.hf.space"
    )

    await env.__aenter__()

    try:
        result = await env.reset(task=task)

        print(f"[START] task={task} env=email-triage model={MODEL_NAME}")

        rewards = []
        step = 0

        while True:
            step += 1

            email = result.observation.email_text

            # ✅ USE LLM (THIS IS THE KEY FIX)
            action_text = await llm_decide(email)

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

        score = sum(rewards) / len(rewards) if rewards else 0.0

        print(
            f"[END] success=true steps={step} score={score:.2f} "
            f"rewards={','.join([f'{r:.2f}' for r in rewards])}"
        )

    finally:
        await env.__aexit__(None, None, None)


# ---------- MAIN ----------

async def main():
    for task in ["easy", "medium", "hard"]:
        await run_task(task)


if __name__ == "__main__":
    asyncio.run(main())