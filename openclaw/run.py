import yaml
import os
from whatsapp_notifier import send_whatsapp_alert

DATA_PATH = "./data/jobs.yaml"
SENT_FILE = "./data/sent_jobs.yaml"

def load_jobs():
    if os.path.exists(DATA_PATH):
        with open(DATA_PATH) as f:
            return yaml.safe_load(f) or []
    return []

def load_sent():
    if os.path.exists(SENT_FILE):
        with open(SENT_FILE) as f:
            return set(yaml.safe_load(f) or [])
    return set()

def save_sent(sent):
    with open(SENT_FILE, "w") as f:
        yaml.safe_dump(list(sent), f)

def main():
    jobs = load_jobs()
    sent = load_sent()

    for job in jobs:
        job_id = job.get("url")

        if job_id and job_id not in sent:
            try:
                send_whatsapp_alert(job)
                print(f"✅ Sent WhatsApp alert for {job_id}")
                sent.add(job_id)
            except Exception as e:
                print(f"❌ Failed: {e}")

    save_sent(sent)

if __name__ == "__main__":
    main()
