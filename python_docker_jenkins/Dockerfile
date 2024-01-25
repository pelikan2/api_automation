FROM python:3.11-slim-buster
#ADD . /python_api_automation
WORKDIR /python_api_automation
COPY . /python_api_automation
RUN pip3 install pytest
RUN pip3 install requests
CMD ["pytest" , "test_steps.py" ]