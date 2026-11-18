
from urllib.parse import urlparse
import subprocess
from pathlib import Path
from urllib.parse import urlparse

def validate_github_url(repository_url: str) -> bool:
    parsed_url = urlparse(repository_url)

    if parsed_url.scheme != "https":
        return False

    if parsed_url.netloc.lower() != "github.com":
        return False

    path_parts = parsed_url.path.strip("/").split("/")

    if len(path_parts) != 2:
        return False

    username, repository = path_parts

    if not username or not repository:
        return False

    if repository.endswith(".git"):
        repository = repository[:-4]

    if not repository:
        return False

    return True

def clone_repository(repository_url: str) -> str:
    repository_name = Path(urlparse(repository_url).path).name

    if repository_name.endswith(".git"):
        repository_name = repository_name[:-4]

    clone_path = Path("cloned_repositories") / repository_name

    if clone_path.exists():
        if (clone_path / ".git").exists():
            return str(clone_path)

        raise FileExistsError("A folder with this repository name already exists")

    clone_path.parent.mkdir(parents=True, exist_ok=True)

    try:
        subprocess.run(
            ["git", "clone", "--depth", "1", repository_url, str(clone_path)],
            check=True,
            capture_output=True,
            text=True,
            timeout=120
        )

    except subprocess.CalledProcessError as error:
        raise RuntimeError("Failed to clone repository") from error

    except subprocess.TimeoutExpired as error:
        raise RuntimeError("Repository cloning timed out") from error

    return str(clone_path)



def find_python_files(repository_path: str) -> list[str]:
    repo_path = Path(repository_path)

    python_files = list(repo_path.rglob("*.py"))

    return [str(file) for file in python_files]


