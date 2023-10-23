# ancient-greek-modern-accents

Many native Modern Greek speakers will read and pronounce Ancient Greek texts (whether in their head or aloud) using modern pronunciation of the words. 

This script takes a text in polytonic Greek and outputs the words in modern monotonic orthography. It could be used to either simplify a text for one's own reading, or to take an Ancient Greek text and turn it into a format that a text-to-speech software could speak according to Modern Greek pronunciation. 

### Example Usage

The function ancient_text_to_modern_pronunciation, if it is fed the first two sentences of [Epictetus' Enchiridion](https://dcc.dickinson.edu/epictetus-encheiridion/chapter-1):
> τῶν ὄντων τὰ μέν ἐστιν ἐφ' ἡμῖν, τὰ δὲ οὐκ ἐφ' ἡμῖν. ἐφ' ἡμῖν μὲν ὑπόληψις, ὁρμή, ὄρεξις, ἔκκλισις καὶ ἑνὶ λόγῳ ὅσα ἡμέτερα ἔργα· οὐκ ἐφ' ἡμῖν δὲ τὸ σῶμα, ἡ κτῆσις, δόξαι, ἀρχαὶ καὶ ἑνὶ λόγῳ ὅσα οὐχ ἡμέτερα ἔργα.

Will output the following:
> των όντων τα μεν εστιν εφ' ημίν, τα δε ουκ εφ' ημίν. εφ' ημίν μεν υπόληψις, ορμή, όρεξις, έκκλισις και ενί λόγω όσα ημέτερα έργα· ουκ εφ' ημίν δε το σώμα, η κτήσις, δόξαι, αρχαί και ενί λόγω όσα ουχ ημέτερα έργα.
