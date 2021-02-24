import requests
from config import Semedico_API, Subset_Size
import os
import json
from textwrap3 import wrap
from keywords import keywords

def save(keyword, content):
    my_path = os.path.join(os.path.realpath('..'), "Semedico", "json")
    if not os.path.exists(my_path):
        os.mkdir(my_path)
    my_path = os.path.join(my_path, "{0}.json".format(keyword))
    f = open(my_path, "wb")
    f.write(content)
    f.close()

def crawel():
    for keyword in keywords:
        limited_keyword = keyword + " biodiversity"
        # limited_keyword = keyword + " biodiversity"
        url = Semedico_API.format(limited_keyword, Subset_Size)
        response = requests.get(url)
        save(keyword, response.content)

def convert2txt():
    my_path = os.path.join(os.path.realpath('..'), "Semedico", "json")
    files = [f for f in os.listdir(my_path) if os.path.isfile(os.path.join(my_path, f))]

    res_path = os.path.join(os.path.realpath('..') , "Semedico", "txt")
    if not os.path.exists(res_path):
        os.mkdir(res_path)
    for file in files:
        print(file)
        try:
            file_path = os.path.join(my_path, file)
            res = ''
            with open(file_path, encoding="utf8") as f:
                data = json.load(f)
                for i in range(Subset_Size):
                    title = data['bibliographylist'][i]['articleTitle']
                    abstract = data['bibliographylist'][i]['abstractText']
                    abstract_lines = wrap(abstract, 100)
                    abstract = ''
                    for line in abstract_lines:
                        abstract = abstract + line + '\n'
                    res = res + title + '\n' + '\n' + abstract + '\n' + '\n' + '\n'

                file_name = os.path.splitext(file)[0]
                with open(os.path.join(res_path, '{0}.txt'.format(file_name)), "w", encoding="utf8") as res_file:
                    res_file.write(res)
        except Exception as ex:
            print(ex)

if __name__ == '__main__':
    crawel()
    convert2txt()

