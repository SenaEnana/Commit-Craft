import sys
from backend.date_utils import get_custom_date_env
from backend.git_utils import execute_commit

TYPES = {
    "1": ("feat", "A new feature for the user"),
    "2": ("fix", "A bug fix"),
    "3": ("docs", "Documentation only changes"),
    "4": ("refactor", "Code change that neither fixes a bug nor adds a feature"),
    "5": ("chore", "Maintenance tasks, builds, or package updates")
}

def main():
    print("🚀 Commit Craft v4 - Modular Semantic Versioning & Time-Travel Assistant\n")
    
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
   
    commit_env = get_custom_date_env()

    header = f"{commit_type}{scope_str}{breaking_mark}: {message}"
    full_payload = f"{header}\n\n{body}" if body else header
    
    print(f"\n📦 Generated Commit:\n{'-'*40}\n{full_payload}\n{'-'*40}\n")
 
    confirm = input("Execute 'git add .' and commit? (y/n): ").strip().lower()
    if confirm == 'y':
        execute_commit(full_payload, commit_env)
    else:
        print("⚠️ Commit cancelled.")

if __name__ == "__main__":
    main()