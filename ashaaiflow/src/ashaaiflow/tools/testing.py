import os
import glob

user_id =1
file_path = f"ashaaiflow/src/ashaaiflow/knowledge/{user_id}"
file_patterns = ["*.txt"]
txt_file = None

for pattern in file_patterns:
    files = glob.glob(os.path.join(file_path, pattern))
    if files:
        txt_file = files[0] 
        break
    
if not txt_file:
    print("No context file found.")
else:
    print(txt_file)

file_path = f'ashaaiflow/src/ashaaiflow/knowledge/{user_id}/'        
file_patterns = ["*.pdf", "*.doc", "*.docx"]
resume_file = None

for pattern in file_patterns:
    files = glob.glob(os.path.join(file_path, pattern))
    if files:
        resume_file = files[0]  # Take the first match
        break
# resume_file = "ashaaiflow/src/ashaaiflow/knowledge/1/Vidhi Resume.pdf"
if not resume_file:
    print("No resume file found.")
else:
    print(resume_file)