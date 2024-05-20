FROM python:3.9

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 5001

ENV FLASK_APP app.py

CMD bash -c "if [ ! -d 'migrations' ]; then flask db init; fi && \
    flask db migrate && \
    flask db upgrade && \
    flask run --host=0.0.0.0 --port=5001"
