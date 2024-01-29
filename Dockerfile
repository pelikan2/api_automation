FROM python:3.11-slim-buster
WORKDIR /python_api_automation
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
CMD ["pytest", "test_steps.py"]