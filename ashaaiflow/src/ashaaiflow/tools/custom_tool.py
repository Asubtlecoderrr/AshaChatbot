from crewai.tools import BaseTool
from typing import Type ,Dict, Optional
from pydantic import BaseModel, Field, StrictStr
import json
import requests
import fitz 
import glob
import os
from crewai_tools import (
    FileReadTool,
)
from shared.user_context import user_id_var
from cryptography.fernet import Fernet
from dotenv import load_dotenv
load_dotenv()

fernet_key = os.getenv("FERNET_KEY")
if not fernet_key:
    raise ValueError("FERNET_KEY not found in environment")

cipher = Fernet(fernet_key.encode())

SERPAPI_KEY = os.getenv("SERPAPI_KEY")


class HerkeyJobAPIToolInput(BaseModel):
    skills: str = Field(..., description="Skills of the user")
    location: Optional[str] = Field(None, description="Location of the user")

class HerKeyJobAPITool(BaseTool):
    name: str = "herkey_job_api"
    description: str = (
       "Fetch job listings from HerKeys internal API."
    )
    args_schema: Type[BaseModel] = HerkeyJobAPIToolInput
    
    def _run(self, skills: str, location: str) -> str:

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
            "is_global_query": "false",
        }
        
        if skills:
            skill_lst = skills.split(",")
            print(skill_lst)
            params["job_skills"] = skills
        if location:
            params["location_name"] = location
        
        resp = requests.get(
            url=url,
            params=params,
            headers=headers,
            timeout=10
        )
        payload = resp.json()
        data = payload.get("body", [])        
        return data

class HerKeyLearningAPITool(BaseTool):
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

        return sessions

class JobAPIToolInput(BaseModel):
    keywords: Dict = Field(..., description="Keyword/skill to search for jobs")
    location: Optional[Dict] = Field(None, description="Location to search for jobs")
    experience: Optional[Dict] = Field(None, description="Experience level to search for jobs")

class JobAPITool(BaseTool):
    name: str = "job_api"
    description: str = (
       "Fetch job listings from API."
    )
    args_schema: Type[BaseModel] = JobAPIToolInput
        
    def _run(self, keywords: dict, location: Optional[dict],experience: Optional[dict]) -> list:
        count=10
        days_ago=7
        platform="all"
        all_jobs = []
        keywords = keywords["description"]
        location = location["description"] if location else None
        experience = experience["description"] if experience else None
        try:
            # Base URL for SerpAPI Google Jobs
            url = "https://serpapi.com/search"

            # Prepare query parameters
            if location:
                query = f"{keywords} jobs in {location} with {experience} experience" if experience else f"{keywords} jobs in {location}"
            else:
                query = f"{keywords} jobs in India"
                
            if platform.lower() != "all":
                query += f" {platform}"

            params = {
                "engine": "google_jobs",
                "q": query,
                "api_key": SERPAPI_KEY,
                "hl": "en",
                "chips": f"date_posted:{days_ago}d"
            }

            # Make API request
            response = requests.get(url, params=params, verify=False)
            data = response.json()

            # Process jobs
            job_results = data.get("jobs_results", [])
            for i, job in enumerate(job_results):
                if i >= count:
                    break

                title = job.get("title", "Unknown Title")
                company = job.get("company_name", "Unknown Company")
                location_name = job.get("location", "Unknown Location")
                description = job.get("description", "No description available")
                extensions = job.get("detected_extensions", {})
                job_type = extensions.get("schedule_type", extensions.get("employment_type", "Not specified"))
                date_posted = extensions.get("posted_at", "Recent")
                job_platform = job.get("via", "Unknown")

                # Skip if platform doesn't match
                if platform.lower() != "all" and platform.lower() not in job_platform.lower():
                    continue

                # Extract apply link
                apply_url = (
                    job.get("apply_link", {}).get("link") or
                    (job["apply_options"][0].get("link") if "apply_options" in job and job["apply_options"] else None) or
                    (f"https://www.google.com/search?q={job['job_id']}" if "job_id" in job else None)
                )

                job_entry = {
                    "title": title,
                    "company": company,
                    "location": location_name,
                    "description": description,
                    "url": apply_url,
                    "date_posted": date_posted,
                    "platform": job_platform,
                    "job_type": job_type,
                    "is_real_job": True
                }

                all_jobs.append(job_entry)

        except Exception as e:
            print(f"Error fetching jobs for platform {platform}: {e}")

        if not all_jobs:
            print("SerpAPI search returned no results. Consider adding fallback logic.")

        return all_jobs


class YTLearningToolSchema(BaseModel):
    
    cohort : Dict = Field(..., description="cohort of the user")
    keyword: Dict = Field(..., description="keyword/skills to search for courses")

