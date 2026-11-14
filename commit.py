import os
import subprocess
import sys
from datetime import datetime

TYPES = {
    "1": ("feat", "A new feature for the user"),
    "2": ("fix", "A bug fix"),
    "3": ("docs", "Documentation only changes"),
    "4": ("refactor", "Code change that neither fixes a bug nor adds a feature"),
    "5": ("chore", "Maintenance tasks, builds, or package updates")
}

def get_current_branch():
    try:
        res = subprocess.run(["git", "branch", "--show-current"], capture_output=True, text=True, check=True)
        return res.stdout.strip()
    except subprocess.CalledProcessError:
        return "main"

def get_custom_date_env():
    """Prompts for an optional custom commit date and returns updated environment variables."""
    env = os.environ.copy()
    use_custom = input("Set a custom commit date (backdate/future)? (y/n) [default: n]: ").strip().lower()
    
    if use_custom == 'y':
        print("Enter date in 'YYYY-MM-DD HH:MM:SS' or 'YYYY-MM-DD' format (e.g., 2026-11-15 14:30:00):")
        date_str = input("Custom date: ").strip()
        
        try:
            if len(date_str) == 10:
                dt = datetime.strptime(date_str, "%Y-%m-%d")
                # Default to current time of day if only date is provided
                now = datetime.now()
                dt = dt.replace(hour=now.hour, minute=now.minute, second=now.second)
            else:
                dt = datetime.strptime(date_str, "%Y-%m-%d %H:%M:%S")
                
            formatted_date = dt.strftime("%Y-%m-%dT%H:%M:%S")
            env["GIT_AUTHOR_DATE"] = formatted_date
            env["GIT_COMMITTER_DATE"] = formatted_date
            print(f"🕒 Commit timestamp set to: {formatted_date}")
        except ValueError:
            print("❌ Invalid date format. Aborting to prevent bad timestamp.")
            sys.exit(1)
            
    return env

def main():
    print("🚀 Commit Craft v3 - Semantic Versioning & Time-Travel Assistant\n")
    
    # 1. Select commit type
    print("Select commit type:")
    for key, (t, desc) in TYPES.items():
        print(f"  [{key}] {t:8} - {desc}")
        
    choice = input("\nEnter choice (1-5): ").strip()
    if choice not in TYPES:
        print("❌ Invalid choice. Aborting.")
        sys.exit(1)
        
    commit_type = TYPES[choice][0]
    
    # 2. Optional scope & breaking change flag
    scope = input("Enter scope (optional, e.g., cli, ui, core) [Enter to skip]: ").strip()
    scope_str = f"({scope})" if scope else ""
    
    is_breaking = input("Is this a BREAKING CHANGE? (y/n) [default: n]: ").strip().lower() == 'y'
    breaking_mark = "!" if is_breaking else ""
    
    # 3. Short description & optional body
    message = input("Enter short commit description: ").strip()
    if not message:
        print("❌ Commit message cannot be empty. Aborting.")
        sys.exit(1)
        
    body = input("Enter detailed body description (optional) [Enter to skip]: ").strip()
    
    # 4. Custom Date (Backdate / Future)
    commit_env = get_custom_date_env()
    
    # Construct header and full commit payload
    header = f"{commit_type}{scope_str}{breaking_mark}: {message}"
    full_payload = f"{header}\n\n{body}" if body else header
    
    print(f"\n📦 Generated Commit:\n{'-'*40}\n{full_payload}\n{'-'*40}\n")
    
    # 5. Stage, Commit & Optional Push
    confirm = input("Execute 'git add .' and commit? (y/n): ").strip().lower()
    if confirm == 'y':
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
    else:
        print("⚠️ Commit cancelled.")

if __name__ == "__main__":
    main()