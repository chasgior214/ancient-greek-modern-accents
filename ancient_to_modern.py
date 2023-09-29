import unicodedata
import re

lowercase_vowels_without_accents = ['α', 'ε', 'η', 'ι', 'ο', 'υ', 'ω']
diphthongs = ['αι','αυ','ει','ευ','ου','οι']
modern_tono = '\u0301'
diaeresis = '\u0308'


def remove_accents(text_string):
    """
    This function removes all accents from a string
    """
    normalized_letter = unicodedata.normalize('NFD', text_string)
    string_without_accents = ''.join(c for c in normalized_letter if not unicodedata.combining(c))
    return string_without_accents

def count_accents(text):
    """
    This function counts the number of accents in a piece of text
    """
    normalized_text = unicodedata.normalize('NFD', text)
    count = 0

    for char in normalized_text:
        if unicodedata.category(char) == 'Mn':
            count += 1
    return count

def count_vowels(text):
    """
    This function counts the number of vowels in a piece of text
    """
    normalized_text = unicodedata.normalize('NFD', text)
    count = 0

    for char in normalized_text:
        if char.lower() in lowercase_vowels_without_accents:
            count += 1 
    return count

def ancient_text_to_modern_pronunciation(ancient_text):
    """
    This functions takes an Ancient Greek text, removes its accents, and adds accents such that the words are pronounced with a modern pronunciation
    """
    text_with_accent_chars_separate = unicodedata.normalize('NFD',ancient_text)
    words = text_with_accent_chars_separate.split()
    output_words = ''
    accents_i_do_not_care_about = ['\u0313', '\u0314','\u0345']

    for word in words:
        # strip the accents that mean nothing (the psili, the daseia, and the iota subscript)
        word = ''.join([char for char in word if char not in accents_i_do_not_care_about])
        # count remaining accents
        num_accents = count_accents(word) 
        # if no accent, no accents
        if num_accents == 0:
            output_words += word + ' '
            continue
        # if one vowel, no accents
        vowel_count = count_vowels(word)
        if vowel_count == 1:
            output_words += remove_accents(word) + ' '
            continue
        # if only two vowels and they make a diphthong, no accent
        if vowel_count == 2 and not all(not bool(re.search(re.escape(chars), remove_accents(word))) for chars in diphthongs): 
            output_words += remove_accents(word) + ' '
            continue
        # list each letter and its accents
        non_accent_chars = [char for char in word if not unicodedata.combining(char)]
        num_non_accent_chars = len(non_accent_chars)
        accents_in_word = [char for char in word if unicodedata.combining(char)]
        accent_character_locations = []
        position = 0
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
                if i == accent_character_locations[-1]:
                    word += modern_tono
            output_words += word + ' '
            continue
        # if exactly 2 oxiae, modern tono only on the first one
        if num_accents == 2:
            if accents_in_word[0]=='\u0301' and accents_in_word[1]=='\u0301':
                word = ''
                for i in range(num_non_accent_chars):
                    word += non_accent_chars[i]
                    if i == accent_character_locations[0]:
                        word += modern_tono
                output_words += word + ' '
                continue
        # if only one oxia and one diaeresis, keep as-is (oxia has same unicode representation as modern tono, ancient and modern diaeresis have the same unicode representations)
            if (accents_in_word[0]=='\u0301' or accents_in_word[0] == diaeresis) and (accents_in_word[1]=='\u0301' or accents_in_word[1]== diaeresis):
                output_words += word + ' '
                continue                
        # giving up on other cases
        print(word) # list words it's given up on
        output_words += word + ' '
    return(output_words)
