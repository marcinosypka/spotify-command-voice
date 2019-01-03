import csv
from collections import defaultdict
from collections import Counter
import re
import requests
import json
import itertools

from wordnet.wordnet_api import get_word_senses, get_synsets_for_senses, get_synonyms


class Normalizer:

    def __init__(self, filename):
        self._numerals = {}
        with open(filename) as file:
            for line in file:
                forms = line.split(";")
                self._numerals[forms[1]] = forms[0]
        print("Normalizer created.")

    def normalize_sentence(self, text):
        return " ".join([self._numerals.get(x, x) for x in text.split()])


def send_request(content):
    headers = {'Content-type': 'application/json'}
    url = 'http://localhost:9200/'
    return requests.post(url, data=content.encode('utf-8'), headers=headers)


def normalize_sentence(occurrence):
    content = send_request(occurrence).content.decode("utf-8")
    tokens = [token.split('\t') for token in content.split('\n')]
    tokens = [token_list for token_list in tokens if len(token_list) > 1]
    return " ".join([token[1] for token in tokens[1::2]]).strip()


def extract_answers(row, row_number):
    terms = [term.lower().strip() for term in row[row_number].split(',') if term.strip()]
    return [" ".join(re.findall(r"[\w']+", term)) for term in terms]


def get_synonyms_for_words(word):
    word_dict = {word: i for i in range(1, 3)}
    target_synsets = set()
    for key, value in word_dict.items():
        sense = get_word_senses(key, senseNumber=value)
        synset = get_synsets_for_senses(sense)
        target_synsets = target_synsets.union(set(synset))

    return get_synonyms(target_synsets)


if __name__ == '__main__':
    # reading from CSV and tokenizing
    with open('survey_data.csv', encoding='utf8') as csvfile:
        reader = csv.reader(csvfile, delimiter=',')
        functions = defaultdict(list)
        lematised_functions = defaultdict(list)
        next(reader)
        for row in reader:
            functions['stop'].extend(extract_answers(row, 1))
            functions['start'].extend(extract_answers(row, 2))
            functions['back'].extend(extract_answers(row, 3))
            functions['next'].extend(extract_answers(row, 4))
            functions['loop'].extend(extract_answers(row, 5))
            functions['shuffle'].extend(extract_answers(row, 6))
            functions['jump'].extend(extract_answers(row, 7))
            functions['volume'].extend(extract_answers(row, 8))

        for key, value in functions.items():
            print('-----------------------------------------------------')
            print(key.upper())
            occurrences = sorted(Counter(value).items(), key=lambda x: x[1], reverse=True)
            print(occurrences)
            options = list()
            lematised_options = list()
            for occ, _ in occurrences:
                lematised = normalize_sentence(occ)
                # we remember both original and lematised version
                options.append(occ)
                options.append(lematised)
                lematised_options.append(lematised)
            functions[key] = options
            lematised_functions[key] = lematised_options
            print(lematised_options)

    # storing lematised data
    with open('lematised_results.json', 'w') as fp:
        json.dump(lematised_functions, fp)
    with open('results.json', 'w') as fp:
        json.dump(functions, fp)


    # finding synonyms in wordnet
    print('-----------------------------------------------------------')
    with open('lematised_results.json', 'r') as fp:
        lematised_functions_dict = json.loads(fp.read())

    with open('results.json', 'r') as fp:
        functions_dict = json.loads(fp.read())
        for key, value in functions_dict.items():
            functions_dict[key] = set(value)

    all_phrases = {}
    for key, values in lematised_functions_dict.items():
        print('------------------------------------------')
        print(key.upper())
        print(values)
        all_phrases[key] = set()
        for value in values:
            t = value.split(' ')
            if len(t) > 2:
                continue
            elif len(t) == 2:
                try:
                    first = get_synonyms_for_words(t[0])
                    first.append(t[0])
                    second = get_synonyms_for_words(t[1])
                    second.append(t[1])
                    pairs = list(itertools.product(first, second))
                    pairs = {" ".join(pair) for pair in pairs}
                    all_phrases[key].update(pairs)
                except KeyError:
                    pass
            elif len(t) == 1:
                try:
                    first = get_synonyms_for_words(t[0])
                    all_phrases[key].update(first)
                except KeyError:
                    pass
        all_phrases[key].update(functions_dict[key])
        print(all_phrases[key])

    with open('updated_results.txt', 'w', encoding='utf8') as f:
        for key, items in all_phrases.items():
            f.write("%s\n" % key.upper())
            for item in items:
                f.write("%s\n" % item)



