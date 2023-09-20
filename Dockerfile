FROM python:3.10
WORKDIR /code
COPY ../requirements.txt /code/
RUN pip install -r requirements.txt
COPY .. /code/
RUN pip install python-dotenv


