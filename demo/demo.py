import re
import sys
import copy
TEST_EXAMPLES = ['The pump is 536 deep underground.', 'The database has 66723107008 records.', 'I received 23 456,9 KGs',  'Variables reported as having a missing type #65678']

INCREMENTS = [10, 100, 1000, 1000000, 1000000000]
INCREMENT_EQUIVALENT = ['ten', 'hundred', 'thousand', 'million', 'billion']
INCREMENT_DICT = dict((x,y) for (x, y) in zip(INCREMENTS, INCREMENT_EQUIVALENT))
_INCREMENT_EQUIVALENT = copy.copy(INCREMENTS)
_INCREMENT_EQUIVALENT.insert(0, 'one')
units = ['zero','one','two','three','four','five','six','seven','eight','nine', 'ten']

tens = ['eleven', 'twelve', 'thirteen', 'fourteen', 'fifteen']
tens.extend(['{unit}teen'.format(unit=unit) for unit in units[6:-1]])

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
    10: units[10],
    11: tens[0],
    12: tens[1],
    13: tens[2],
    14: tens[3],
    15: tens[4],
    16: tens[5],
    17: tens[6],
    18: tens[7],
    19: tens[8],
}

def compress_units(unit_dict):
    '''
    :param unit_dict:
    :return: compressed dict
    '''
    compressed_dict = {'one': unit_dict[1]}
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
    word = ''
    if number:
        word = override_dict.get(number)
    return word

def compressed_dict_to_words(grouped_dict):
    '''
    :param grouped_dict:
    :return: string number
    '''
    sentence = ''
    for increment in INCREMENT_EQUIVALENT[::-1]:
        number_sentence = construct_number(grouped_dict.pop(increment) if increment in grouped_dict else 0 )
        if not number_sentence:
            continue
        splitter = ', ' if grouped_dict else 'and'
        sentence = sentence + splitter + number_sentence + ' ' + increment
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
    return compressed_dict_to_words(compressed_units)

def main():
    output = []
    with open('number_snippets.txt') as file:
        for line in file.readlines():
            sentence_output = []
            prepend = ''
            parsed_numbers = extract_numbers_from_sentence(line)
            for parsed_number in parsed_numbers:
                if parsed_number < 0:
                    prepend = 'minus'
                    parsed_number = parsed_number*-1
                unit_split = split_into_relevant_units(parsed_number)
                complete_sentence = compile_into_words(unit_split)
                output.append(prepend + ' ' + complete_sentence)
        #sys.stdout(output)
        print(output)

if __name__== '__main__':
    main()
