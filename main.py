import json
import argostranslate.package, argostranslate.translate
from argostranslate import translate
import os
import re
import urllib.request

def get_argos_model(source, target):
    lang = f'{source} -> {target}'
    source_lang = [model for model in translate.get_installed_languages() if lang in map(repr, model.translations_from)]
    target_lang = [model for model in translate.get_installed_languages() if lang in map(repr, model.translations_to)]
    
    return source_lang[0].get_translation(target_lang[0])

lang = 'nl'
# get quote from JSON file and translate it
with open("main.json", "r") as quotes_file:
    quotes = json.load(quotes_file)
    if os.path.exists(f"file_{lang}.json"):
        os.remove(f"file_{lang}.json")
    else:
        print("The file does not exist, generating new file")
    # Add [ to the file and remove all of it contents
    with open(f"file_{lang}.json", 'w', encoding='utf-8') as f:
        f.write("[")
        f.close()

    count = 0
    for quote in quotes:
        urllib.request.urlretrieve('https://argosopentech.nyc3.digitaloceanspaces.com/argospm/translate-en_nl-1_4.argosmodel', 'translate-en_nl-1_4.argosmodel')
        download_path = "translate-en_nl-1_4.argosmodel"
        argostranslate.package.install_from_path(download_path)
        argos_ru_en = get_argos_model('English', 'Dutch')
        translation = argos_ru_en.translate(quote['quote'])
        # save the translation in a new JSON file
        with open(f"file_{lang}.json", "a",  encoding="utf-8") as quotes_file:
            f = open(f"file_{lang}.json", "a")
            f.write('{"quote":"' + translation + '",')
            f.write('"author":"' + str(quote['author']) + '"},')
            f.close()
            count += 1
            print(f"Translated {count} quotes")

#Opens the json file and removes the whole quote and author if unkown characters are found
with open(f"file_{lang}.json", 'rb+') as filehandle:
    filehandle.seek(-1, os.SEEK_END)
    filehandle.truncate()
    filehandle.write(']'.encode('utf-8'))
    filehandle.close()
obj  = json.load(open(f"file_{lang}.json"))
with open(f"file_{lang}.json", "r") as quotes_file:
    quotes = json.load(quotes_file)
    for quote in quotes:
        for idx, obj in enumerate(quotes):
            import re
            def corr(s):
                sub = re.sub(r'\.(?! )', '. ', re.sub(r' +', ' ', s))
                print(sub)
                return sub

            obj['quote'] = corr(obj['quote'])
            if '\u00ef\u00bf\u00bd' in obj['quote']:
                quotes.pop(idx)
                print("Removed quote")

with open(f"file_{lang}.json", 'w', encoding='utf-8') as f:
    f.write(json.dumps(quotes, indent=2))

