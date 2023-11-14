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

def text_to_speech(ancient_text, azure_key=None, azure_region=None, azure_voice=None, fileName = None):
    """
    ancient_text: string of polytonic Ancient Greek text
    azure_voice: string of Azure voice name ('el-GR-AthinaNeural', 'el-GR-NestorasNeural')
    azure_key: string of Azure key
    azure_region: string of Azure region (e.g. 'eastus')
    fileName: string of file name to save to (e.g. 'output.mp3')
    """
    text = text_processing(ancient_text)
    if azure_key:
        import azure.cognitiveservices.speech as speechsdk
        speech_config = speechsdk.SpeechConfig(subscription=azure_key, region=azure_region)
        speech_config.speech_synthesis_voice_name = azure_voice
        speech_synthesizer = speechsdk.SpeechSynthesizer(speech_config=speech_config)
        result = speech_synthesizer.speak_text_async(text).get()
        if fileName:
            with open(fileName, 'wb') as file: file.write(result.audio_data)
        return result
    else:
        from gtts import gTTS
        result = gTTS(text=text, lang='el')
        if fileName:
            result.save(fileName)
        return result