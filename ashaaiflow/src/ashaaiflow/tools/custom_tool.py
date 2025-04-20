from crewai.tools import BaseTool
from typing import Type ,Dict, Optional
from pydantic import BaseModel, Field
import json
import requests
import fitz 
import glob
import os
from crewai_tools import (
    FileReadTool,
)


class HerKeyJobAPIToolInput(BaseModel):
    """Input schema for HerKeyJobAPITool."""

    skills: Optional[str] = Field(
        None, description="Skills to filter job listings."
    )
    location: Optional[str] = Field(
        None, description="Location to filter job listings."
    )
    
class HerKeyJobAPITool(BaseTool):
    name: str = "herkey_job_api"
    description: str = (
       "Fetch job listings from HerKeys internal API."
    )
    args_schema: Type[BaseModel] = HerKeyJobAPIToolInput
    
    def _run(self, skills: Optional[str], location:Optional[str]) -> str:
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
    """Input schema for HerKeyJobAPITool."""

    keywords: Optional[str] = Field(
        None, description="Skills to filter job listings."
    )
    location: Optional[str] = Field(
        None, description="Location to filter job listings."
    )
    platform: Optional[str] = Field(
        None, description="job platforms to search."
    )
    
class JobAPITool(BaseTool):
    name: str = "job_api"
    description: str = (
       "Fetch job listings from API."
    )
    args_schema: Type[BaseModel] = JobAPIToolInput
        
    def _run(self, keywords: Optional[str], location:Optional[str], platform: str) -> list:
        SERAPH_KEY = "3237d985f10df42f6e578b99a5966ff84131358dae814931afd18373384e28a9"  # Your Seraph API key for integrati
        count=10
        days_ago=7
        all_jobs = []

        try:
            # Base URL for SerpAPI Google Jobs
            url = "https://serpapi.com/search"

            # Prepare query parameters
            query = f"{keywords} jobs in {location}"
            if platform.lower() != "all":
                query += f" {platform}"

            params = {
                "engine": "google_jobs",
                "q": query,
                "api_key": SERAPH_KEY,
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

class YTLearningInput(BaseModel):
    """Input schema for HerKeyJobAPITool."""

    topic: Optional[str] = Field(
        None, description="Skills to filter job listings."
    )
    cohort: Optional[str] = Field(
        None, description="Cohort to filter job listings."
    )
    
class YTLearningTool(BaseTool):
    name: str = "youtube courses"
    description: str = (
       "Fetch YT courses from API."
    )
    args_schema: Type[BaseModel] = YTLearningInput
        
    def _run(self, topic: str, cohort: str) -> list:
        SERPAPI_KEY = "3237d985f10df42f6e578b99a5966ff84131358dae814931afd18373384e28a9"

        LEVEL_KEYWORDS = {
            "beginner": ["introduction", "for beginners", "basics", "zero to hero"],
            "intermediate": ["hands-on", "real world", "intermediate"],
            "advanced": ["advanced", "deep dive", "expert level"]
        }
        count=5
        if cohort=="Riser":
            level = ["intermediate","advanced"]
        elif cohort=="Starter":
            level = ["beginner"]
        elif cohort=="Restarter":
            level = ["beginner","intermediate"]
            
        for l in level:
            try:
                url = "https://serpapi.com/search"
                level_terms = LEVEL_KEYWORDS.get(l.lower(), [])
                level_query = " OR ".join(level_terms)
                query = f"{topic} ({level_query})"

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

class ResumeReaderInput(BaseModel):
    """Input schema for ResumeReaderTool."""

    user_id: Optional[str] = Field(
        None, description="User ID to fetch resume."
    )

class ResumeReaderTool(BaseTool):
    name: str = "Resume Reader"
    description: str = (
        "Read resumes from local directory."
    )
        
    def _run(self, user_id:str) -> str:
        
        folder_path = f"src/ashaaiflow/knowledge/{user_id}/"
        file_patterns = ["*.pdf", "*.doc", "*.docx"]
        resume_file = None

        for pattern in file_patterns:
            files = glob.glob(os.path.join(folder_path, pattern))
            if files:
                resume_file = files[0]  # Take the first match
                break

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


class contextInput(BaseModel):
    """Input schema for contextModel."""

    user_id: Optional[str] = Field(
        None, description="User ID to fetch context."
    )

class contextTool(BaseTool):
    name: str = "Context Sharing"
    description: str = (
      "Context of conversation between user and AI"
    )
    args_schema: Type[BaseModel] = contextInput
    
    def _run(self, user_id: str) -> str:
        file_path = f'src/ashaaiflow/knowledge/{user_id}/context.txt'
 
        context_tool = FileReadTool(
            file_path=file_path,
            collection_name="context",
            description="This is the context of the user. It contains the user's previous interactions and preferences."
        )
        
        return context_tool

class CommunityInput(BaseModel):
    
    topic: str = Field(
        "women", description="Topic to search for communities about."
    )

class CommunitySearchTool(BaseTool):
    name: str = "Community Search"
    description: str = (
        "Search for communities related to a specific topic."
    )
    args_schema: Type[BaseModel] = CommunityInput
    
    def _run(self, topic: str) -> str:
        SERPAPI_KEY = "3237d985f10df42f6e578b99a5966ff84131358dae814931afd18373384e28a9"
        url = "https://serpapi.com/search"

        # Search query to find online communities (forums, groups, etc.)
        search_query = f"{topic} community OR forum OR group"

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