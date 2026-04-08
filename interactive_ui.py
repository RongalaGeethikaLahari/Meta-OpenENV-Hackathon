import gradio as gr
import asyncio
import matplotlib.pyplot as plt

from client import EmailEnvClient
from core.models import EmailAction

import ssl
import certifi

ssl._create_default_https_context = ssl._create_unverified_context

def decide(email):
    email = email.lower()

    if "free" in email or "win" in email:
        return "spam"
    if "deadline" in email or "asap" in email:
        return "urgent"
    return "important"


async def run_episode(task):
    env = EmailEnvClient(base_url="https://adamk29-meta-openenv-hackathon.hf.space")
    await env.__aenter__()

    rewards = []
    logs = []

    try:
        result = await env.reset(task=task)

        step = 0

        while True:
            step += 1

            email = result.observation.email_text
            action = decide(email)

            result = await env.step(
                EmailAction(action_type="classify", content=action)
            )

            reward = result.reward or 0.0
            done = result.done

            rewards.append(reward)

            logs.append(
                f"""
[STEP {step}]
State (Email): {email}
Action: {action}
Reward: {reward:.2f}
Cumulative Reward: {sum(rewards):.2f}
"""
            )

            if done:
                break

        # Plot reward curve
        fig = plt.figure()
        plt.plot(rewards)
        plt.title("Reward Over Episode")

        score = sum(rewards)

        return "\n".join(logs), score, fig

    finally:
        await env.__aexit__(None, None, None)


def run(task):
    return asyncio.run(run_episode(task))


with gr.Blocks() as demo:
    gr.Markdown("# 🤖 RL Email Triage Environment")
    gr.Markdown("Trajectory-based RL interaction")

    task = gr.Dropdown(["easy", "medium", "hard"], value="easy")

    run_btn = gr.Button("▶ Run Episode")

    logs = gr.Textbox(lines=25, label="Trajectory Logs")
    score = gr.Number(label="Total Reward")
    graph = gr.Plot(label="Reward Curve")

    run_btn.click(run, inputs=task, outputs=[logs, score, graph])

demo.launch()