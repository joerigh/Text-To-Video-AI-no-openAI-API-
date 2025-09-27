import os
from datetime import datetime
import json

# Log types
LOG_TYPE_SCRIPT = "SCRIPT"
LOG_TYPE_PEXEL = "PEXEL"

# Log directory paths
DIRECTORY_LOG_SCRIPT = ".logs/script_logs"
DIRECTORY_LOG_PEXEL = ".logs/pexel_logs"

def log_response(log_type, query, response):
    log_entry = {
        "query": query,
        "response": response,
        "timestamp": datetime.now().isoformat()
    }

    if log_type == LOG_TYPE_SCRIPT:
        if not os.path.exists(DIRECTORY_LOG_SCRIPT):
            os.makedirs(DIRECTORY_LOG_SCRIPT)
        filename = '{}_script.txt'.format(datetime.now().strftime("%Y%m%d_%H%M%S"))
        filepath = os.path.join(DIRECTORY_LOG_SCRIPT, filename)
        with open(filepath, "w") as f:
            f.write(json.dumps(log_entry) + '\n')

    if log_type == LOG_TYPE_PEXEL:
        if not os.path.exists(DIRECTORY_LOG_PEXEL):
            os.makedirs(DIRECTORY_LOG_PEXEL)
        filename = '{}_pexel.txt'.format(datetime.now().strftime("%Y%m%d_%H%M%S"))
        filepath = os.path.join(DIRECTORY_LOG_PEXEL, filename)
        with open(filepath, "w") as f:
            f.write(json.dumps(log_entry) + '\n')