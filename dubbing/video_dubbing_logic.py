import os
import subprocess
from deep_translator import GoogleTranslator
import whisper
from gtts import gTTS
from pydub import AudioSegment

# Initialize Whisper model
model = whisper.load_model("medium.en")

# Supported languages and their language codes
LANGUAGE_CODES = {
    'es': 'es',    # Spanish
    'mr': 'mr',    # Marathi
    'hi': 'hi',    # Hindi
    'ta': 'ta',    # Tamil
    'te': 'te',    # Telugu
    'ru': 'ru',    # Russian
    'ja': 'ja',    # Japanese
    'fr': 'fr',    # French
    'de': 'de',    # German
    'it': 'it',    # Italian
    'ar': 'ar',    # Arabic
    'bn': 'bn',    # Bengali
    'pa': 'pa',    # Punjabi
    'gu': 'gu'     # Gujarati
}

def process_video(file_path, target_language):
    audio_path = extract_audio(file_path)
    transcription, segments = transcribe_audio(audio_path)
    translated_segments = translate_segments(segments, target_language)
    
    # Create the dubbed audio with synced timing
    dubbed_audio_path = text_to_speech_with_timestamps(translated_segments, target_language)
    
    # Merge the final dubbed audio with the original video (excluding original audio)
    dubbed_video_path = merge_audio_with_video(file_path, dubbed_audio_path)

    # Clean up temporary files
    os.remove(audio_path)
    os.remove(dubbed_audio_path)

    return dubbed_video_path

def extract_audio(video_path):
    audio_path = os.path.splitext(video_path)[0] + "_audio.wav"
    command = f"ffmpeg -i \"{video_path}\" -q:a 0 -map a \"{audio_path}\""
    subprocess.run(command, shell=True, check=True)
    return audio_path

def transcribe_audio(audio_path):
    result = model.transcribe(audio_path, word_timestamps=True)
    segments = result['segments']
    return result['text'], segments

def translate_segments(segments, target_language):
    language_code = LANGUAGE_CODES.get(target_language, 'en')
    translator = GoogleTranslator(source='auto', target=language_code)
    
    translated_segments = []
    for segment in segments:
        translated_text = translator.translate(segment['text'])
        translated_segments.append({
            'start': segment['start'],
            'end': segment['end'],
            'text': translated_text
        })
    
    return translated_segments

def text_to_speech_with_timestamps(segments, language):
    language_code = LANGUAGE_CODES.get(language, 'en')
    dubbed_audio_output = os.path.splitext(language)[0] + f"_dubbed_{language_code}.mp3"
    
    combined_audio = AudioSegment.silent(duration=int(segments[-1]['end'] * 1000))  # Create an empty audio file of the duration of the last word segment
    
    for segment in segments:
        tts = gTTS(text=segment['text'], lang=language_code)
        temp_audio = os.path.splitext(language)[0] + "_temp.mp3"
        tts.save(temp_audio)

        # Load the temporary TTS audio and add it at the correct timestamp
        tts_audio = AudioSegment.from_mp3(temp_audio)
        start_time = int(segment['start'] * 1000)
        combined_audio = combined_audio.overlay(tts_audio, position=start_time)

        os.remove(temp_audio)  # Clean up the temporary audio file
    
    combined_audio.export(dubbed_audio_output, format="mp3")
    return dubbed_audio_output

def merge_audio_with_video(video_path, audio_path):
    output_video_path = os.path.splitext(video_path)[0] + "_dubbed_video.mp4"
    
    # Use FFmpeg to replace the original audio with the dubbed audio
    command = f"ffmpeg -i \"{video_path}\" -i \"{audio_path}\" -c:v copy -map 0:v -map 1:a -shortest \"{output_video_path}\""
    subprocess.run(command, shell=True, check=True)
    
    return output_video_path