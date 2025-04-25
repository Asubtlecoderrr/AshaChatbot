# **🚀 Asha AI Bot – Deployment Guide**  

This guide will help you set up and deploy the Asha AI chatbot (FastAPI backend + React frontend) on a Google Cloud VM instance using Docker.

## 📦 Local Development   
### ✅ Frontend

`cd frontend/my-app`
`npm install`
`npm run start`  
### ✅ Backend

`pip install -r requirements.txt`
`uvicorn backend.main:app`

## ☁️ GCP VM Deployment Using Docker  

### ✅ Step 1: SSH into Your VM
Use the Google Cloud Console or gcloud CLI to SSH into your VM instance.

### ✅ Step 2: Navigate to the Project and Pull Latest Code

`cd AshaChatbot`
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

`cd frontend/my-app`
`git pull`  

### ✅ Step 8: Build Docker Image (Frontend)

`docker build -t my-asha-chatbot .`  

### ✅ Step 9: Run Docker Container (Frontend)

`docker run -d -p 3000:3000 my-asha-chatbot`  

## 🌐 Expose VM IP to Access the App  

To allow external traffic to your VM:  

Go to **VPC Network > Firewall** in the GCP Console.  

### Click Create Firewall Rule.

Name: allow-http
Targets: All instances in the network
Source IP ranges: 0.0.0.0/0
Protocols and ports: Check Specified protocols and ports, then allow:
tcp:8000
tcp:3000

**Now you can access your app via:**

`http://<your-external-vm-ip>:3000  # Frontend`
`http://<your-external-vm-ip>:8000  # Backend API`  

### ✅ Done!  

Your Asha AI Bot is now up and running on a GCP VM! 🎉
Make sure to monitor logs and container health for smooth operation.


![AshaAI](https://github.com/user-attachments/assets/87fbb4d3-9b61-47c3-9a44-79e35deab183)
