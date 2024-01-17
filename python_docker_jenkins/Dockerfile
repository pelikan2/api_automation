FROM python:3.11-slim-buster
ADD . /python_api_automation
WORKDIR /python_api_automation
RUN pip install pytest
RUN pip install requests
CMD [ "python3 pytest -m user -v -s", "./test_steps.py"]