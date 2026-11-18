
from app.services.scanner_service import run_all_scanners

repository_path = "cloned_repositories/requests"

try:
    results = run_all_scanners(repository_path)

    print(results["message"])
    print("Repository:", results["repository"])

    print("\nGenerated reports:")

    for scanner, report in results["reports"].items():
        print(scanner, ":", report)

except Exception as error:
    print("Scanning failed:", error)
