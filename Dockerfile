FROM python:3.9-slim

# Install Tesseract
RUN apt-get update && apt-get install -y tesseract-ocr


# Copy requirements and install them
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

# Copy the application code
COPY . .

# Set the command to run the Streamlit app
CMD ["streamlit", "run", "ind.py"]
