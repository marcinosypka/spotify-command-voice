import re

from data.data_utils import lematise_sentence
from data.manual_data import get_updated_data


def create_regex_from_data(filename):
    all_phrases = get_updated_data(filename)
    commands_set = set()
    pattern = ''
    for key, phrases in all_phrases.items():
        group_pattern = r'(?P<'
        group_pattern += key + '>'
        commands_set.add(key)
        for phrase in phrases:
            group_pattern += phrase + '|'
        group_pattern = group_pattern[:-1]
        group_pattern += ')'
        pattern += group_pattern + '|'

    pattern = pattern[:-1]
    return re.compile(pattern, re.IGNORECASE), commands_set


def get_commands(sentence, filename):
    compiled_pattern, commands = create_regex_from_data(filename)
    result_commands = []
    for match in compiled_pattern.finditer(lematise_sentence(sentence)):
        for command in commands:
            if match.group(command):
                result_commands.append(command)
    return result_commands


if __name__ == '__main__':
    print(get_commands(r'wróć, daj następny, stop', 'updated_results_manual.txt'))
