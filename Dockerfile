FROM python:3.7-alpine
# FROM dreen/flask

WORKDIR /app

# Install dependencies.
ADD requirements.txt /app
RUN cd /app && \
    pip install -r requirements.txt

# RUN apt install python3-flask

# Add actual source code.
ADD Blockchain.py /app
ADD app.py /app

EXPOSE 5000
# Exposing the Local Port of 5000 for further Usage 

CMD ["python", "app.py"]
