import shutil
import git
from os import path
from pathlib import Path


def create_dir_tree(path):
    """Create a directory tree.  Ignoring already created.

    Args:
        path: Directory tree string.
    """
    Path(path).mkdir(parents=True, exist_ok=True)


def requirements_file_exist(file_path):
    """Check if requirements.txt file exists.  Only needed for python based packages.

    Args:
        file_path: Directory to check if the requirements.txt file exits.

    Returns:
        Boolean.
    """
    return path.exists(file_path)


def clean_up_repo(dir_path):
    """Deletes a repo target path.

    Args:
        dit_path: Directory to delete, all files and folders.
    """
    shutil.rmtree(dir_path, ignore_errors=True)


def clone_repo(git_url, repo_dir):
    """Clone the public GitHub repository into a given directory.

    Args:
        git_url: Repo GitHub url.
        repo_dir: Path to clone the repo into.
    """
    git.Git(repo_dir).clone(git_url)
