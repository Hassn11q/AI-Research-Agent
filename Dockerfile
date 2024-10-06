FROM python:3.11-slim 

WORKDIR /code 

COPY ./requirements.txt /code/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

COPY ./app /code/app

CMD ["fastapi" , "run" , "app.main:app" , "--port" , "80"]