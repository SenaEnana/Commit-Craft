# import json
# from datetime import datetime

# def add_note(content: str, tag: str = "general") -> None:
#     data_file = "notes.json"
#     try:
#         with open(data_file, "r") as f:
#             notes = json.load(f)
#     except (FileNotFoundError, json.JSONDecodeError):
#         notes = []

#     new_entry = {
#         "id": len(notes) + 1,
#         "content": content,
#         "tag": tag,
#         "created_at": datetime.utcnow().isoformat()
#     }
    
#     notes.append(new_entry)
#     with open(data_file, "w") as f:
#         json.dump(notes, f, indent=2)
#     print(f"Added note #{new_entry['id']} under [{tag}]")

# if __name__ == "__main__":
#     add_note("Initial commit: Quick note system initialized!", "meta")