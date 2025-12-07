from flask import Flask, request
import requests
import os
import time
import logging
from threading import Thread

app = Flask(__name__)

# Configuration via environment variables
JELLYFIN_URL = os.environ.get("JELLYFIN_URL")
API_KEY = os.environ.get("JELLYFIN_API_KEY")
CLEAN_CACHE_TASK_ID = os.environ.get("CLEAN_CACHE_TASK_ID")
ANALYZE_TASK_ID = os.environ.get("ANALYZE_TASK_ID")
DELAY_SECONDS = int(os.environ.get("DELAY_SECONDS", 300))  # Fallback to 5 minutes
# Setting up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
# Printing basic data
logging.info(f"Jellyfin URL: {JELLYFIN_URL}")
logging.info(f"Jellyfin API set: {bool(API_KEY)}")
logging.info(f"CLEAN_CACHE_TASK_ID: {CLEAN_CACHE_TASK_ID}")
logging.info(f"ANALYZE_SEGMENTS_TASK_ID: {ANALYZE_TASK_ID}")
# Defining the functions
def trigger_task(task_id):
    url = f"{JELLYFIN_URL}/ScheduledTasks/Running/{task_id}?api_key={API_KEY}"
    try:
        resp = requests.post(url, timeout=10, verigy=False)
        if resp.status_code in [200, 204]:
            logging.info(f"Task {task_id} triggered successfully")
        else:
            logging.info(f"Failed to trigger task {task_id}: {resp.status_code} {resp.text}")
    except Exception as e:
        logging.info(f"Error triggering task {task_id}: {e}")

def run_intro_skipper_sequence():
    # Step 1: Trigger Clean Cache immediately
    logging.info("Triggering Intro Skipper Clean Cache task")
    trigger_task(CLEAN_CACHE_TASK_ID)

    logging.info(f"Waiting {DELAY_SECONDS} seconds before running Detect & Analyze Media Segments task")
    # Step 2: Wait for a short delay (library scan should finish)
    time.sleep(DELAY_SECONDS)

    # Step 3: Trigger Detect & Analyze Media Segments
    logging.info("Triggering Detect & Analyze Media Segments task")
    trigger_task(ANALYZE_TASK_ID)

@app.route("/trigger", methods=["POST"])
def trigger():
    # Run the Intro Skipper sequence in a background thread
    logging.info("Webhook received from Sonarr/Radarr")
    Thread(target=run_intro_skipper_sequence).start()
    # Respond immediately
    return "Intro Skipper sequence triggered", 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
