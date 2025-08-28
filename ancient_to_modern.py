import unicodedata
import re

lowercase_vowels_without_accents = {'α', 'ε', 'η', 'ι', 'ο', 'υ', 'ω'}
diphthongs = {'αι','αυ','ει','ευ','ου','οι'}
unimportant_accents = {'\u0313', '\u0314','\u0345'} # the psili, the daseia, and the iota subscript
modern_tono = '\u0301'
diaeresis = '\u0308'

def remove_accents(text): return ''.join(c for c in text if not unicodedata.combining(c))
def count_accents(text): return sum(1 for char in text if unicodedata.category(char) == 'Mn')
def count_vowels(text): return len([char for char in text.lower() if char in lowercase_vowels_without_accents])

def split_text_into_words(text: str):
    """Splits a text into a list of words and punctuation/whitespace so that words are delimited correctly."""
    # This regex matches sequences of Greek letters (including accented ones) and separates them from punctuation
    return re.findall(r'\b[\w\u0300-\u036f]+\b|[^\w\s]|\s+', text, re.UNICODE)

def modern_accents_on_word(word: str, debug: bool = False):
    """Applies modern Greek accentuation rules to a single word."""

    # strip accents that don't matter
    word = ''.join([char for char in word if char not in unimportant_accents])

    # count remaining accents, number of vowels
    num_accents = count_accents(word)
    vowel_count = count_vowels(word)

    # if no vowels, just return the string of consonants
    if vowel_count == 0:
        return word

    # if no accent, no accents
    if num_accents == 0:
        if debug:
            if vowel_count > 1 and (vowel_count > 2 or all(not bool(re.search(re.escape(chars), remove_accents(word.lower()))) for chars in diphthongs)): print(f'Word should have accent(s) but could not find appropriate position(s): {word}')
        return word

    # if one vowel, no accents
    if vowel_count == 1:
        return remove_accents(word)

    # if only two vowels and they make a diphthong
    if vowel_count == 2 and not all(not bool(re.search(re.escape(chars), remove_accents(word.lower()))) for chars in diphthongs): 
        # if the diphthong has no diaeresis, no accents
        if "\u0308" not in word:
            return remove_accents(word)
        # if the diphthong has only a diaeresis, keep word as-is
        elif num_accents == 1:
            return word
        # if the diphthong has a diaeresis and one oxia, keep word as-is (tono has same unicode representation as oxia)
        elif num_accents == 2 and "\u0301" in word:
            return word
        # if the diphthong has a diaeresis and either one perispomeni or one vareia, replace perispomeni/vareia with a tono
        elif num_accents == 2:
            if "\u0300" in word:
                word = word.replace("\u0300", modern_tono)
            if "\u0342" in word:
                word = word.replace("\u0342", modern_tono)
            return word
        # if the diphthong has a diaeresis and some other combination of accents, give up
        if debug: print(f'Could not find appropriate accent(s) for: {word}')
        return word

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
    
    # if only one accent, modern tono on that letter
    if num_accents == 1:
        word = ''
        for i in range(num_non_accent_chars):
            word += non_accent_chars[i]
            if i == accent_character_locations[0]:
                word += modern_tono
        return word

    # if exactly 2 accents, and both are either oxiae, perispomeni, or vareia, modern tono only on the first one
    if num_accents == 2:
        if accents_in_word[0] in {'\u0300', '\u0301', '\u0342'} and accents_in_word[1] in {'\u0300', '\u0301', '\u0342'}:
            word = ''
            for i in range(num_non_accent_chars):
                word += non_accent_chars[i]
                if i == accent_character_locations[0]:
                    word += modern_tono
            return word

    # if one diaeresis and either an oxia, a perispomeni, or a vareia, keep diaeresis as-is (ancient and modern diaeresis have the same unicode representations), and turn the other accent into a tono
        if diaeresis in accents_in_word:
            if '\u0301' in accents_in_word[0] or '\u0301' in accents_in_word[1]:
                return word
            elif '\u0342' in accents_in_word[0] or '\u0342' in accents_in_word[1]:
                return word.replace('\u0342', '\u0301')
            elif '\u0300' in accents_in_word[0] or '\u0300' in accents_in_word[1]:
                return word.replace('\u0300', '\u0301')

    # give up on other cases
    if debug: print(f"Could not find appropriate accent(s) for: {word}")
    return word

