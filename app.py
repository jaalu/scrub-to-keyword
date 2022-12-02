import argparse
import logging
import random

import ffmpeg
import whisper
import yake
import yake.highlight
import os
logging.basicConfig(level=logging.DEBUG)

from flask import Flask, render_template, send_from_directory, request
app = Flask(__name__)

MAX_KEYWORDS = 10

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/audio/<path:path>")
def send_audio(path):
    return send_from_directory('audio', path)

@app.post("/process")
def process():
    file = request.files['file']
    logging.debug("Extracting audio from video.")

    video_path = "upload/video" + str(random.randint(0, 2**31))
    file.save(video_path)

    audio_path = "audio/audio" + str(random.randint(0, 2**31)) + ".wav"
    in_file = ffmpeg.input(video_path)
    audio = in_file.audio
    out = ffmpeg.output(audio, audio_path).overwrite_output().run()

    
    logging.debug("Running TTS.")
    model = whisper.load_model("small")
    results = model.transcribe(audio_path)
    lang = results['language']
    print("Model guesses language:", lang)

    print("Performing keyword extraction.")
    full_text = results['text']
    kw_extractor = yake.KeywordExtractor(lan=lang, top=MAX_KEYWORDS)
    keywords = kw_extractor.extract_keywords(full_text)
    keyword_list = [kw[0] for kw in keywords]
    
    th = yake.highlight.TextHighlighter(max_ngram_size = 3, highlight_pre = "**", highlight_post= "**")
    print("Highlighting in transcription")
    transcript = [(segment["start"], th.highlight(segment["text"], keywords)) for segment in results["segments"]]

    return render_template("viewer.html", audio_source=audio_path, transcription=transcript, audio_keywords = keyword_list)

if __name__ == '__main__' and os.getenv('RUNNING_IN_CONTAINER') == 'true':
    app.run(host='0.0.0.0', port=5000)