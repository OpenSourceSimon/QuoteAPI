import json
import os
import re
import sys
import time
import urllib.request

import argostranslate.package
import argostranslate.translate
from argostranslate import translate


def get_argos_model(source, target):
    lang = f'{source} -> {target}'
    source_lang = [model for model in translate.get_installed_languages() if lang in map(repr, model.translations_from)]
    target_lang = [model for model in translate.get_installed_languages() if lang in map(repr, model.translations_to)]

    return source_lang[0].get_translation(target_lang[0])


def get_remaining_time(speed, forinto, forinfrom, count):
    remaining = (forinto - count) / speed
    if remaining > 3600:
        return f'{int(round(remaining, 2) / 3600)} hours'
    elif remaining > 60:
        return f'{int(round(remaining, 2) / 60)} minutes'
    else:
        return f'{int(round(remaining, 2))} seconds'


start_time = time.time()

with open("main.json", "r") as quotes_file:
    quotes = json.load(quotes_file)
    # Gets all the quotes from the JSON file and counts how many there are
    quote_count = len(quotes)
    print(f'Loaded {quote_count} quotes')
    forinfrom = int(sys.argv[1])
    forinto = int(sys.argv[2])
    lang = sys.argv[3]
    argosmodels = {"ar": "translate-en_ar-1_0.argosmodel", "az": "translate-en_az-1_5.argosmodel",
                   "cs": "translate-en_cs-1_5.argosmodel", "da": "translate-en_da-1_3.argosmodel",
                   "de": "translate-en_de-1_0.argosmodel", "el": "translate-en_el-1_5.argosmodel",
                   "eo": "translate-en_eo-1_5.argosmodel", "es": "translate-en_es-1_0.argosmodel",
                   "fa": "translate-en_fa-1_5.argosmodel", "fi": "translate-en_fi-1_5.argosmodel",
                   "fr": "translate-en_fr-1_0.argosmodel", "ga": "translate-en_ga-1_1.argosmodel",
                   "he": "translate-en_he-1_5.argosmodel", "hi": "translate-en_hi-1_1.argosmodel",
                   "hu": "translate-en_hu-1_5.argosmodel", "id": "translate-en_id-1_2.argosmodel",
                   "it": "translate-en_it-1_0.argosmodel", "ja": "translate-en_ja-1_1.argosmodel",
                   "ko": "translate-en_ko-1_1.argosmodel", "nl": "translate-en_nl-1_4.argosmodel",
                   "pl": "translate-en_pl-1_1.argosmodel", "pt": "translate-en_pt-1_0.argosmodel",
                   "ru": "translate-en_ru-1_7.argosmodel", "sk": "translate-en_sk-1_5.argosmodel",
                   "sv": "translate-en_sv-1_5.argosmodel", "tr": "translate-en_tr-1_5.argosmodel",
                   "uk": "translate-en_uk-1_4.argosmodel", "zh": "translate-en_zh-1_1.argosmodel"}
    path = argosmodels[lang]
    getmodel = {"ar": "Arabic", "az": "Azerbaijani", "cs": "Czech", "da": "Danish", "de": "German", "el": "Greek",
                "eo": "Esperanto", "es": "Spanish", "fa": "Persian", "fi": "Finnish", "fr": "French", "ga": "Irish",
                "he": "Hebrew", "hi": "Hindi", "hu": "Hungarian", "id": "Indonesian", "it": "Italian", "ja": "Japanese",
                "ko": "Korean", "nl": "Dutch", "pl": "Polish", "pt": "Portuguese", "ru": "Russian", "sk": "Slovak",
                "sv": "Swedish", "tr": "Turkish", "uk": "Ukrainian", "zh": "Chinese"}
    if os.path.exists(f"file_{lang}.json"):
        print("File already exists")
    else:
        print("The file does not exist, generating new file")


    def translation():
        urllib.request.urlretrieve(f'https://simonrijntjes.nl/argosmodel/{path}', path)
        count = 0
        for quote in quotes:
            if count < forinfrom:
                count += 1
                continue
            # Download the model
            download_path = path
            argostranslate.package.install_from_path(download_path)
            argos = get_argos_model('English', getmodel[lang])
            translation = argos.translate(quote['quote'])
            # save the translation in a new JSON file
            with open(f"file_{lang}.json", "a", encoding='utf-8') as f:
                if count == quote_count - 1:
                    text = translation.encode('utf-8')
                    final = text.decode('utf-8')
                    f.write(f'{{"quote": "{final}", "author": "{quote["author"]}"}}]')
                    f.close()
                    print(f'Finished translating {quote_count} quotes')
                    count += 1
                    break
                else:
                    text = translation.encode('utf-8')
                    final = text.decode('utf-8')
                    f.write(f'{{"quote": "{final}", "author": "{quote["author"]}"}},')
                    f.close()
                    count += 1
                    speed = (forinfrom - count) / (start_time - time.time())
                    remaining_time = get_remaining_time(speed, forinto, forinfrom, count)
                    print(
                        f'{count} of {quote_count} quotes translated. {round(speed, 2)} quotes per second. {remaining_time} remaining')

    if forinfrom == 0:
        with open(f"file_{lang}.json", 'w', encoding='utf-8') as f:
            f.write("[")
            f.close()
            translation()
    else:
        translation()

    # Opens the json file and removes the whole quote and author if unkown characters are found
    if forinto == 5000:
        print("Now reformatting the file")
        obj = json.load(open(f"file_{lang}.json"))
        last_start_time = time.time()
        with open(f"file_{lang}.json", "r") as quotes_file:
            quotes = json.load(quotes_file)
            num = 0
            for quote in quotes:
                for idx, obj in enumerate(quotes):
                    def corr(s):
                        sub = re.sub(r'\.(?! )', '. ', re.sub(r' +', ' ', s))
                        return sub


                    num += 1
                    speed = num / (last_start_time - time.time()) * -1
                    print(f'{num} of {quote_count} quotes reformated, {round(speed, 3)} quotes/s')
                    obj['quote'] = corr(obj['quote'])
                    if '\u00ef\u00bf\u00bd' in obj['quote'] or '\u00ef\u00bf\u00bd' in obj['author'] or 'Ã«' in obj[
                        'quote']:
                        quotes.pop(idx)
                        print("Removed quote")

        with open(f"file_{lang}.json", 'w', encoding='utf-8') as f:
            f.write(json.dumps(quotes, indent=2))
            f.close()
            print("Done with reformatting the file")
