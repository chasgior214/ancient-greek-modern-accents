# ancient-greek-modern-accents
Many native Modern Greek speakers will read and pronounce Ancient Greek texts (whether aloud or in their head) using modern pronunciation of the words. 

## Change Text to Modern Accents
The "ancient_text_to_modern_pronunciation" function in "ancient_to_modern.py" takes a text in polytonic Greek and returns it rendered in modern monotonic orthography. It could be used to either simplify a text for one's own reading, or to take an Ancient Greek text and turn it into a format that a text-to-speech software could speak according to Modern Greek pronunciation. 

### Example Usage
The function ancient_text_to_modern_pronunciation, when fed the first two sentences of [Epictetus' Enchiridion](https://el.wikisource.org/wiki/%CE%95%CE%B3%CF%87%CE%B5%CE%B9%CF%81%CE%AF%CE%B4%CE%B9%CE%BF%CE%BD):
> Τῶν ὄντων τὰ μέν ἐστιν ἐφ' ἡμῖν, τὰ δὲ οὐκ ἐφ' ἡμῖν. ἐφ' ἡμῖν μὲν ὑπόληψις, ὁρμή, ὄρεξις, ἔκκλισις καὶ ἑνὶ λόγῳ ὅσα ἡμέτερα ἔργα: οὐκ ἐφ' ἡμῖν δὲ τὸ σῶμα, ἡ κτῆσις, δόξαι, ἀρχαὶ καὶ ἑνὶ λόγῳ ὅσα οὐχ ἡμέτερα ἔργα.

Will output the following:
> Των όντων τα μεν εστιν εφ' ημίν, τα δε ουκ εφ' ημίν. εφ' ημίν μεν υπόληψις, ορμή, όρεξις, έκκλισις και ενί λόγω όσα ημέτερα έργα: ουκ εφ' ημίν δε το σώμα, η κτήσις, δόξαι, αρχαί και ενί λόγω όσα ουχ ημέτερα έργα.

## Create Audio from Ancient Text
The "text_to_speech" function in "tts.py" takes a text in polytonic Greek and uses text-to-speech software to convert it into audio. It optionally takes in Azure credentials to use Azure's Speech Service, and otherwise it uses gTTS (https://github.com/pndurette/gTTS).