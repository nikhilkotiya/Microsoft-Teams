FROM python :3.8
ENV PYTHONUNBUFFERED = 1
WORKDIR /usr/src/Microsoft_Teams
COPY requirements.txt 
RUN pip install -r requirements.txt