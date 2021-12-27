from google_trans_new import google_translator, constant
import deepl
import re

URL_SUFFIX_LIST = [re.search('translate.google.(.*)', url.strip()).group(1) for url in constant.DEFAULT_SERVICE_URLS]

TargetLangs = ["af", "sq", "am", "ar", "hy", "az", "eu", "be", "bn", "bs", "bg", "ca", "ceb", "ny", "zh-CN", "zh-TW", "co",
                "hr", "cs", "da", "nl", "en", "eo", "et", "tl", "fi", "fr", "fy", "gl", "ka", "de", "el", "gu", "ht", "ha",
                "haw", "iw", "hi", "hmn", "hu", "is", "ig", "id", "ga", "it", "ja", "jw", "kn", "kk", "km", "ko", "ku", "ky",
                "lo", "la", "lv", "lt", "lb", "mk", "mg", "ms", "ml", "mt", "mi", "mr", "mn", "my", "ne", "no", "ps", "fa",
                "pl", "pt", "ma", "ro", "ru", "sm", "gd", "sr", "st", "sn", "sd", "si", "sk", "sl", "so", "es", "su", "sw",
                "sv", "tg", "ta", "te", "th", "tr", "uk", "ur", "uz", "vi", "cy", "xh", "yi", "yo", "zu"]

deepl_lang_dict = {'de':'DE', 'en':'EN', 'fr':'FR', 'es':'ES', 'pt':'PT', 'it':'IT', 'nl':'NL', 'pl':'PL', 'ru':'RU', 'ja':'JA', 'zh-CN':'ZH'}

class Translator:

    def __init__(self, to_lang):
        self.gtranslator = google_translator()
        self.to_lang = to_lang # aka lang_dest

    # Parse <language_code>:<message>
    def specified_lang(self, msg):
        m = msg.split(':')
        if len(m) >= 2:
            if m[0] in TargetLangs:
                self.to_lang = m[0]
                msg = ':'.join(m[1:])
        return msg

    # Filter out Emotes
    def handle_emotes(self, message_obj):
        emote_list = []
        if message_obj.tags:
            if message_obj.tags['emotes']:
                sent_emotes = message_obj.tags['emotes'].split('/')
                for emote in sent_emotes:
                    e_id, e_pos = emote.split(':')
                    print(f'** e_pos: {e_pos} **')
                    if ',' in e_pos:
                        ed_pos = e_pos.split(',')
                        for e in ed_pos:
                            print(f'** {e} **')
                            print(e.split('-'))
                            e_s, e_e = e.split('-')
                            print(message_obj.content[int(e_s):int(e_e)+1])
                            emote_list.append(
                                message_obj.content[int(e_s):int(e_e)+1]
                            )
                    else:
                        e = e_pos
                        e_s, e_e = e.split('-')
                        emote_list.append(
                            message_obj.content[int(e_s):int(e_e)+1]
                        )
                print(f'** message with emote: {message_obj.content} **')
                for w in sorted(emote_list, key=len, reverse=True):
                    print(w)
                    message = message_obj.content.replace(w, '')
                print(f'** message without emote: {message}')
                return message
        return message_obj.content

    # Use Google Translate for detection
    # Index 0 is the two-character language ID
    # e.g. ['en', 'english']
    def detect_language(self, text):
        try:
            detected_language = self.gtranslator.detect(text)[0]
            print(f'** [Translator::detect_language] Detectect language {detected_language}')
        except Exception as e:
            print(f'** [Translator::detect_language] Error detecting language of text {text}')
        return detected_language

    # Leverage Deepl, GT for translation
    def translate(self, msg, detected_language):
        translated_text = ''
        try:
            if detected_language in deepl_lang_dict.keys() and self.to_lang in deepl_lang_dict.keys():
            # deepl doesn't seem to translate non-english to japanese, for example es => ja
                translated_text = deepl.translate(
                    source_language=deepl_lang_dict[detected_language],
                    target_language=deepl_lang_dict[self.to_lang],
                    text=msg
                )
                print(f'** [Translator::translate DeepL Translate]({deepl_lang_dict[detected_language]} > {deepl_lang_dict[self.to_lang]})')
            else:
                translated_text = self.gtranslator.translate(msg, self.to_lang)
                print(f'** [Translator::translate Google Translate]({detected_language} > {self.to_lang})')
        except Exception as e:
            print(e)
        return translated_text

    # Format outgoing translation
    def format_message(self, user, detected_language, translated_text):
        return '{}: [{}] {}'.format(user, detected_language.upper(), translated_text)

    def process(self, message_obj):
        # Handle Emotes first
        message = self.handle_emotes(message_obj)
        # Filter out emote only messages
        if message == '':
            return

        # Detect Language
        detected_language = self.detect_language(message)
        # If detected language is EN, set destination to JA and vice versa
        if detected_language == 'en':
            self.to_lang = 'ja'
        elif detected_language == 'ja':
            self.to_lang = 'en'
        else:
            self.to_lang # ? Might come back to bite me

        # Parse a specified language
        self.specified_lang(message)

        # Call on DeepL or Google Translate for translation
        translated_text = self.translate(message, detected_language)

        # Format Translation
        user = message_obj.author.name.lower()
        outgoing_text = self.format_message(user, detected_language, translated_text)

        # Send to Bot
        return outgoing_text, detected_language