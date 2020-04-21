import re
import sys
from collections import OrderedDict
TEST_EXAMPLES = ['The pump is 536 deep underground.', 'The database has 66723107008 records.']

#TEST_EXAMPLES.extend(['I received 23 456,9 KGs',
#                 'Variables reported as having a missing type #65678']) #TODO Come back to these cases

PATTERN = re.compile('[0-9]+')
INCREMENTS= (10, 10*10, 10*10*10, 10*10*10*10*10*10, 10*10*10*10*10*10*10*10*10)
INCREMENT_EQUIVALENT = ('ten', 'hundred', 'thousand', 'million', 'billion')
INCREMENT_DICT = OrderedDict((x,y) for (x, y) in zip(INCREMENTS, INCREMENT_EQUIVALENT))

units = ['','one','two','three','four','five','six','seven','eight','nine']

tens = ['', 'eleven', 'twelve', 'thirteen', 'fourteen', 'fifteen']
#tens.extend(['{unit}teen'.format(unit=unit) for unit in units[6:]])
#for i in units:
    #tens.extend(['{unit}nty-{unit}'].format(unit=unit) for unit in units[2:]])





hundreds = []

thousands = []

def num_to_words(num):
    pass













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
    split_units_dict = {1: 'zero'}
    if number == 0:
        return split_units_dict
    for increments_in_ten in INCREMENTS:
        i, d = divmod(number, increments_in_ten)
        if i and not d:
            split_units_dict[increments_in_ten] = i
            number = i
        elif d:
            split_units_dict[increments_in_ten/10] = d
        if not i:
            break
    return split_units_dict

def compile_into_words(unit_dict):
    '''
    :param unit_dict: key,value pair of units
    :return: completed string
    '''
    #for unit, values in unit_dict.items():
        #parse(value)


def main():
    #with open('number_snippets.txt') as file:
        #for line in file.readlines():
        output = []
        for line in TEST_EXAMPLES:
            sentence_output = []
            prepend = ''
            parsed_numbers = extract_numbers_from_sentence(line)
            for parsed_number in parsed_numbers:
                if parsed_number < 0:
                    prepend = 'minus'
                    parsed_number = parsed_number*-1
                unit_split = split_into_relevant_units(parsed_number)
                if not unit_split:
                    prepend = 'zero'
                #complete_sentence = compile_into_words(unit_split)
                #sentence_output.append(prepend + ' ' + complete_sentence)
                output.append(unit_split)
        print(output)

if __name__== '__main__':
    main()
