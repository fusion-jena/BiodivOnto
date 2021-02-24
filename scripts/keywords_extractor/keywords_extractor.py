import json
from os import listdir, makedirs, mkdir
from os.path import realpath, join, exists
import pandas as pd
from pattern.text.en import singularize
import nltk

def save_entry_keywords(keywords, corpus_name, file_i):
    print(corpus_name , ' file: ',  file_i, len(keywords))
    keywords.sort()  # sort alphabetically
    d = {"Keywords": keywords}
    df = pd.DataFrame(d)
    # print(len(df))

    df = df.drop_duplicates()
    # print(len(df))
    # print(df.head(5))

    res_dir = join(realpath('.'), 'files_results', corpus_name+'_files_result')
    if not exists(res_dir):
        makedirs(res_dir)
    df.to_csv(join(res_dir, '{0}_{1}.csv'.format(corpus_name, file_i)), index=None)

def parse_corpus(dir_path, file, category):
    corpus_name = file.split('.')[0]
    mypath = join(dir_path, file)

    dataset_i = 0
    keyword_lst = []
    lowered_lst = []

    with open(mypath, 'r', encoding='utf8', errors="ignore") as file:
        res_lst = json.load(file)
        for file_i, res in enumerate(res_lst):

            ents = res["entities"][category]
            for i, ent in enumerate(ents):
                start = ent['indices'][0]
                end = ent['indices'][1]
                keyword = (res["text"][start:end]).strip()
                if keyword is not None and keyword != "" and keyword.lower() not in lowered_lst:
                    lowered_lst.append(keyword.lower())
                    keyword_lst.append(keyword)

            #each two files represents 1 dataset
            if (file_i + 1) % 2 == 0:
                dataset_i = dataset_i + 1
                filtered_keywords,_ = filter(keyword_lst, keyword_lst)
                save_entry_keywords(filtered_keywords, corpus_name, dataset_i)
                keyword_lst = []
                lowered_lst = []


def parse_semedico_corpus(dir_path, file, category):
    corpus_name = file.split('.')[0]
    mypath = join(dir_path, file)

    with open(mypath, 'r', encoding='utf8', errors="ignore") as file:
        res_lst = json.load(file)
        for file_i, res in enumerate(res_lst):
            keyword_lst = []
            lowered_lst = []

            ents = res["entities"][category]
            for i, ent in enumerate(ents):
                start = ent['indices'][0]
                end = ent['indices'][1]
                keyword = (res["text"][start:end]).strip()
                if keyword is not None and keyword != "" and keyword.lower() not in lowered_lst:
                    lowered_lst.append(keyword.lower())
                    keyword_lst.append(keyword)

            filtered_keywords, _ = filter(keyword_lst, keyword_lst)
            save_entry_keywords(filtered_keywords, corpus_name, file_i)


####################################################################
def read(dir_path, file, category):
    mypath = join(dir_path, file)
    keyword_lst = []
    with open(mypath, 'r', encoding='utf8', errors="ignore") as file:
        res_lst = json.load(file)
        for res in res_lst:
            ents = res["entities"][category]
            for i, ent in enumerate(ents):
                start = ent['indices'][0]
                end = ent['indices'][1]
                keyword = (res["text"][start:end]).strip()
                if keyword is not None and keyword != "" and keyword not in keyword_lst:
                    keyword_lst.append(keyword)
    return keyword_lst

def save(keywords, cates, file_path):
    keywords.sort()  # sort alphabetically
    if cates is None:
        d = {"Keywords": keywords}
    else:
        d = {"Keywords": keywords, "Categories": cates}
    df = pd.DataFrame(d)
    # print(len(df))
    # df = df.drop_duplicates()
    print(len(df))

    print(df.head(5))
    df.to_csv(file_path, index=None)

def filter (keywords, cates):
    key_lst, cates_lst = [], []
    lst = [(singularize(plural), cate) for plural, cate in zip(keywords, cates)]
    unique = list(set([(word.lower(), cat) for word, cat in lst]))

    for key, cat in unique:
        key_lst = key_lst + [key]
        cates_lst = cates_lst + [cat]
    return key_lst, cates_lst

def stem(keywords):
    p = nltk.PorterStemmer()
    stemmed = [p.stem(keyword) for keyword in keywords]
    return stemmed

