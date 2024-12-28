import random
import pymorphy3

from rest_framework.serializers import ValidationError

from .words import ADJECTIVES, HEROES, NOUNS


morph = pymorphy3.MorphAnalyzer()


class Word:
    def __init__(self, word):
        self.word = word
        self.best_parse = morph.parse(self.word)[0]
        self.gender = self.best_parse.tag.gender

    def get_case(self):
        for word in self.best_parse.lexeme:
            if self.word == word.word:
                return word.tag.case

    def get_number(self):
        return self.best_parse.tag.number

    def get_gender(self):
        return self.best_parse.tag.gender

    def set_case_gender_and_number(self, case, gender, number='sing'):
        if self.best_parse.tag.POS == 'NOUN':
            gender = self.get_gender()
        for lexeme in self.best_parse.lexeme:
            if all([
                lexeme.tag.case == case,
                lexeme.tag.number == number,
                lexeme.tag.gender == gender,
                'превосх' not in lexeme.tag.cyr_repr,
            ]):
                self.word = lexeme.word

    def __str__(self):
        return self.word


NUMBER = ['sing', 'plur']
CASES = ['nomn', 'gent', 'datv', 'accs', 'ablt', 'loct']
GENDER = ['masc', 'femn', 'neut']


def clean_data(data) -> list:
    clean_data = []
    for words in data:
        if len(words) == 1:
            clean_data.append(words[0])
        if len(words) != 1:
            key = random.randrange(len(words))
            clean_data.append(words[key])
    for word in clean_data:
        if word['value'] == '':
            if word['type'] == 'which':
                word['value'] = random.choice(ADJECTIVES)
            elif word['type'] == 'what':
                word['value'] = random.choice(NOUNS)
            elif word['type'] == 'whose':
                word['value'] = random.choice(HEROES)
            else:
                raise ValidationError('Invalid type')
    return clean_data


def generate(data) -> str:
    flag = False
    for word in data:
        if word['type'] == 'what':
            main_word = word['value']
            flag = True
            break
        elif word['type'] == 'whose':
            main_word = word['value']
            flag = True
    if not flag:
        main_word = data[0]['value']
    main_word = Word(main_word)
    result = ''
    for word in data:
        if word['value'] != main_word:
            not_main = Word(word['value'])
            case = 'nomn'
            if word['type'] == 'whose' or (
                    word['type'] == 'what' and word['value'] != main_word.word
            ):
                case = 'gent'
            not_main.set_case_gender_and_number(
                case,
                main_word.get_gender(),
                main_word.get_number()
            )
            result += f'{not_main} '
        else:
            result += f'{main_word} '
    return result
