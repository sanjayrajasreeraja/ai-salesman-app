import whisper


def transcribe_audio(path, model_size='small', language=None):
    model = whisper.load_model(model_size)
    kwargs = {'fp16': False}
    if language:
        kwargs['language'] = language
    result = model.transcribe(path, **kwargs)
    return result['text'], result.get('language', None)


def translate_to_english(path, model_size='small'):
    model = whisper.load_model(model_size)
    result = model.transcribe(path, task='translate', fp16=False)
    return result['text']


if __name__ == "__main__":
    WAV_FILE = '/Users/amartyanambiar/Projects/AI Salesman/recording/recording_20240910_153703.wav'
    transcript, lang = transcribe_audio(WAV_FILE)
    print('Transcription:')
    print(transcript)
    if lang != 'en':
        translation = translate_to_english(WAV_FILE)
        print('Translation to English:')
        print(translation)

