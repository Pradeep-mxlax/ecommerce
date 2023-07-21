FROM python:3.10.4-slim
ADD . /app/server
WORKDIR /app/server
COPY . requirements.txt /app/server/
COPY . /app/server/
RUN pip install --upgrade pip && pip install -r requirements.txt

CMD [ "python","manage.py","runserver" ,"0.0.0.0:8000"]