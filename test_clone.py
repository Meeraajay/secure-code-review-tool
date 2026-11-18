
from app.services.git_service import (
    clone_repository,
    find_python_files
)

url = "https://github.com/psf/requests"

try:
    path = clone_repository(url)
except FileExistsError:
    path = "cloned_repositories/requests"

python_files = find_python_files(path)

print("Total Python files found:", len(python_files))

for file in python_files[:10]:
    print(file)
