import json
import argostranslate.package, argostranslate.translate
from argostranslate import translate
import os
import re
import urllib.request
import time
import sys

def get_argos_model(source, target):
    lang = f'{source} -> {target}'
    source_lang = [model for model in translate.get_installed_languages() if lang in map(repr, model.translations_from)]
    target_lang = [model for model in translate.get_installed_languages() if lang in map(repr, model.translations_to)]
    
    return source_lang[0].get_translation(target_lang[0])

def get_remaining_time(speed, quote_count, forinfrom, count):
    remaining = (forinto - forinfrom) / speed
    if remaining > 3600:
        return f'{int(round(remaining, 2) / 3600)} hours'
    elif remaining > 60:
        return f'{int(round(remaining, 2) / 60)} minutes'
    else:
        return f'{int(round(remaining, 2))} seconds'

lang = 'nl'
start_time = time.time()
# get quote from JSON file and translate it
with open("main.json", "r") as quotes_file:
    quotes = json.load(quotes_file)
    #gets all the quotes from the JSON file and counts how many there are
    quote_count = len(quotes)
    print(f'Loaded {quote_count} quotes')
    forinfrom = int(sys.argv[1])
    forinto = int(sys.argv[2])
    if os.path.exists(f"file_{lang}.json"):
        print("File already exists")
    else:
        print("The file does not exist, generating new file")
    # Add [ to the file and remove all of it contents
    if forinfrom == 0:
        with open(f"file_{lang}.json", 'w', encoding='utf-8') as f:
            f.write("[")
            f.close()

    count = 0
    for quote in quotes:
        if count < forinfrom:
            count += 1
            continue
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
            speed = (forinfrom - forinto) / (start_time - time.time())
            remaining_time = get_remaining_time(speed, quote_count, forinfrom, count)
            print(f'{count} of {quote_count} quotes translated, {round(speed, 3)} quotes/s, {remaining_time} remaining')
        if count == forinto:
            print(f'Done. Onto the next batch!')
            count += 1
            break
    print("Done with translating quotes. Now reformatting the file")

#Opens the json file and removes the whole quote and author if unkown characters are found
if forinto == 5000:
    with open(f"file_{lang}.json", 'rb+') as filehandle:
        filehandle.seek(-1, os.SEEK_END)
        filehandle.truncate()
        filehandle.write(']'.encode('utf-8'))
        filehandle.close()
    obj  = json.load(open(f"file_{lang}.json"))
    last_start_time = time.time()
    with open(f"file_{lang}.json", "r") as quotes_file:
        quotes = json.load(quotes_file)
        num = 0
        for quote in quotes:
            for idx, obj in enumerate(quotes):
                import re
                def corr(s):
                    sub = re.sub(r'\.(?! )', '. ', re.sub(r' +', ' ', s))
                    return sub

                num += 1
                speed = count / (last_start_time - time.time())  * -1
                remaining_time = get_remaining_time(speed, quote_count, count)
                print(f'{num} of {quote_count} quotes translated, {round(speed, 3)} quotes/s, {remaining_time} remaining')
                obj['quote'] = corr(obj['quote'])
                if '\u00ef\u00bf\u00bd' in obj['quote']:
                    quotes.pop(idx)
                    print("Removed quote")

    with open(f"file_{lang}.json", 'w', encoding='utf-8') as f:
        f.write(json.dumps(quotes, indent=2))
        f.close()
        print("Done with reformatting the file")
