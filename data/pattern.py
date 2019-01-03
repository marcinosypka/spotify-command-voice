import re

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
    pattern += r'|(?P<TIME>\d+:\d+)'
    commands_set.add('TIME')

    return re.compile(pattern, re.IGNORECASE), commands_set


def process_result(commands):
    result = []
    for i in range(len(commands) - 1):
        if commands[i][0] == 'JUMP' and commands[i + 1][0] == 'TIME':
            time = commands[i + 1][1][:4]
            if len(time) == 3:
                time = time[:2] + '0' + time[2:]
            result.append((commands[i][0], time))
        elif commands[i][0] == 'JUMP' or commands[i][0] == 'TIME':
            continue
        else:
            result.append((commands[i][0], None))

    return result


def get_commands(sentence, filename, debug=False):
    compiled_pattern, commands = create_regex_from_data(filename)
    result_commands = []

    if debug:
        print(sentence, '\n')
    for match in compiled_pattern.finditer(sentence):
        if debug:
            print(match)
        for command in commands:
            if match.group(command):
                result_commands.append((command, match.group(command)))

    result = process_result(result_commands)
    if debug:
        print('\n', result)

    return result


if __name__ == '__main__':
    print(get_commands(r'wróć, daj następny, stop, przewiń na 2:21', 'updated_results_manual.txt'))