def ancient_text_to_modern_pronunciation(ancient_text : str, debug: bool = False):
    """
    Takes polytonic Greek text, converts its diacritics (accents) into monotonic orthography corresponding to Modern Greek phonology.

    Args
    ----
    ancient_text : str
        Polytonic Greek text.

    Returns
    -------
    str
        Monotonic Greek text corresponding to Modern Greek phonology.
    """
    output_text = ''
    chunks = split_text_into_words(ancient_text)
    for chunk in chunks:
        # split accents characters from letters
        word = unicodedata.normalize('NFD', chunk)
        has_greek_letters = any('\u0391' <= c <= '\u03CA' for c in word)
        # if it's a word
        if has_greek_letters:
            # apply modern accents
            word = modern_accents_on_word(word, debug)
            # recombine accents into letters
            word = unicodedata.normalize('NFC', word)
            output_text += word
        # if it's punctuation/whitespace/numeric/etc
        else:
            output_text += chunk

    return output_text

if __name__ == "__main__":
    text_tester = """ὁ
1.1 τῶν ὄντων τὰ μέν ἐστιν ἐφ ἡμῖν, τὰ δὲ οὐκ ἐφ ἡμῖν. ἐφ ἡμῖν μὲν ὑπόληψις, ὁρμή, ὄρεξις, ἔκκλισις καὶ ἑνὶ λόγῳ ὅσα ἡμέτερα ἔργα: οὐκ ἐφ ἡμῖν δὲ τὸ σῶμα, ἡ κτῆσις, δόξαι, ἀρχαὶ καὶ ἑνὶ λόγῳ ὅσα οὐχ ἡμέτερα ἔργα.
1.2 καὶ τὰ μὲν ἐφ ἡμῖν ἐστι φύσει ἐλεύθερα, ἀκώλυτα, ἀπαραπόδιστα, τὰ δὲ οὐκ ἐφ ἡμῖν ἀσθενῆ, δοῦλα, κωλυτά, ἀλλότρια. μέμνησο οὖν,
1.3 ὅτι, ἐὰν τὰ φύσει δοῦλα ἐλεύθερα οἰηθῇς καὶ τὰ ἀλλότρια ἴδια, ἐμποδισθήσῃ, πενθήσεις, ταραχθήσῃ, μέμψῃ καὶ θεοὺς καὶ ἀνθρώπους, ἐὰν δὲ τὸ σὸν μόνον οἰηθῇς σὸν εἶναι, τὸ δὲ ἀλλότριον, ὥσπερ ἐστίν, ἀλλότριον, οὐδείς σε ἀναγκάσει οὐδέποτε, οὐδείς σε κωλύσει, οὐ μέμψῃ οὐδένα, οὐκ ἐγκαλέσεις τινί, ἄκων πράξεις οὐδὲ ἕν, οὐδείς σε βλάψει, ἐχθρὸν οὐχ ἕξεις, οὐδὲ γὰρ βλαβερόν τι πείσῃ.
1.4 τηλικούτων οὖν ἐφιέμενος μέμνησο, ὅτι οὐ δεῖ μετρίως κεκινημένον ἅπτεσθαι αὐτῶν, ἀλλὰ τὰ μὲν ἀφιέναι παντελῶς, τὰ δ ὑπερτίθεσθαι πρὸς τὸ παρόν. ἐὰν δὲ καὶ ταῦτ ἐθέλῃς καὶ ἄρχειν καὶ πλουτεῖν, τυχὸν μὲν οὐδ αὐτῶν τούτων τεύξῃ διὰ τὸ καὶ τῶν προτέρων ἐφίεσθαι, πάντως γε μὴν ἐκείνων ἀποτεύξη, δι ὧν μόνων ἐλευθερία καὶ εὐδαιμονία περιγίνεται.
1.5 εὐθὺς οὖν πάσῃ φαντασίᾳ τραχείᾳ μελέτα ἐπιλέγειν ὅτι «φαντασία εἶ καὶ οὐ πάντως τὸ φαινόμενον.» ἔπειτα ἐξέταζε αὐτὴν καὶ δοκίμαζε τοῖς κανόσι τούτοις οἷς ἔχεις, πρώτῳ δὲ τούτῳ καὶ μάλιστα, πότερον περὶ τὰ ἐφ ἡμῖν ἐστιν ἢ περὶ τὰ οὐκ ἐφ ἡμῖν: κἂν περί τι τῶν οὐκ ἐφ ἡμῖν ᾖ, πρόχειρον ἔστω τὸ διότι «οὐδὲν πρὸς ἐμέ».
"""
    print(ancient_text_to_modern_pronunciation(text_tester, True))
    print(split_text_into_words(text_tester))