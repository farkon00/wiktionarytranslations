#!/usr/bin/env python3

import requests
import gzip
import os

def clear():
    if os.name == 'nt':
        os.system('cls')
    else:
        os.system('clear')

if __name__ == '__main__':
    url = 'https://en.wiktionary.org/w/api.php?action=parse&'

    headers = {
        'User-Agent': 'WiktionaryTranslations/1.0 (https://github.com/morrigan-plus-plus/wiktionarytranslations/;r.chapple.business@gmail.com)',
        'Accept-Encoding': 'gzip'
        }
    clear()
    print("Wiktionary Translations v1.0 [https://github.com/morrigan-plus-plus/wiktionarytranslations]")

    print("[INFO] Wiktionary titles are case-sensitive.")
    title = input("Please enter the word you wish to get the translation(s) of: ")

    # TODO: Verify valid word and/or convert to Wiktionary URL format

    res = requests.get(url + 'page=' + title + '&prop=wikitext&format=json&formatversion=2')

    if res.status_code != 200:
        print(f"Error contacting the Wiktionary API. Status Code: {res.status_code}.")
        exit(1)

    res_json = res.json()

    if 'error' in res_json.keys():
        error = res_json['error']
        print(error['info'] + ": " + error['code'])
        print("[INFO] Ensure the capitalization of your search term is correct and try again.")
        exit(1)

    if 'parse' not in res_json.keys():
        print("Unknown error.")
        exit(1)

    wiki_text = res_json['parse']['wikitext']
    title = res_json['parse']['title']

    clear()
    print(f"Success! The page {title} was found!")
    success = False
    while not success:
        print("[INFO] For a full list of language codes, see https://en.wikipedia.org/wiki/List_of_ISO_639-1_codes")
        lang = input("Please enter the 2 letter language code (e.g. fi, ko, de) you wish to translate to: ")
        if len(lang) != 2:
            clear()
            print(f"[ERROR] {lang} is not a valid language code.")
        else:
            success = True

    trans_tops = []

    for line in wiki_text.splitlines():
        if '{{trans-top' in line:
            trans_tops.append(line.split('|')[1][:-2])
    clear()
    if (len(trans_tops) == 0):
        print("Unfortunately, this page contains no translations.")
        exit(1)

    if (len(trans_tops) == 1):
        print(f"1 definition found to translate. Defaulting to `{trans_tops[0]}`.")
    else:
        print(f"{len(trans_tops)} definitions found to translate: ")

        i = 0
        for trans_top in trans_tops:
            i += 1
            print(f"- Option {i}: {trans_top}")
