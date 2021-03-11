import os
import requests
from pip_check_reqs import find_extra_reqs, common

from .helpers import create_dir_tree, requirements_file_exist, clean_up_repo, clone_repo


class Options(object):
    """Options objects for pip_check_reqs.
    """
    @classmethod
    def fromdict(cls, d):
        df = {k : v for k, v in d.items()}
        return cls(**df)

    def __init__(self, paths, ignore_files, ignore_reqs, ignore_mods, skip_incompatible):
        self.paths = paths
        self.ignore_files = common.ignorer(ignore_files)
        self.ignore_reqs = common.ignorer(ignore_reqs)
        self.ignore_mods = common.ignorer(ignore_mods)
        self.skip_incompatible = skip_incompatible


def repo_fetch(created="2018-01-01", limit=10, language="python"):
    """Call GitHub repo search api with custom parameters.
    """
    created_param = f'created:">{created}"'
    url = f"https://api.github.com/search/repositories?q={created_param}language:{language}&sort=stars&order=desc&per_page={limit}"
    results = requests.get(url).json()
    return results


def python_check_repo_reqs(requirements_file, **kwargs):
    """Check Python repo extra requirements.

    Args:
        requirements_file: String containing the requirements.txt local path.
        paths: List of paths to be used in the requirements scan.
        ignore_files: List of ignored files to be used in the requirements scan.
        ignore_reqs: List of ignored paths to be used in the requirements scan.
        ignore_mods: List of mods to be used in the requirements scan.
        skip_incompatible: Boolean to skip or not incompatible modules.

    Returns:
        Dictionary containing collected scan outputs.
    """
    options = {
        'paths': kwargs.get('paths', []),
        'ignore_files': kwargs.get('ignore_files', []),
        'ignore_reqs': kwargs.get('ignore_reqs', []),
        'ignore_mods': kwargs.get('ignore_mods', []),
        'skip_incompatible': kwargs.get('ignore_mods', False),
    }

    options = Options.fromdict(options)

    return find_extra_reqs.find_extra_reqs(options, requirements_file)


def python_repo_run(repo_path: str) -> dict:
    """Run scans for Python specific repo.

    Args:
        repo_path: String containing the repo local path.

    Returns:
        Dictionary containing collected scan outputs.
    """
    ret = {
        'req': {
            'message': "",
            'extras': None
        }
    }
    requirements_file_path = f"{repo_path}/requirements.txt"
    if requirements_file_exist(requirements_file_path):
        ret['req']['extras'] = python_check_repo_reqs(requirements_file_path, paths=[repo_path])
    else:
        ret['req']['message'] = "Missing requirements.txt file."
    
    return ret


def calc_score(scan_data: dict) -> int:
    """A very naive score generation.

    Args:
        scan_data: A dictionary containing the repo's scan data.

    Returns:
        Integer score.
    """
    total_score = 100
    total_unused = scan_data['req']['extras']

    if total_unused:
        total_unused_num = len(total_unused)
        total_score = total_score - (100 * total_unused_num / 100)
    else:
        total_score = None
    
    return total_score


def run(date_created: str, limit: int, language="python") -> dict:
    """Main run function. Defaulting to python language for repo fetch.

    - Fetch trending list.
    - For each item in the list clone the repo, run scan, clean repo directory.

    Args:
        date_created: String, something like 2021-01-01.
        limit: Integer.
        language: String, python, javascript, golang.

    Returns:
        Dictionary with a breakdown of repos, their scan and score data.
    """
    trending_repos_resp = repo_fetch(created=date_created, limit=limit, language=language)
    resp = {}

    for repo in trending_repos_resp['items']:
        repo_name = repo['name']
        resp[repo_name] = {
            'name': repo_name,
            'owner': repo['owner']['login'],
            'html_url': repo['html_url']
        }
        download_to = f"{os.getcwd()}/repos/"
        repo_path = f"{download_to}/{repo_name}"
        create_dir_tree(download_to)
        clone_repo(repo['git_url'], download_to)

        if language == "python":
            scan_data = python_repo_run(repo_path)
        else:
            scan_data = {
                'req': {
                    'message': f"{language} not yet supported...",
                    'extras': None
                }
            }
        
        resp[repo_name]['scan'] = scan_data
        resp[repo_name]['score'] = calc_score(scan_data)
        clean_up_repo(repo_path)
    
    return resp
