from setup.config import DOCS_PATH, LOGS_PATH, Logs

DOCS_PATH_APPROVALS = f"{DOCS_PATH}/approvals"

LOGS_PATH = f"{LOGS_PATH}/approvals.log"

SOURCE_PATH = "src.approvals"

Logs.add_logs(SOURCE_PATH, LOGS_PATH)
