import subprocess
import time
import webbrowser
import sys

import ssl
import certifi

ssl._create_default_https_context = ssl._create_unverified_context

# ---------- STEP 1: START SERVER ----------

def start_server():
    print("🚀 Starting OpenEnv server...")

    return subprocess.Popen(
        ["uvicorn", "server.app:app", "--host", "127.0.0.1", "--port", "8000"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )


# ---------- STEP 2: TRAIN MODEL ----------

def train_model():
    print("\n🧠 Training RL Agent...\n")

    process = subprocess.Popen(
        [sys.executable, "train_agent.py"]
    )

    process.wait()
    print("\n✅ Training completed\n")


# ---------- STEP 3: TEST MODEL ----------

def test_model():
    print("\n🧪 Testing trained model...\n")

    process = subprocess.Popen(
        [sys.executable, "test_agent.py"]
    )

    process.wait()
    print("\n✅ Testing completed\n")


# ---------- STEP 4: LAUNCH UI ----------

def launch_ui():
    print("\n🎨 Launching Interactive UI...\n")

    subprocess.Popen(
        [sys.executable, "interactive_ui.py"]
    )


# ---------- MAIN DEMO PIPELINE ----------

def main():

    # 1. Start server
    # server = start_server()

    # Wait for server to boot
    time.sleep(5)

    try:
        # 2. Train model
        train_model()

        # 3. Test model
        test_model()

        # 4. Launch UI
        launch_ui()

        print("\n🔥 DEMO READY!")
        print("👉 Open UI: http://127.0.0.1:7860\n")
        
        time.sleep(60)
        webbrowser.open("http://127.0.0.1:7860")

        # Keep running
        while True:
            time.sleep(1)

    except KeyboardInterrupt:
        print("\n🛑 Stopping demo...")

    finally:
        print("Exited!")
        # server.terminate()


if __name__ == "__main__":
    main()