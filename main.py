import json
from googletrans import Translator
import os
import re

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
        translator = Translator()
        translation = translator.translate(quote["quote"], dest=lang).text
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
