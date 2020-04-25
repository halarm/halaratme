import re
import sys
TEST_EXAMPLES = ['The pump is 536 deep underground.', 'The database has 66723107008 records.']

#TEST_EXAMPLES.extend(['I received 23 456,9 KGs',
#                 'Variables reported as having a missing type #65678']) #TODO Come back to these cases

PATTERN = re.compile('[0-9]+')
INCREMENTS = (10, 100, 1000, 1000000, 1000000000)
INCREMENT_EQUIVALENT = ('ten', 'hundred', 'thousand', 'million', 'billion')
INCREMENT_DICT = dict((x,y) for (x, y) in zip(INCREMENTS, INCREMENT_EQUIVALENT))

units = ['','one','two','three','four','five','six','seven','eight','nine']

tens = ['', 'eleven', 'twelve', 'thirteen', 'fourteen', 'fifteen']
#tens.extend(['{unit}teen'.format(unit=unit) for unit in units[6:]])
#for i in units:
    #tens.extend(['{unit}nty-{unit}'].format(unit=unit) for unit in units[2:]])

def compress_units(unit_dict):
    '''
    :param unit_dict:
    :return: compressed dict
    '''
    compressed_dict = {1: unit_dict[1]}
    for increment, word_equivalent in INCREMENT_DICT.values():
        if increment > list(unit_dict.keys())[-1]:
            break
        else:
            increment_grouping = unit_dict.get(increment, 0)
            _increment = increment*10
            while _increment not in INCREMENTS and _increment <= list(unit_dict.keys())[-1]:
                increment_grouping+=unit_dict.get(_increment, 0)
                _increment = _increment*10
        compressed_dict[word_equivalent] = increment_grouping/increment
    return compressed_dict

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
    :param original_number:
    :return: dict {unit: digit}
    '''
    divisor = 10
    split_units_dict = {1: 0}
    while number:
        remainder = divmod(number, divisor)[-1]
        split_units_dict[divisor/10] = remainder
        number = number - remainder
        divisor = divisor*10
    return split_units_dict

def compile_into_words(unit_dict):
    '''
    :param unit_dict: key,value pair of units
    :return: completed string
    '''
    compressed_units = compress_units(unit_dict)


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
                complete_sentence = compile_into_words(unit_split)
                sentence_output.append(prepend + ' ' + complete_sentence)
                output.append(complete_sentence)
        print(output)

if __name__== '__main__':
    main()
