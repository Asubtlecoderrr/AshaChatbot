import os
import glob
user_id = 1

folder_path = f"ashaaiflow/src/ashaaiflow/knowledge/user1/"
file_patterns = ["*.pdf", "*.doc", "*.docx"]
resume_file = None
for pattern in file_patterns:
    files = glob.glob(os.path.join(folder_path, pattern))
    if files:
        resume_file = files[0]  # Take the first match
        break
print(os.getcwd())
print(resume_file)