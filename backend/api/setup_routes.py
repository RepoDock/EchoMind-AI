from fastapi import APIRouter
import shutil
import requests
import subprocess
import threading
import time
router = APIRouter()


@router.get("/check")
def check_setup():

    # Ollama installed?
    if shutil.which("ollama") is None:
        return {
            "status": "not_installed",
            "message": "AI Engine is not installed."
        }

    # Ollama running?
    try:

        requests.get(
            "http://127.0.0.1:11434",
            timeout=2
        )

    except:

        return {
            "status": "not_running",
            "message": "AI Engine is not running."
        }

    # Model installed?
    try:

        response = requests.get(
            "http://127.0.0.1:11434/api/tags",
            timeout=3
        )

        models = response.json()["models"]

        installed = any(
            m["name"].startswith("qwen2.5:7b")
            for m in models
        )

        if not installed:

            return {
                "status": "model_missing",
                "message": "AI Model is missing."
            }

    except:

        return {
            "status": "unknown"
        }

    return {
        "status": "ready"
    }
@router.post("/download-model")
def download_model():

    def worker():
        subprocess.run([
            "ollama",
            "pull",
            "qwen2.5:7b"
        ])

    threading.Thread(
        target=worker,
        daemon=True
    ).start()

    return {
        "status": "started"
    }


@router.get("/model-status")
def model_status():

    response = requests.get(
        "http://127.0.0.1:11434/api/tags"
    )

    models = response.json()["models"]

    installed = any(
        m["name"].startswith("qwen2.5:7b")
        for m in models
    )

    return {
        "installed": installed
    }
import os

@router.post("/install-engine")
def install_engine():

    installer = os.path.join(
        os.path.dirname(__file__),
        "..",
        "resources",
        "OllamaSetup.exe"
    )

    installer = os.path.abspath(installer)

    if not os.path.exists(installer):
        return {
            "success": False,
            "message": "Ollama installer not found."
        }

    def worker():

        # Install Ollama
        process = subprocess.Popen([installer])
        process.wait()

        # Wait until Ollama API starts
        while True:

            try:

                requests.get(
                    "http://127.0.0.1:11434",
                    timeout=2
                )

                break

            except:

                time.sleep(2)

        # Download model
        subprocess.run([
            "ollama",
            "pull",
            "qwen2.5:7b"
        ])

    threading.Thread(
        target=worker,
        daemon=True
    ).start()

    return {
        "success": True,
        "message": "Installation started."
    }
