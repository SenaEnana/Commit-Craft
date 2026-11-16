import os
import subprocess

def is_valid_git_repo(repo_path: str) -> bool:
    """Checks if the provided directory exists and contains a .git folder."""
    return os.path.isdir(repo_path) and os.path.isdir(os.path.join(repo_path, ".git"))

def get_repo_status(repo_path: str) -> list[dict]:
    """Returns a list of modified/untracked files in the target project."""
    if not is_valid_git_repo(repo_path):
        raise ValueError("Invalid Git repository path.")
        
    res = subprocess.run(
        ["git", "status", "--porcelain"],
        cwd=repo_path,
        capture_output=True,
        text=True,
        check=True
    )
    
    files = []
    for line in res.stdout.splitlines():
        if line.strip():
            status = line[:2].strip()
            filepath = line[3:].strip()
            files.append({"status": status, "file": filepath})
    return files

def execute_external_commit(repo_path: str, files: list[str], full_payload: str, commit_env: dict, push: bool = False):
    """Stages selected files and commits them inside the target repository."""
    if not is_valid_git_repo(repo_path):
        raise ValueError("Invalid Git repository path.")

    if files == ["all"]:
        subprocess.run(["git", "add", "."], cwd=repo_path, check=True)
    else:
        subprocess.run(["git", "add"] + files, cwd=repo_path, check=True)
        
    subprocess.run(["git", "commit", "-m", full_payload], cwd=repo_path, env=commit_env, check=True)
    
    if push:
        branch_res = subprocess.run(
            ["git", "branch", "--show-current"],
            cwd=repo_path,
            capture_output=True,
            text=True,
            check=True
        )
        branch = branch_res.stdout.strip()
        subprocess.run(["git", "push", "origin", branch], cwd=repo_path, check=True)