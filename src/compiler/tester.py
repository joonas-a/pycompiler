from compiler.parser import parse
from compiler.tokenizer import tokenize
from compiler.utils import Token, L, Location

"""
Use this function for local testing
Run with ./main.sh in root
"""

input_string = "1 % 2"

input_list = input_string.split()

tokenized = tokenize(input_string)


def main() -> None:
    print(parse(tokenized))