class YTLearningTool(BaseTool):
    name: str = "youtube courses"
    description: str = (
       "Fetch YT courses from API."
    )
    args_schema: Type[BaseModel] = YTLearningToolSchema
        
    def _run(self, cohort: dict, keyword: dict) -> list:

        LEVEL_KEYWORDS = {
            "beginner": ["introduction", "for beginners", "basics", "zero to hero"],
            "intermediate": ["hands-on", "real world", "intermediate"],
            "advanced": ["advanced", "deep dive", "expert level"]
        }
        
        cohort = cohort["description"]
        keyword = keyword["description"]
        count=5
        if cohort=="Riser":
            level = ["intermediate","advanced"]
        elif cohort=="Starter":
            level = ["beginner"]
        elif cohort=="Restarter":
            level = ["beginner","intermediate"]
        else:
            level = ["beginner","intermediate","advanced"]
            
        for l in level:
            try:
                url = "https://serpapi.com/search"
                level_terms = LEVEL_KEYWORDS.get(l.lower(), [])
                level_query = " OR ".join(level_terms)
                query = f"{keyword} ({level_query})"

                params = {
                    "engine": "youtube",
                    "search_query": query,
                    "api_key": SERPAPI_KEY,
                    "num": count
                }

                response = requests.get(url, params=params, verify=False)
                data = response.json()

                results = []
                for item in data.get("video_results", [])[:count]:
                    results.append({
                        "title": item.get("title", "No title"),
                        "link": item.get("link", ""),
                        "description": item.get("description", ""),
                        "is_course_search_result": True
                    })

                return results

            except Exception as e:
                print(f"SerpAPI YouTube course search error: {e}")
                return []


class ResumeReaderTool(BaseTool):
    name: str = "Resume Reader"
    description: str = (
        "Read resumes from local directory."
    )
        
    def _run(self) -> str:

        user_id = user_id_var.get()
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
            return "No resume file found."
        
        text = ""
        try:
            with fitz.open(resume_file) as doc:
                for page_num in range(len(doc)):
                    page = doc.load_page(page_num)
                    text += page.get_text()
        except Exception as e:
            return f"Error reading resume: {str(e)}"

        return text


class ContextReaderTool(BaseTool):
    name: str = "User Context Reader"
    description: str = """Reads the context.txt file for the current user query to extract conversation history and preferences and follow the flow of conversation"""

    def _run(self) -> str:
        user_id = user_id_var.get()
        
        file_path = f"ashaaiflow/src/ashaaiflow/knowledge/{user_id}"
        file_patterns = ["*.txt"]
        txt_file = None

        for pattern in file_patterns:
            files = glob.glob(os.path.join(file_path, pattern))
            if files:
                txt_file = files[0] 
                break
            
        if not txt_file:
            return "No context file found."

        try:
            decrypted_lines = []
            with open(txt_file, "r") as file:
                for line in file:
                    decrypted_line = cipher.decrypt(line.strip().encode()).decode()
                    decrypted_lines.append(decrypted_line)
            return "\n".join(decrypted_lines)

        except FileNotFoundError:
            return "No context file found for this user."
        except Exception as e:
            return f"Error reading or decrypting context file: {str(e)}"
        
class CommunitySearchToolInput(BaseModel):
    keyword: StrictStr = Field(..., description="Keyword to search for communities")

class CommunitySearchTool(BaseTool):
    name: str = "Community Search"
    description: str = (
        "Search for communities related to a specific keyword."
    )
    args_schema: Type[BaseModel] = CommunitySearchToolInput
    
    def _run(self, keyword: str) -> str:
        url = "https://serpapi.com/search"

        # Search query to find online communities (forums, groups, etc.)
        search_query = f"{keyword} community OR forum OR group"
        if type(keyword) == dict:
            keyword = keyword["description"]
            
        params = {
            "engine": "google",
            "q": search_query,
            "api_key": SERPAPI_KEY,
            "num": 10,
        }

        response = requests.get(url, params=params, verify=False)
        data = response.json()

        # Define community platforms to filter
        community_platforms = ['linkedin.com', 'facebook.com', 'slack.com', 'telegram.org', 'discord.com', 'reddit.com']

        results = []
        for item in data.get("organic_results", [])[:10]:
            # Filter results that match community platforms
            link = item.get("link", "")
            if any(platform in link for platform in community_platforms):
                community = {
                    "title": item.get("title", "No title"),
                    "description": item.get("snippet", ""),
                    "link": link,
                    "is_community_search_result": True
                }
                results.append(community)

        return results
    
class skillsLocationResponse(BaseModel):
    skills: str = Field(description="Skills of the user")
    location: float = Field(description="location of the user")
