import os
import sys
from datetime import datetime, timedelta

def parse_relative_date(date_str: str) -> datetime:
    """Parses relative offsets (-1d, -2w, +3h) or absolute dates."""
    date_str = date_str.strip().lower()
    now = datetime.now()
    
    if date_str.startswith('-') or date_str.startswith('+'):
        unit = date_str[-1]
        try:
            val = int(date_str[1:-1])
            if unit == 'd':
                delta = timedelta(days=val)
            elif unit == 'w':
                delta = timedelta(weeks=val)
            elif unit == 'h':
                delta = timedelta(hours=val)
            else:
                raise ValueError("Unsupported unit. Use 'd' (days), 'w' (weeks), or 'h' (hours).")
            
            return now - delta if date_str.startswith('-') else now + delta
        except (ValueError, IndexError):
            raise ValueError("Invalid relative format. Use e.g., -1d, -2w, +5h.")

    if len(date_str) == 10:
        dt = datetime.strptime(date_str, "%Y-%m-%d")
        return dt.replace(hour=now.hour, minute=now.minute, second=now.second)
    else:
        return datetime.strptime(date_str, "%Y-%m-%d %H:%M:%S")

def get_custom_date_env():
    """Prompts for custom dates or relative shortcuts and returns updated environment variables."""
    env = os.environ.copy()
    use_custom = input("Set a custom commit date (backdate/future)? (y/n) [default: n]: ").strip().lower()
    
    if use_custom == 'y':
        print("Enter relative shortcut (e.g., -1d for yesterday, -7d) or absolute date ('YYYY-MM-DD'):")
        date_str = input("Date / Offset: ").strip()
        
        try:
            dt = parse_relative_date(date_str)
            formatted_date = dt.strftime("%Y-%m-%dT%H:%M:%S")
            env["GIT_AUTHOR_DATE"] = formatted_date
            env["GIT_COMMITTER_DATE"] = formatted_date
            print(f"🕒 Commit timestamp set to: {formatted_date}")
        except Exception as e:
            print(f"❌ Error parsing date: {e}. Aborting.")
            sys.exit(1)
            
    return env