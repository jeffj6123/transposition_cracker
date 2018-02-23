"""
based off the following
http://homepages.math.uic.edu/~leon/mcs425-s08/handouts/breaking_tranposition_cipher.pdf
"""
import sys
import csv

letter_data = list(csv.reader(open("standard_letter_frequency.txt")))
letter_dict = {}
for letter in letter_data:
    letter_dict[letter[0]] = float(letter[1])
digraph_data = list(csv.reader(open('digraph_scores.csv')))


def get_letter_frequency(letter):
    return letter_dict[letter.upper()]


def letter_to_int(letter):
    letter = letter.lower()
    alphabet = list('abcdefghijklmnopqrstuvwxyz')
    return alphabet.index(letter)


def get_letter_score(letter1, letter2):
    l1 = letter_to_int(letter1)
    l2 = letter_to_int(letter2)
    return float(digraph_data[l1][l2])


def get_and_clean_cypher_text(file_name):
    input_data = ''.join(open(file_name).readlines())
    concatText = ''.join(input_data.strip().split())
    return concatText


def generate_grid_from_text(text, size):
    formatted_input_data = [""] * int(len(text) / size)
    for i in range(len(text)):
        formatted_input_data[i % int(len(text) / size)] += text[i]
    return formatted_input_data


def Main():
    size = int(sys.argv[2])

    file_name = sys.argv[1]

    clean_text = get_and_clean_cypher_text(file_name)

    if len(clean_text) % size != 0:
        sys.exit("invalid length size for square")

    formatted_input_data = generate_grid_from_text(clean_text, size)

    """
    generate a size * size grid where each has a i row, j column referring to a i column j column summation as seen in the
    guide above to generate values.
    """
    sum_matrix = []
    for i in range(size):
        row_i = []
        for j in range(size):
            if i != j:
                summation = 0
                for row in formatted_input_data:
                    summation += get_letter_frequency(row[i]) * get_letter_frequency(row[j]) * get_letter_score(row[i], row[j])

                row_i.append(str(summation)[:6])
            else:
                row_i.append('000000')

        sum_matrix.append(row_i)

    """
    the previous start values are then used to generate candidates for a starting column and then a chain reaction
    """
    s = 0
    possible_start_rows = [True] * size
    highest_dict = {}
    for r in sum_matrix:
        highest = 0
        for i in range(len(r)):
            if s != i:
                if float(r[i]) > float(r[highest]):
                    highest = i
        possible_start_rows[highest] = False
        highest_dict[str(s)] = highest

        s += 1

    next_column = 0
    l = 0
    for state in possible_start_rows:
        if state:
            next_column = l
        l += 1

    countdown = size

    order_guess = []
    while countdown > 0:
        order_guess.append(next_column)
        next_column = highest_dict[str(next_column)]
        countdown -= 1
    print("guess of column order, starting from 0")
    print(order_guess)

    output = ''
    for row in formatted_input_data:
        for guessIndex in order_guess:
            output += row[guessIndex]

    print("guess for text")
    print(output)

if __name__ == '__main__':
    Main()
