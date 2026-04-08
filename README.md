---
title: Email Triage OpenEnv
emoji: 📧
colorFrom: blue
colorTo: green
sdk: docker
sdk_version: "1.0"
app_file: app.py
pinned: false
---
# 🚀 RL Email Triage Environment (OpenEnv)

An **end-to-end Reinforcement Learning (RL) environment** for intelligent email triage, where agents learn to classify, prioritize, and manage emails sequentially under real-world constraints.

🔗 **Live Environment (Hugging Face Space):**  
https://adamk29-meta-openenv-hackathon.hf.space

---

# 🧠 Problem Statement

Modern email systems require more than classification:

- Emails arrive sequentially
- Some require urgent action
- Delays have consequences
- Mistakes accumulate over time

👉 This project models email handling as a **Sequential Decision Making (RL Problem)**

---

# 🎯 Objective

Train an intelligent agent that can:

- Process incoming emails
- Identify urgent emails correctly
- Clear inbox efficiently
- Maximize long-term reward
- Avoid critical failures

---

# 🏗️ Project Architecture

hackathon/
├── core/                  # Core logic (dataset, reward, models)
├── server/                # OpenEnv server (FastAPI)
├── data/                  # Email dataset
├── scripts/               # Validation scripts
│
├── train_agent.py         # RL training
├── test_agent.py          # Model testing
├── inference.py           # Rule-based baseline
├── interactive_ui.py      # RL visualization UI
├── demo.py                # Full pipeline
│
├── client.py              # Env client
├── Dockerfile
├── pyproject.toml
├── uv.lock
└── README.md

---

# 📊 Environment Design

## 🧩 State (Observation)

Each step returns:

- email_text
- sender
- subject
- history
- message

---

## 🎮 Action Space

spam | important | urgent

---

## 🔄 Environment Dynamics

- Emails arrive sequentially
- Agent acts per step
- Environment transitions
- Episode ends when inbox is cleared or failure occurs

---

# 🧩 Dataset

- Enron-style emails
- File: data/enron_sample.txt

## 🏷️ Labeling Logic

if contains (urgent/asap/deadline) → urgent  
if contains (free/win/offer/$) → spam  
else → important  

---

# 🏆 Reward Design (Core RL)

- Correct classification → +2.0  
- Wrong classification → -0.5  
- Correct urgent handling → +1.5  
- Missed urgent → -1.0  
- Step penalty → -0.01  
- Progress reward → +1/(remaining emails)  
- Stability bonus → +0.2  
- Completion bonus → up to +5  

👉 Designed similar to goal-driven RL environments (like AirSim)

---

# 🤖 RL Training

Policy Gradient (REINFORCE):

- Neural network policy
- Action sampling
- Discounted rewards
- Entropy for exploration

---

## ▶️ Train Agent

python train_agent.py

Model saved as:
email_agent.pth

---

# 🧪 Testing

## ▶️ Test Model

python test_agent.py

Includes:
- Environment evaluation
- Custom samples

---

# ⚡ Inference (Baseline)

python inference.py

---

# 🎨 Interactive UI

python interactive_ui.py

Open:
http://127.0.0.1:7860

Features:
- Trajectory view
- Reward curve
- RL logs

---

# 🔥 Full Demo

python demo.py

✔ Train  
✔ Test  
✔ Launch UI  
✔ Auto open browser  

---

# 🛠️ Setup Guide

## 1. Clone Repo

git clone https://github.com/<your-username>/Meta-OpenENV-Hackathon.git  
cd Meta-OpenENV-Hackathon  

---

## 2. Create Environment

python -m venv env  
source env/bin/activate  

---

## 3. Install Dependencies

pip install -r requirements.txt  

---

## 4. Run Server (optional)

uvicorn server.app:app --port 8000  

---

# 🌐 Hosted Environment

https://adamk29-meta-openenv-hackathon.hf.space

---

# ⚠️ Common Errors & Fixes

## 🔐 SSL Error

Error:
SSL: CERTIFICATE_VERIFY_FAILED  

Fix:

pip install certifi  
export SSL_CERT_FILE=$(python -m certifi)  

OR:

import ssl, certifi  
ssl._create_default_https_context = ssl.create_default_context(cafile=certifi.where())  

---

## 🔌 WebSocket Error

Use EXACT URL:

https://adamk29-meta-openenv-hackathon.hf.space  

Do NOT use:
- http
- trailing /

---

---

# 🐳 Docker (Optional)

docker build -t email-env .  
docker run -p 8000:8000 email-env  

---

# RL

- Sequential decisions ✔  
- Delayed rewards ✔  
- State transitions ✔  
- Exploration ✔  
- Episode termination ✔  

---

# 🚀 Developer Usage

env = EmailEnvClient(base_url="https://adamk29-meta-openenv-hackathon.hf.space")

obs = await env.reset()  
obs = await env.step(action)  

---

# 🏆 Highlights

- Real RL environment  
- OpenEnv compliant  
- Hugging Face deployed  
- Trainable agent  
- Interactive UI  

---

# 📜 License

MIT

---
# Authors
- Koda Adam
- Rongala Geethika Lahari
- Bobbili Revanth
---

# 🔥 Demo Link

```bash 
https://adamk29-meta-openenv-hackathon.hf.space
```

---

🚀 Built for OpenEnv Hackathon