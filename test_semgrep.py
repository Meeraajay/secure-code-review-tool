
from app.services.scanner_service import run_semgrep

repository_path = "cloned_repositories/requests"

try:
    result = run_semgrep(repository_path)

    print("Semgrep scan completed!")
    print("Report saved at:", result)

except Exception as error:
    print("Semgrep scan failed:", error)
