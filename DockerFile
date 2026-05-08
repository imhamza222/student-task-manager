cd ~/devops-assignment/devops-flask-app

# Create Dockerfile
cat > Dockerfile << 'EOF'
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Initialize database
RUN python -c "from app import app, db; app.app_context().push(); db.create_all()"

EXPOSE 5000

CMD ["python", "app.py"]
EOF