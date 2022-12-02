FROM python:3.9
ADD requirements.txt /app/requirements.txt
WORKDIR /app/
RUN pip install --no-cache-dir -r requirements.txt
RUN python -c "import whisper; whisper.load_model('small')"
RUN apt-get update && apt-get install -y ffmpeg 
ADD . /app/
ENV RUNNING_IN_CONTAINER=true
CMD python app.py