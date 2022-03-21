#
FROM python:3.9
#
WORKDIR /code
#
COPY ./requirements.txt /code/requirements.txt
COPY ./src /code/src
COPY ./templates /code/templates
COPY ./main.py /code/
#
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt
#
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "80"]
