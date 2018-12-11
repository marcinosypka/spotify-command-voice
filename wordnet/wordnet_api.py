
import requests
import json

headers = {'Content-type': 'application/json'}


def get_word_senses(word, partOfSpeech=None, senseNumber=None):
    word_id = get_word_id(word)
    url = 'http://api.slowosiec.clarin-pl.eu:80/plwordnet-api/senses/search?lemma=' + word
    if partOfSpeech:
        url += '&&&partOfSpeech=' + partOfSpeech + '&&&&&&'
    else:
        url += '&&&&&&&&&'
    r = requests.get(url, headers=headers)
    r = json.loads(r.text)
    senses = [sense['id'] for sense in r['content'] if sense['lemma']['id'] == word_id]
    if senseNumber:
        senses = [sense['id'] for sense in r['content'] if
                  sense['lemma']['id'] == word_id and sense['senseNumber'] == senseNumber]
    return senses


def get_word_id(word):
    url = 'http://api.slowosiec.clarin-pl.eu:80/plwordnet-api/words/search?lemma=' + word
    r = requests.get(url, headers=headers)
    r = json.loads(r.text)
    return r[0]['id']


def get_synsets_for_senses(senses):
    synsets = []
    for sense in senses:
        url = 'http://api.slowosiec.clarin-pl.eu:80/plwordnet-api/senses/' + str(sense) + '/synset'
        r = requests.get(url, headers=headers)
        r = json.loads(r.text)
        synsets.append(r['id'])
    return synsets


def get_synsets_explanations(synsets):
    explanations = []
    for synset in synsets:
        url = 'http://api.slowosiec.clarin-pl.eu:80/plwordnet-api/synsets/' + str(synset) + '/attributes'
        r = requests.get(url, headers=headers)
        r = json.loads(r.text)
        for attr in r:
            if attr['type']['typeName'] in {'definition'}:
                explanations.append(attr['value'])
    return explanations


def get_synonyms(synsets):
    synonyms = []
    for synset in synsets:
        url = 'http://api.slowosiec.clarin-pl.eu:80/plwordnet-api/synsets/' + str(synset) + '/senses'
        r = requests.get(url, headers=headers)
        r = json.loads(r.text)
        for attr in r:
            synonyms.append(attr['lemma']['word'])
    return synonyms


def get_realtions_to(synset, relation='hiperonimia'):
    relations = []
    url = 'http://api.slowosiec.clarin-pl.eu:80/plwordnet-api/synsets/' + str(synset) + '/relations/to'
    r = requests.get(url, headers=headers)
    r = json.loads(r.text)
    for rel in r:
        if rel['relation']['name'] == relation:
            relations.append(rel['synsetFrom']['id'])
    return relations


def get_synset_core(synset):
    url = 'http://api.slowosiec.clarin-pl.eu:80/plwordnet-api/synsets/' + str(synset) + '/core'
    r = requests.get(url, headers=headers)
    r = json.loads(r.text)
    return r['lemma']['word'] + ':' + str(r['senseNumber'])


def get_neighbours(synset):
    neighbours = []
    url = 'http://api.slowosiec.clarin-pl.eu:80/plwordnet-api/synsets/' + str(synset) + '/relations'
    r = requests.get(url, headers=headers)
    r = json.loads(r.text)
    for rel in r:
        if rel['synsetFrom']['id'] == synset:
            neighbours.append(rel['synsetTo']['id'])
    return neighbours


def get_neighbours_2(synset):
    neighbours = set()
    url = 'http://api.slowosiec.clarin-pl.eu:80/plwordnet-api/synsets/' + str(synset) + '/relations'
    r = requests.get(url, headers=headers)
    r = json.loads(r.text)
    for rel in r:
        try:
            if rel['synsetFrom']['id'] == synset:
                neighbours.add(rel['synsetTo']['id'])
            if rel['synsetTo']['id'] == synset:
                neighbours.add(rel['synsetFrom']['id'])
        except TypeError:
            continue
    return neighbours


def get_relation(parent, synset):
    url = 'http://api.slowosiec.clarin-pl.eu:80/plwordnet-api/synsets/' + str(parent) + '/relations'
    r = requests.get(url, headers=headers)
    r = json.loads(r.text)
    for rel in r:
        if rel['synsetTo']['id'] == synset:
            return rel['relation']['name']
