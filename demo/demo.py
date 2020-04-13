import re
import sys
from collections import OrderedDict
TEST_EXAMPLES = ['The pump is 536 deep underground.', 'The database has 66723107008 records.']

#TEST_EXAMPLES.extend(['I received 23 456,9 KGs',
#                 'Variables reported as having a missing type #65678']) #TODO Come back to these cases

PATTERN = re.compile('[0-9]+')
UNITS = (10, 10*10, 10*10*10, 10*10*10*10*10*10, 10*10*10*10*10*10*10*10*10)[::-1]
UNIT_EQUIVALENT = ('ten', 'hundred', 'thousand', 'million', 'billion')[::-1]
UNIT_DICT = OrderedDict((x,y) for (x, y) in zip(UNITS, UNIT_EQUIVALENT))

def extract_numbers_from_sentence(sentence_string):
    '''
    :param sentence_string: Full Sentence
    :return: list of matches
    '''
    return [int(x) for x in PATTERN.findall(sentence_string)]

def split_into_relevant_units(number):
    '''
    :param number: int
    :return: dictionary of units
    '''
    split_units_dict = OrderedDict()
    if number == 0:
        return split_units_dict
    for k, v in UNIT_DICT.items():
        modulo = number % k
        if modulo:
            split_units_dict[v] = number
        continue
    return split_units_dict

def compile_into_words(unit_dict):
    '''
    :param unit_dict: key,value pair of units
    :return: completed string
    '''
    pass

def main():
    #with open('number_snippets.txt') as file:
        #for line in file.readlines():
        for line in TEST_EXAMPLES:
            prepend = ''
            number = extract_numbers_from_sentence(line)[0]
            if number < 0:
                prepend = 'minus'
            unit_split = split_into_relevant_units(number)
            if not unit_split:
                prepend = 'zero'
            complete_sentence = compile_into_words(unit_split)
            sys.stdout(prepend + ' ' + complete_sentence)

if __name__== '__main__':
    main()
