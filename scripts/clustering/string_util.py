import inflection
from os import makedirs
from os.path import exists

def to_snake_case(word):
    new_word = word.replace(" ", "_").replace(".", "_").replace('-', '_')
    new_word = inflection.underscore(new_word)
    return new_word

def assert_dir(dir_path):
    if not exists(dir_path):
        makedirs(dir_path, exist_ok=True) #recursive mkdir