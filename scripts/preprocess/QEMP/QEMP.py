import json
from os import listdir
from os.path import realpath, join
import pandas as pd

def read(dir_path, file, category):
    print(file)
    mypath = join(dir_path, file)
    keyword_lst = []
    lowered_lst = []
    with open(mypath, 'r', encoding='utf8', errors="ignore") as file:
        res = json.load(file)
        ents = res["entities"][category]
        for i, ent in enumerate(ents):
            start = ent['indices'][0]
            end = ent['indices'][1]
            keyword = (res["text"][start:end]).strip()
            if keyword.lower() not in lowered_lst:
                lowered_lst.append(keyword.lower())
                keyword_lst.append(keyword)

    return keyword_lst

if __name__ == '__main__':
    categories = ["Environment", "Quality", "Material", "Process"]
    dir_path = join(realpath(''), "QEMP_data")
    files = [file for file in listdir(dir_path) if file.endswith('.json')]
    res_keyword = []
    res_cat = []
    for file in files:
        for cat in categories:
            keylst = read(dir_path, file, cat)
            res_keyword = res_keyword + keylst
            catlst = [cat for i in range(len(keylst))]
            res_cat = res_cat + catlst

    d = {"Keywords": res_keyword, "Categories":res_cat}
    df = pd.DataFrame(d)
    print(df.head(5))
    print(len(df))

    df = df.drop_duplicates()
    print(len(df))

    csv_path = join(dir_path, "QEMP_Keyword.csv")
    df.to_csv(csv_path, index=None)