import subprocess
import sys

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

def main():
    print("🚀 Commit Craft v2 - Semantic Versioning Assistant\n")

    print("Select commit type:")
    for key, (t, desc) in TYPES.items():
        print(f"  [{key}] {t:8} - {desc}")
        
    choice = input("\nEnter choice (1-5): ").strip()
    if choice not in TYPES:
        print("❌ Invalid choice. Aborting.")
        sys.exit(1)
        
    commit_type = TYPES[choice][0]
    
    scope = input("Enter scope (optional, e.g., cli, ui, core) [Enter to skip]: ").strip()
    scope_str = f"({scope})" if scope else ""
    
    is_breaking = input("Is this a BREAKING CHANGE? (y/n) [default: n]: ").strip().lower() == 'y'
    breaking_mark = "!" if is_breaking else ""
    
    message = input("Enter short commit description: ").strip()
    if not message:
        print("❌ Commit message cannot be empty. Aborting.")
        sys.exit(1)
        
    body = input("Enter detailed body description (optional) [Enter to skip]: ").strip()

    header = f"{commit_type}{scope_str}{breaking_mark}: {message}"
    full_payload = f"{header}\n\n{body}" if body else header
    
    print(f"\n📦 Generated Commit:\n{'-'*40}\n{full_payload}\n{'-'*40}\n")

    confirm = input("Execute 'git add .' and commit? (y/n): ").strip().lower()
    if confirm == 'y':
        try:
            subprocess.run(["git", "add", "."], check=True)
            subprocess.run(["git", "commit", "-m", full_payload], check=True)
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