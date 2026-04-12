def text_processing(ancient_string):
    from ancient_to_modern import ancient_text_to_modern_pronunciation
    modern_accent_string = ancient_text_to_modern_pronunciation(ancient_string)

    # combine single consonants with following word - add support for 'δ'' etc?
    modern_accent_words = modern_accent_string.split(' ')
    lowercase_consonants = {'β', 'γ', 'δ', 'ζ', 'θ', 'κ', 'λ', 'μ', 'ν', 'ξ', 'π', 'ρ', 'σ', 'ς', 'τ', 'φ', 'χ', 'ψ'}
    final_word_list = []
    consonant_prefix = ''
    for word in modern_accent_words:
        if len(word) == 1:
            if word in lowercase_consonants:
                consonant_prefix = word
            else:
                final_word_list.append(word)
        else:
            final_word_list.append(consonant_prefix+word)
            consonant_prefix = ''
    final_string = ' '.join(final_word_list)

    return final_string

def text_to_speech(ancient_text: str, azure_key: str = None, azure_region: str = None, azure_voice: str = None, fileName: str = None, skip_processing: bool = False):
    """
    Converts polytonic Ancient Greek text to audio using Modern Greek phonology.

    Parameters
    ----------
    ancient_text : str
        String of polytonic Ancient Greek text to be converted to audio.
    azure_key : str, optional
        Azure Speech Service key. If provided, Azure's TTS service will be used. Otherwise, gTTS is used.
    azure_region : str, optional
        Azure region for the Speech Service (e.g., 'eastus'). Required if `azure_key` is provided.
    azure_voice : str, optional
        Azure voice name to use for speech synthesis (e.g., 'el-GR-AthinaNeural'). Required if `azure_key` is provided.
    fileName : str, optional
        File name to save the generated audio (e.g., 'output.mp3'). If not provided, the audio will not be saved.
    skip_processing : bool, optional
        If True, skips text processing using the `text_processing` function and directly uses the input `ancient_text` for TTS. Default is False.

    Returns
    -------
    result : azure.cognitiveservices.speech.SpeechSynthesisResult or gtts.gTTS
        The result of the text-to-speech operation. If Azure TTS is used, returns an Azure SpeechSynthesisResult.
        If gTTS is used, returns a gTTS object.
    """
    if skip_processing:
        text = ancient_text
    else:
        text = text_processing(ancient_text)

    if azure_key:
        import azure.cognitiveservices.speech as speechsdk
        speech_config = speechsdk.SpeechConfig(subscription=azure_key, region=azure_region)
        speech_config.speech_synthesis_voice_name = azure_voice
        speech_synthesizer = speechsdk.SpeechSynthesizer(speech_config=speech_config)
        result = speech_synthesizer.speak_text_async(text).get()
        if fileName:
            with open(fileName, 'wb') as file:
                file.write(result.audio_data)
        return result
    else:
        from gtts import gTTS
        result = gTTS(text=text, lang='el')
        if fileName:
            result.save(fileName)
        return result