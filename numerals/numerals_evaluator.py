import re


class NumeralsNormalizer:

    def __init__(self, filename):
        self._numerals = {}
        with open(filename) as file:
            for line in file:
                forms = line.split(";")
                self._numerals[forms[1]] = forms[0]

    def normalize_numerals(self, text):
        return " ".join([self._numerals.get(x, x) for x in text.split()])


class NumeralsTransformer:

    def __init__(self, normalizer):
        units = [
            "zero", "jeden", "dwa", "trzy", "cztery", "pięć", "sześć", "siedem", "osiem",
            "dziewięć", "dziesięć", "jedenaście", "dwanaście", "trzynaście", "czternaście", "piętnaście",
            "szesnaście", "siedemnaście", "osiemnaście", "dziewiętnaście",
        ]

        tens = [
            "", "", "dwadzieścia", "trzydzieści", "czterdzieści", "pięćdziesiąt",
            "sześćdziesiąt", "siedemdziesiąt", "osiemdziesiąt", "dziewięćdziesiąt"
        ]

        hundreds = [
            "", "sto", "dwieście", "trzysta", "czterysta", "pięćset", "sześćset",
            "siedemset", "osiemset", "dziewięćset"
        ]

        scales = ["tysiąc", "milion", "miliard", "bilion", "biliard"]

        self._numwords = {}

        for idx, word in enumerate(units):
            self._numwords[word] = (1, idx)
        for idx, word in enumerate(tens):
            self._numwords[word] = (1, idx * 10)
        for idx, word in enumerate(hundreds):
            self._numwords[word] = (1, idx * 100)
        for idx, word in enumerate(scales):
            self._numwords[word] = (10 ** (idx * 3 + 3), 0)

        self._numerals_set = set(units) | set(tens) | set(hundreds) | set(scales)
        self._normalizer = normalizer

    def _transform_to_number(self, numerals):
        current = result = 0
        for word in numerals:
            if word not in self._numwords:
                raise Exception("Illegal word: " + word)

            scale, increment = self._numwords[word]
            current = current * scale + increment
            if scale > 100:
                result += current
                current = 0

        return result + current

    @staticmethod
    def _handle_floats(text):
        return re.sub(r'(\d+)\s+(przecinek|kropka|koma|dwukropek)\s+(\d+)', r'\1:\3', text)

    def replace_with_numbers(self, text):
        normalized_text = self._normalizer.normalize_numerals(text)
        result = []
        numerals = []
        for word in normalized_text.split():
            if word in self._numerals_set:
                numerals.append(word)
            else:
                if numerals:
                    result.append(self._transform_to_number(numerals))
                result.append(word)
                numerals = []
        if numerals:
            result.append(self._transform_to_number(numerals))
        result = [str(r) for r in result]
        return self._handle_floats(" ".join(result))
