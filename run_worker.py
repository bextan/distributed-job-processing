import sys
import subprocess


def run_worker():

    cmd = [
        sys.executable, "-m", "celery",
        "-A", "app.core.celery_app.celery_app",
        "worker",
        "--loglevel=info"
    ]
    
    if sys.platform.startswith("win"):
        print("Detected Windows OS: Using --pool=solo for Windows compatibility.")
        cmd.extend(["--pool=solo"])
        
    try:
        subprocess.run(cmd)
    except KeyboardInterrupt:
        print("\nWorker stopped by user.")


if __name__ == "__main__":
    run_worker()
