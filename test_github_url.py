
from app.services.git_service import validate_github_url

test_urls = [
    "https://github.com/psf/requests",
    "https://github.com/psf/requests.git",
    "https://example.com/project",
    "https://github.com/psf"
]

for url in test_urls:
    print(url, "->", validate_github_url(url))
