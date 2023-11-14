import sys
sys.path.append('./')
from ancient_to_modern import ancient_text_to_modern_pronunciation
from tts import text_to_speech

def enchiridion_to_string():
    # Enchiridion of Epictetus sourced from https://github.com/jtauber/enchiridion/blob/master/text/enchiridion.txt
    with open('example/Enchiridion.txt', 'r', encoding='utf-8') as file:
        lines_list = []
        for line in file:
            space_location = line.find(' ')
            lines_list.append(line[space_location+1:].strip())
    enchir_string = ''
    for line in lines_list:
        enchir_string += line.strip() + ' '
    return enchir_string

enchir_string = enchiridion_to_string()

# convert first chapter of Enchiridion to modern pronunciation
enchir_modern_ch_1 = ancient_text_to_modern_pronunciation(enchir_string[:1371])
print('The monotonic representation of the first chapter of the Enchiridion is:\n')
print(enchir_modern_ch_1)

TTS_string = enchir_modern_ch_1
azure_TTS_API_key = None
azure_TTS_region = 'eastus'

text_to_speech(TTS_string, azure_key=azure_TTS_API_key, azure_region=azure_TTS_region, azure_voice='el-GR-AthinaNeural', fileName='example/output.mp3')
