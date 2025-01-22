FROM python:3.13.1
# # set work directory
WORKDIR /app
# # install dependencies
COPY ./requirements.txt /app
RUN pip install --upgrade -r requirements.txt 

COPY . /app

CMD ["uvicorn", "main:app", "--reload", "--host", "0.0.0.0", "--port", "3001"]