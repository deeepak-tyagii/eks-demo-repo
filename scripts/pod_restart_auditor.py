#!/usr/bin/env python3

import logging
from kubernetes import client, config
from datetime import datetime

# Configure logging
logging.basicConfig(
    filename="restart_report.log",
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)

# Load Kubernetes config
try:
    config.load_kube_config()
except:
    config.load_incluster_config()

core_api = client.CoreV1Api()

RESTART_THRESHOLD = 3  # alert if restarts > threshold

def audit_pods():
    logging.info("Starting Kubernetes Pod Restart Audit...")
    pods = core_api.list_pod_for_all_namespaces(watch=False)

    flagged = []

    for pod in pods.items:
        pod_name = pod.metadata.name
        namespace = pod.metadata.namespace
        for container in pod.status.container_statuses or []:
            restarts = container.restart_count
            cname = container.name

            if restarts > RESTART_THRESHOLD:
                log_line = f"[ALERT] {namespace}/{pod_name} [{cname}] restarted {restarts} times"
                logging.warning(log_line)
                flagged.append({
                    "namespace": namespace,
                    "pod": pod_name,
                    "container": cname,
                    "restarts": restarts
                })
            else:
                logging.info(f"{namespace}/{pod_name} [{cname}] is healthy")

    return flagged

def send_report(flagged):
    if not flagged:
        logging.info("No issues found. No report sent.")
        return

    print("Restart Report:")
    for entry in flagged:
        print(f" - {entry['namespace']}/{entry['pod']} [{entry['container']}]: {entry['restarts']} restarts")

if __name__ == "__main__":
    flagged_pods = audit_pods()
    send_report(flagged_pods)

