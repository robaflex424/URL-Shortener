import random
from datetime import datetime, timezone

from fastapi import HTTPException

def get_random_character(string_array):
  random_number_to_get_string = random.randint(0, len(string_array) - 1)

  random.shuffle(string_array)

  array = string_array[random_number_to_get_string]
  random_character = random.choice(array)
  
  return random_character


def generate_short_code():
  alphabet = "abcdefghijklmnopqrstuvwxyz"
  alphabet_upper = alphabet.upper()
  numbers = "0123456789"
  symbols = "!@#$%^&*()-_+="

  multi_string_array = [alphabet, alphabet_upper, numbers, symbols]

  short_code_to_return = ""

  length_of_short_code = 6


  for n in range(length_of_short_code):
      character = get_random_character(multi_string_array)
      short_code_to_return += character
  
  return short_code_to_return
