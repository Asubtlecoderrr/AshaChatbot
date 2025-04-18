# from crewai.tools import BaseTool
from typing import Type
# from pydantic import BaseModel, Field
import requests

class HerKeyJobAPITool():
    name: str = "herkey_job_api"
    description: str = (
       "Fetch job listings from HerKeys internal API."
    )

    def _run(self, filters: dict):
        url = "https://api-prod.herkey.com/api/v1/herkey/jobs/es_candidate_jobs"

        headers = {
            "Accept": "application/json, text/plain, */*",
            "Authorization": "Token eyJhbGciOiJSUzUxMiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl9rZXkiOiJjNjc5MjBiNjA3MzVmYmRkOGI4ODM3ZGQxOTBhZWUzYmRhZWU4ZTE1OTYxYTg1MWMxNjNmYzI1M2M1ZGY0MTFlIiwicGF0aCI6ImxvZ2luX3VzZXJfdG9rZW5fYnVja2V0L2M2NzkyMGI2MDczNWZiZGQ4Yjg4MzdkZDE5MGFlZTNiZGFlZThlMTU5NjFhODUxYzE2M2ZjMjUzYzVkZjQxMWUiLCJleHBpcnkiOjE3NzYzMTk0NTQsInR5cGUiOiIyZiIsImlhdCI6MTc0NDc4MzQ1NCwidXNlciI6eyJ1c2VyX2lkIjo1MTYxMDY1LCJ1c2VybmFtZSI6IlZpZGhpIERvc2hpIiwicHJvZmlsZV9pbWFnZSI6IiJ9fQ.qMVtkq-LJJyWoghBP5TmHgXChK8mCcyuG_A-Xj75GZqq7CtEIWEV7svGiB4m7EkftdI5OQ8h4gmARZ1d8o-ZrgPpGV_oenEJTL7y7mSMrc3Z0BadS3CAWElOftGw4BKZuwtUTtFyTab9ymj5RrOZlG9AcWvDNnatHkt6iFYt6_erQkBo0OGVkY9SVn0hKsQepAMrSM8AJXKgoPG3sRHrVzOCVhRfDYxvz7fWzRt-7XcJlE4RLbBvunL4D-G_YaoVfM0MhiIbEv2GooNwBXNpicVdqY2IjiDHmVy_nwnvfOy-z8b7x2cz-cfybNbriZdzrQ9opkjfdGzCbRnnBJ7TGA", 
            "Referer": "https://www.herkey.com/",
            "Origin": "https://www.herkey.com",
        }
        
        params = {
            "page_no": 1,
            "page_size": 100,
            "job_skills": filters.get("skills", ""),
            "is_global_query": "false",
        }

        if "location" in filters:
            params["location_name"] = filters["location"]
        
        resp = requests.get(
            url=url,
            params=params,
            headers=headers,
            timeout=10
        )
        payload = resp.json()
        data = payload.get("body", [])        
        return "\n\n".join(
          f"{j['title']} at {j['company_name']} ({j['location_name']})\n{j['work_mode']}"
          for j in data
        )

class HerKeyLearningAPITool():
    name: str = "herkey_learning_api"
    description: str = "Fetch upcoming featured learning sessions from HerKey."

    def _run(self):
        url = "https://api-prod.herkey.com/api/v1/herkey/sessions/get-discussion"
        headers = {
            "Accept": "application/json, text/plain, */*",
            "Authorization": "Token eyJhbGciOiJSUzUxMiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl9rZXkiOiJjNjc5MjBiNjA3MzVmYmRkOGI4ODM3ZGQxOTBhZWUzYmRhZWU4ZTE1OTYxYTg1MWMxNjNmYzI1M2M1ZGY0MTFlIiwicGF0aCI6ImxvZ2luX3VzZXJfdG9rZW5fYnVja2V0L2M2NzkyMGI2MDczNWZiZGQ4Yjg4MzdkZDE5MGFlZTNiZGFlZThlMTU5NjFhODUxYzE2M2ZjMjUzYzVkZjQxMWUiLCJleHBpcnkiOjE3NzYzMTk0NTQsInR5cGUiOiIyZiIsImlhdCI6MTc0NDc4MzQ1NCwidXNlciI6eyJ1c2VyX2lkIjo1MTYxMDY1LCJ1c2VybmFtZSI6IlZpZGhpIERvc2hpIiwicHJvZmlsZV9pbWFnZSI6IiJ9fQ.qMVtkq-LJJyWoghBP5TmHgXChK8mCcyuG_A-Xj75GZqq7CtEIWEV7svGiB4m7EkftdI5OQ8h4gmARZ1d8o-ZrgPpGV_oenEJTL7y7mSMrc3Z0BadS3CAWElOftGw4BKZuwtUTtFyTab9ymj5RrOZlG9AcWvDNnatHkt6iFYt6_erQkBo0OGVkY9SVn0hKsQepAMrSM8AJXKgoPG3sRHrVzOCVhRfDYxvz7fWzRt-7XcJlE4RLbBvunL4D-G_YaoVfM0MhiIbEv2GooNwBXNpicVdqY2IjiDHmVy_nwnvfOy-z8b7x2cz-cfybNbriZdzrQ9opkjfdGzCbRnnBJ7TGA", 
            "Referer": "https://www.herkey.com/",
            "Origin": "https://www.herkey.com",
        }
        params = {
            "isHomePage": "false",
            "page": 1,
            "expiry": "false",
            "session_type": "upcoming_featured"
        }

        resp = requests.get(url, params=params, headers=headers, timeout=10)
        if resp.status_code != 200:
            return f"Failed to fetch sessions. Status code: {resp.status_code}"

        payload = resp.json()
        sessions = payload.get("body", [])
        
        if not sessions:
            return "No learning sessions found."

        return "\n\n".join(
            f" Headline: {s['headline']['headline1']} Topic: {s['post_content']['post_topic_text']}"
            for s in sessions
        )

tool=HerKeyLearningAPITool()
print(tool._run())

