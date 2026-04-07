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

# Email Triage OpenEnv

## Overview
A real-world email management simulation where an AI agent classifies, prioritizes, and responds to emails.

## Tasks
- Easy → Spam detection
- Medium → Priority classification
- Hard → Response generation

## Reward Design
- Partial rewards for close predictions
- Penalizes incorrect classification
- Encourages semantic correctness in replies

## Action Space
- classify
- prioritize
- reply

## Observation
- email_text
- subject
- sender

## Run Locally
pip install -r requirements.txt  
uvicorn server.app:app  

## Inference
python inference.py  

## Deployment
openenv push --repo-id <username>/email-triage-env