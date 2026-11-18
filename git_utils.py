import subprocess

def get_current_branch():
    """Detects and returns the active git branch name."""
    try:
        res = subprocess.run(["git", "branch", "--show-current"], capture_output=True, text=True, check=True)
        return res.stdout.strip()
    except subprocess.CalledProcessError:
        return "main"

def execute_commit(full_payload, commit_env):
    """Stages files, creates the commit with custom environment variables, and pushes if confirmed."""
    try:
        subprocess.run(["git", "add", "."], check=True)
        subprocess.run(["git", "commit", "-m", full_payload], env=commit_env, check=True)
        print("✅ Successfully staged and committed changes!")
        
        branch = get_current_branch()
        push_confirm = input(f"Push directly to 'origin {branch}'? (y/n): ").strip().lower()
        if push_confirm == 'y':
            subprocess.run(["git", "push", "origin", branch], check=True)
            print(f"🚀 Pushed to origin/{branch}!")
    except subprocess.CalledProcessError as e:
        print(f"❌ Git command failed: {e}")