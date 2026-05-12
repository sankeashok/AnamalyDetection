# Use an official lightweight Python image
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file first to leverage Docker cache
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code
# (Models, App, and Preprocessing artifacts)
COPY api.py .
COPY network_anomaly_model.pkl .
COPY scaler.pkl .
COPY label_encoders.pkl .
COPY feature_names.pkl .

# Expose the port Hugging Face requires
EXPOSE 7860

# Set environment variables
ENV FLASK_APP=api.py
ENV FLASK_RUN_HOST=0.0.0.0

# Command to run the application
# We use gunicorn for a production-ready server instead of the Flask dev server
RUN pip install gunicorn
CMD ["gunicorn", "--bind", "0.0.0.0:7860", "api:app"]