def extract_keywords_per_repo():
    categories = ["Thing"]
    dir_path = join(realpath('.'), "json_GATE_docs")
    files = [file for file in listdir(dir_path) if file.endswith('.json')]
    res_keyword = []
    res_cat = []
    for file in files:
        print(file)
        for cat in categories:
            keylst = read(dir_path, file, cat)
            res_keyword = res_keyword + keylst
            catlst = ['Thing' for cat in range(len(keylst))]
            res_cat = res_cat + catlst

        rep = file.split('.')[0]
        res_dir = join(realpath('.'), 'repo_result')
        if not exists(res_dir):
            mkdir(res_dir)

        save(res_keyword, res_cat, join(res_dir, rep + "_All_Keywords.csv"))
        filtered_keywords, filtered_categories = filter(res_keyword, res_cat)
        save(filtered_keywords, filtered_categories, join(res_dir, rep + "_Filtered_Keywords.csv"))
        # stemmed_keywords = stem(res_keyword)
        # save(stemmed_keywords, res_cat, "Stemmed_Keywords.csv")

def extract_keywords_per_file():
    categories = ["Thing"]
    dir_path = join(realpath('.'), "json_GATE_docs")
    files = [file for file in listdir(dir_path) if file.endswith('.json')]
    for file in files:
        print(file)
        for category in categories:
            if file == 'semedico.json':
                parse_semedico_corpus(dir_path, file, category)
            else:
                parse_corpus(dir_path, file, category)

def load_all_keywords():
    filtered = []
    repos = ['befchina', 'dataworld', 'semedico']
    for repo in repos:
        df = pd.read_csv(join(realpath('.'), 'repo_result', '{0}_Filtered_Keywords.csv'.format(repo)))
        filtered = filtered + list(df['Keywords'])
    filtered = list(set(filtered))
    return filtered

def reconcile_keywords_experts():
    all = load_all_keywords()
    df = pd.read_csv(join(realpath('.'), 'keywords_experts', 'Keywords_Experts.csv'))
    expert_keywords = list(df['Keyword'])
    decision = list(df['Decision'])
    in_words = [word for word, d in zip(expert_keywords, decision) if d == 1]
    out_words = [word for word, d in zip(expert_keywords, decision) if d == 0]
    #assure to exclude out words if it is included by mistake in the files
    words_lst = [w for w in all if w not in out_words]
    #assure to include the words that should be included if it is missed in the files by mistake
    words_lst = words_lst + [w for w in in_words if w not in words_lst]

    res_dir = join(realpath('.'), 'result')
    if not exists(res_dir):
        mkdir(res_dir)

    file_path = join(res_dir, 'Combined_Keywords.csv')
    save(words_lst, None, file_path)

def __generate_overlap(lst1, lst2):
    common = []
    for w1 in lst1:
        for w2 in lst2:
            if w1 == w2:
               common = common + [w1]
    return common

def generate_overlaps():
    manual = load_all_keywords()

    repos = ['AquaDiva', 'QEMP', 'Soil']

    res_dir = join(realpath('.'), 'overlap_results')
    if not exists(res_dir):
        mkdir(res_dir)

    all_common_lst  = []
    for external in repos:
        df = pd.read_csv(join(realpath('.'), 'external_srcs', '{0}_Keywords.csv'.format(external)))
        repoLst = set(list(df['Keywords']))

        commonLst = __generate_overlap(manual, repoLst)
        all_common_lst = all_common_lst + [commonLst]
        file_path = join(res_dir, '{0}_and_Manual.csv'.format(external))
        save(commonLst, None, file_path)

    # Here calculate the common part between the Manual, AquaDiva and QEMP 
    common1 = __generate_overlap(all_common_lst[0], all_common_lst[1])
    file_path = join(res_dir, 'manual_aquadiva_QEMP.csv')
    save(common1, None, file_path)

    #No further overlap between the above common work and Soil keywords
    common2 = __generate_overlap(all_common_lst[1], all_common_lst[2])
    file_path = join(res_dir, 'manual_soil_QEMP.csv')
    save(common2, None, file_path)


if __name__ == '__main__':
    # extract_keywords_per_repo()
    # extract_keywords_per_file()
    # reconcile_keywords_experts()
    generate_overlaps()