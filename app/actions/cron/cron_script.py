import time
import os
import requests



CRON_TOKEN = os.environ.get("CRON_TOKEN")

for _ in range(6):
    print(f'CRON_TOKEN: {CRON_TOKEN}')
    requests.get(url="http://127.0.0.1/blue/cron/rewards/send", headers={"Authorization": f"Bearer {CRON_TOKEN}", "User-Agent": "milestones-cron-send-rewards"})
    time.sleep(10)
