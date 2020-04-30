import re
import sys
import copy
import argparse
TEST_EXAMPLES = ['0', 'The pump is 536 deep underground.', 'The database has 66723107008 records.', 'I received 23 456,9 KGs',  'Variables reported as having a missing type #65678']

INCREMENTS = [1, 10, 100, 1000, 1000000, 1000000000]
INCREMENT_EQUIVALENT = ['one', 'ten', 'hundred', 'thousand', 'million', 'billion']
INCREMENT_DICT = dict((x,y) for (x, y) in zip(INCREMENTS, INCREMENT_EQUIVALENT))
units = ['zero','one','two','three','four','five','six','seven','eight','nine', 'ten']
non_conforming_words = ['eleven', 'twelve',]
teens_prepend = ['twen', 'thir', 'four', 'fif', 'six', 'seven', 'eigh', 'nine']


override_dict = {
    1: units[1],
    2: units[2],
    3: units[3],
    4: units[4],
    5: units[5],
    6: units[6],
    7: units[7],
    8: units[8],
    9: units[9],
}

def compress_units(unit_dict):
    '''
    :param unit_dict:
    :return: compressed dict
    '''
    compressed_dict = {}
    for increment, word_equivalent in INCREMENT_DICT.items():
        if increment > list(unit_dict.keys())[-1]:
            break
        else:
            increment_grouping = unit_dict.get(increment, 0)
            _increment = increment*10
            while _increment not in INCREMENTS and _increment <= list(unit_dict.keys())[-1]:
                increment_grouping+=unit_dict.get(_increment, 0)
                _increment = _increment*10
        compressed_dict[word_equivalent] = int(increment_grouping/increment)
    return compressed_dict

def construct_number(number):
    return override_dict.get(number, '')

def handle_tens_and_units(constructed_string, number):
    tens, ones = divmod(number, 10)
    if tens == 1 and not ones:
        return 'ten'
    elif tens == 1 and 0 < ones <=2:
        return non_conforming_words[ones-1]
    elif tens == 1 and 2 < ones <=9:
        return teens_prepend[1:][ones-3] + 'teen'
    elif tens > 1 and not ones:
        return constructed_string % teens_prepend[tens-2]
    else:
        return constructed_string % (teens_prepend[tens-2], override_dict[ones])

def compressed_dict_to_words(grouped_dict, sentence=''):
    '''
    :param grouped_dict:
    :return: string number
    '''
    ten_ones_handle = '%sty-%s' if 'one' and 'ten' in grouped_dict else '%sty'
    for increment in INCREMENT_EQUIVALENT[::-1]:
        number = grouped_dict.pop(increment) if increment in grouped_dict else 0
        number_sentence = construct_number(number)
        if not number:
            continue
        elif number and not number_sentence and increment != 'ten':
            sentence = compressed_dict_to_words(split_into_relevant_units_and_compress(number), sentence)  + ' ' + increment
        else:
            if increment == 'ten':
                if 'one' in grouped_dict:
                    number = number*10 + grouped_dict.pop('one')
                append = handle_tens_and_units(ten_ones_handle, number)
                number_sentence = ''
            elif increment == 'one':
                append = ''
            else:
                append = ' ' + increment
            splitter = ', ' if grouped_dict else ' and '
            if not sentence:  # Beginning
                prepend = ''
            else:
                prepend = sentence + splitter
            sentence =  prepend + number_sentence + append
    return sentence

def extract_numbers_from_sentence(sentence_string):
    '''
    :param sentence_string: Full Sentence
    :return: list of matches
    '''
    special_character_find = re.compile("[$&+,:;=?@#|'<>.^*()%!-]+").findall(sentence_string)
    special_character_positions = [sentence_string.index(s) for s in special_character_find]
    number_find = re.compile('[0-9]+').findall(sentence_string)
    number_positions = [sentence_string.index(n) for n in number_find]
    for number_position in number_positions:
        if number_position+1 in special_character_positions or number_position-1 in special_character_positions:
            return[]
    return [int(x) for x in number_find]

def split_into_relevant_units_and_compress(number):
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
    return compress_units(split_units_dict)

def main(txt_file):
    output = []
    with open(txt_file) as file:
        for line in file.readlines():

            sentence_output = []
            prepend = ''
            parsed_numbers = extract_numbers_from_sentence(line)
            if parsed_numbers:
                for parsed_number in parsed_numbers:
                    if parsed_number < 0:
                        prepend = 'minus '
                        parsed_number = parsed_number*-1
                    unit_split = split_into_relevant_units_and_compress(parsed_number)
                    complete_sentence = compressed_dict_to_words(unit_split) if parsed_number else 'zero'
                    output.append(prepend + complete_sentence)
            else:
                output.append('number invalid')
        print(output)

number_parser = argparse.ArgumentParser(description='Convert numbers in a sentence to string')
number_parser.add_argument('txt_file', type=str, help='Text file to read')
args = number_parser.parse_args()

if __name__== '__main__':
    main(args.txt_file)