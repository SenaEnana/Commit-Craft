import subprocess
import sys

# Standard Conventional Commit types
TYPES = {
    "1": ("feat", "A new feature for the user"),
    "2": ("fix", "A bug fix"),
    "3": ("docs", "Documentation only changes"),
    "4": ("refactor", "A code change that neither fixes a bug nor adds a feature"),
    "5": ("chore", "Maintenance tasks, builds, or package updates")
}

def main():
    print("🚀 Commit Craft - Semantic Versioning Assistant\n")
    
    # 1. Select commit type
    print("Select commit type:")
    for key, (t, desc) in TYPES.items():
        print(f"  [{key}] {t:8} - {desc}")
        
    choice = input("\nEnter choice (1-5): ").strip()
    if choice not in TYPES:
        print("❌ Invalid choice. Aborting.")
        sys.exit(1)
        
    commit_type = TYPES[choice][0]
    
    # 2. Optional scope
    scope = input("Enter scope (optional, e.g., auth, ui, cli) [Press Enter to skip]: ").strip()
    scope_str = f"({scope})" if scope else ""
    
    # 3. Commit message
    message = input("Enter short commit description: ").strip()
    if not message:
        print("❌ Commit message cannot be empty. Aborting.")
        sys.exit(1)
        
    # Construct conventional commit string
    full_message = f"{commit_type}{scope_str}: {message}"
    
    print(f"\n📦 Generated Commit Message:\n   {full_message}\n")
    
    # 4. Git execution confirmation
    confirm = input("Execute 'git add .' and commit? (y/n): ").strip().lower()
    if confirm == 'y':
        try:
            subprocess.run(["git", "add", "."], check=True)
            subprocess.run(["git", "commit", "-m", full_message], check=True)
            print("✅ Successfully staged and committed changes!")
        except subprocess.CalledProcessError as e:
            print(f"❌ Git command failed: {e}")
    else:
        print("⚠️ Commit cancelled. Message was not executed.")

if __name__ == "__main__":
    main()