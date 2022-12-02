# scrub-to-keyword
## Video summarization framework

## WARNING!

Do *not* expose this to the web as is - there is currently no rate-limiting, old video and audio is not cleaned out after processing, and there is no validation of input.

## Summary

Tries to generate a transcript and a summary of videos.

1. (Optional) Use FFMPEG to extract the audio
2. Use the OpenAI Whisper TTS engine to transcribe the video/audio (ideally with alignment)
3. Pass the transcription to the YAKE summarizer 

Run with
```
pip install -r requirements.txt
flask run
```

and navigate to `localhost:5000`.

Note: Whisper will download the model during the first transcription, this may take some time.


