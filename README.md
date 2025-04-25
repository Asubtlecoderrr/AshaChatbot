# **🚀 Asha AI Bot – Deployment Guide**  

This guide will help you set up and deploy the Asha AI chatbot (FastAPI backend + React frontend) on a Google Cloud VM instance using Docker.

## 📦 Local Development   
### ✅ Frontend
 
`cd frontend/my-app` <br>
`npm install` <br>
`npm run start`  
### ✅ Backend

`pip install -r requirements.txt` <br>
`uvicorn backend.main:app`

## ☁️ GCP VM Deployment Using Docker  

### ✅ Step 1: SSH into Your VM
Use the Google Cloud Console or gcloud CLI to SSH into your VM instance.

### ✅ Step 2: Navigate to the Project and Pull Latest Code

`cd AshaChatbot` <br>
`git pull`  

### ✅ Step 3: Set Up Environment Variables
Create a .env file in:

AshaChatbot/.env <br>
AshaChatbot/ashaaiflow/.env <br>
Add your required secrets: <br>
- GEMINI_API_KEY=your_api_key  
- SERPAPI_KEY=your_serpapi_key  
- SECRET_KEY=your_secret  
- ALGORITHM=HS256  
- ACCESS_TOKEN_EXPIRE_MINUTES=30  
- FERNET_KEY=your_fernet_key  
- MODEL=gemini-1.5-flash

### ✅ Step 4: Build Docker Image (Backend)

`docker build -t fastapi-app .`
### ✅ Step 5: Run Docker Container (Backend)

`docker run -d -p 8000:8000 fastapi-app`
### ✅ Step 6: Check Docker Logs (Optional)

`docker logs <container_id>`  

## Frontend Deployment (React App)  

### ✅ Step 7: Navigate to Frontend Directory and Pull Code

`cd frontend/my-app` <br>
`git pull`  

### ✅ Step 8: Build Docker Image (Frontend)

`docker build -t my-asha-chatbot .`  

### ✅ Step 9: Run Docker Container (Frontend)

`docker run -d -p 3000:3000 my-asha-chatbot`  

## 🌐 Expose VM IP to Access the App  

To allow external traffic to your VM:  

Go to **VPC Network > Firewall** in the GCP Console.  

### Click Create Firewall Rule.

Name: allow-http <br>
Targets: All instances in the network <br>
Source IP ranges: 0.0.0.0/0 <br>
Protocols and ports: Check Specified protocols and ports, then allow: <br>
tcp:8000 <br>
tcp:3000 <br>

**Now you can access your app via:**

`http://<your-external-vm-ip>:3000  # Frontend` <br>
`http://<your-external-vm-ip>:8000  # Backend API`  

### ✅ Done!  

Your Asha AI Bot is now up and running on a GCP VM! 🎉
Make sure to monitor logs and container health for smooth operation.

# 🔄 Workflow Overview

1. **User Interaction**:  
   The user initiates a conversation with **Asha AI** via the frontend (React app). Asha listens to the user's query (e.g., job search, resume analysis, etc.).

2. **Intent Classification**:  
   Asha's **CrewAI-based agent** classifies the user's intent (e.g., job search, mentorship, resume feedback). Based on this intent, the appropriate backend agent is triggered.

3. **Specialized Agents**:  
   - **Job Search Agent**: Fetches relevant job listings from HerKey and SerpAPI.
   - **Resume Analyst**: Analyzes and provides feedback on the uploaded resume.
   - **Learning Advisor**: Recommends courses or learning resources based on user needs.

4. **Response Generation**:  
   The backend compiles the response (jobs, advice, feedback) and sends it back to the frontend.

5. **Bias Guardrails**:  
   Throughout the conversation, Asha checks for gender bias in questions and redirects or reframes as needed.

6. **User Receives Feedback**:  
   The frontend displays the relevant information (jobs, resources, or advice) to the user, offering a continuous, empathetic, and personalized experience.

![AshaAI](https://github.com/user-attachments/assets/87fbb4d3-9b61-47c3-9a44-79e35deab183)
