
from app.services.scanner_service import run_bandit

repository_path = "cloned_repositories/requests"

try:
    result = run_bandit(repository_path)

    print("Bandit scan completed!")
    print("Report saved at:", result)

except Exception as error:
    print("Bandit scan failed:", error)
