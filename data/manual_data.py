from collections import defaultdict


def get_updated_data(filename):
    with open(filename, 'r', encoding='utf8') as f:
        lines = f.read().split('\n')
        all_phrases_filtered = defaultdict(set)

        for line in lines:
            line = line.strip()
            if line.split(' ')[0].isupper():
                key = line.replace(" ", "_")
            else:
                all_phrases_filtered[key].add(line)

    return all_phrases_filtered


def store_updated_data(filename, dictionary):
    with open(filename, 'w', encoding='utf8') as f:
        for key, items in dictionary.items():
            f.write("%s\n" % key.upper())
            for item in items:
                f.write("%s\n" % item)


if __name__ == '__main__':
    print(get_updated_data('updated_results_manual.txt'))
