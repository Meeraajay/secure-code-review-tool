
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
