import unicodedata
import re

lowercase_vowels_without_accents = {'α', 'ε', 'η', 'ι', 'ο', 'υ', 'ω'}
diphthongs = {'αι','αυ','ει','ευ','ου','οι'}
accents_i_do_not_care_about = {'\u0313', '\u0314','\u0345'} # the psili, the daseia, and the iota subscript
modern_tono = '\u0301'
diaeresis = '\u0308'

def remove_accents(text): return ''.join(c for c in text if not unicodedata.combining(c))
def count_accents(text): return sum(1 for char in text if unicodedata.category(char) == 'Mn')
def count_vowels(text): return len([char for char in text.lower() if char in lowercase_vowels_without_accents])

def ancient_text_to_modern_pronunciation(ancient_text):
    """
    This functions takes an Ancient Greek text, removes its accents, and adds accents such that the words are pronounced with a modern pronunciation
    """
    text_with_accent_chars_separate = unicodedata.normalize('NFD',ancient_text)
    words = text_with_accent_chars_separate.split()
    output_words_list = []
    
    for word in words:
        # strip the accents that don't matter
        word = ''.join([char for char in word if char not in accents_i_do_not_care_about])
        # count remaining accents
        num_accents = count_accents(word) 
        # if no accent, no accents
        if num_accents == 0:
            output_words_list.append(word + ' ')
            continue
        # if one vowel, no accents
        vowel_count = count_vowels(word)
        if vowel_count == 1:
            output_words_list.append(remove_accents(word) + ' ')
            continue
        # if only two vowels and they make a diphthong
        if vowel_count == 2 and not all(not bool(re.search(re.escape(chars), remove_accents(word))) for chars in diphthongs): 
            # if the diphthong has no diaeresis, no accents
            if "\u0308" not in word:
                output_words_list.append(remove_accents(word) + ' ')
                continue
            # if the diphthong has only a diaeresis, keep word as-is
            elif num_accents == 1: 
                output_words_list.append(word + ' ')
                continue
            # if the diphthong has a diaeresis and one oxia, keep word as-is (tono has same unicode representation as oxia)
            elif num_accents == 2 and '\u0301' in word:
                output_words_list.append(word + ' ')
                continue
            # if the diphthong has a diaeresis and either one perispomeni or one vareia, replace perispomeni/vareia with tono
            elif num_accents == 2:
                if '\u0300' in word:
                    output_words_list.append(word.replace('\u0300', '\u0301') + ' ')
                    continue
                elif '\u0342' in word:
                    output_words_list.append(word.replace('\u0342', '\u0301') + ' ')
                    continue
            # if the diphthong has a diaeresis and some other combination of accents, give up
            else:
                output_words_list.append(word + ' ')
                continue
        # list each letter and its accents
        non_accent_chars = [char for char in word if not unicodedata.combining(char)]
        num_non_accent_chars = len(non_accent_chars)
        accents_in_word = [char for char in word if unicodedata.combining(char)]
        accent_character_locations = []
        position = -1
        for char in word:
            if not unicodedata.combining(char):
                position+=1
            else:
                accent_character_locations.append(position)
        # if only one accent, modern accent on that letter
        if num_accents == 1:
            word = ''
            for i in range(num_non_accent_chars):
                word += non_accent_chars[i]
                if i == accent_character_locations[0]:
                    word += modern_tono
            output_words_list.append(word + ' ')
            continue
        # if exactly 2 accents, and both are either oxiae, perispomeni, or vareia, modern tono only on the first one
        if num_accents == 2:
            if accents_in_word[0] in {'\u0300', '\u0301', '\u0342'} and accents_in_word[1] in {'\u0300', '\u0301', '\u0342'}:
                word = ''
                for i in range(num_non_accent_chars):
                    word += non_accent_chars[i]
                    if i == accent_character_locations[0]:
                        word += modern_tono
                output_words_list.append(word + ' ')
                continue
        # if one diaeresis and either an oxia, a perispomeni, or a vareia, keep diaeresis as-is (ancient and modern diaeresis have the same unicode representations), and turn the other accent into a tono
            if diaeresis in accents_in_word:
                if '\u0301' in accents_in_word[0] or '\u0301' in accents_in_word[1]:
                    output_words_list.append(word + ' ')
                    continue
                elif '\u0342' in accents_in_word[0] or '\u0342' in accents_in_word[1]:
                    output_words_list.append(word.replace('\u0342', '\u0301') + ' ')
                    continue
                elif '\u0300' in accents_in_word[0] or '\u0300' in accents_in_word[1]:
                    output_words_list.append(word.replace('\u0300', '\u0301') + ' ')
                    continue
        # giving up on other cases
        print(word) # list words it's given up on
        output_words_list.append(word + ' ')
    output_words = ''.join(output_words_list)
    return(output_words)
