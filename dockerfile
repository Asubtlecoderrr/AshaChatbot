FROM python:3.11

# Set the working directory inside the container to /app
WORKDIR /app

# Copy the requirements.txt file to the container
COPY requirements.txt .

# Upgrade pip to the latest version
RUN pip install --upgrade pip

# Install pydantic[email] and all other dependencies from the requirements.txt file
RUN pip install pydantic[email]

# Install the dependencies from requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy the entire backend directory (which includes main.py and other folders) into /app/backend
COPY backend /app/backend

# Copy the ashaaiflow directory (or any other dependent folder) into the container
COPY ashaaiflow /app/ashaaiflow

# Copy the shared directory (or any other dependent folder) into the container
COPY shared /app/shared

# Copy the frontend directory into the container
COPY frontend /app/frontend

# Set environment variables if needed (e.g., for .env file)
# You can optionally add the .env file or configure them here

# Run the FastAPI app with Uvicorn, pointing to the main.py file inside backend
CMD ["uvicorn", "backend.main:app", "--host", "0.0.0.0", "--port", "8000"]
