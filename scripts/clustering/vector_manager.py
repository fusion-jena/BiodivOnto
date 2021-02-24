from gensim.models import KeyedVectors
import numpy as np
from string_util import to_snake_case, assert_dir
from os.path import realpath, join
import pandas as pd

class VectorManager():
    def __init__(self, words):
        self.words = words
        self.model = self.__load_model()


    def __load_model(self):
        print("Loading model...")
        model = KeyedVectors.load_word2vec_format(
            join(realpath('.'), 'assets', 'GoogleNews-vectors-negative300.bin'), binary=True)
        return model

    def __preprocess_words(self, lst):
        print("Preprocess words in lst")
        new_lst = []
        for word in lst:
            new_lst = new_lst + [to_snake_case(word)]
        return new_lst

    def save(self,i, word, mag, vec):
        res_dir = join(realpath('.'), 'results')
        assert_dir(res_dir)
        res_dir = join(res_dir, 'keywords_vecs.csv')
        str_vec = [str(i) for i in vec]
        line = str(i) + ',' + str(mag) +',' + '0' + ',' + word  + ',' + ','.join(str_vec) + '\n'
        with(open(res_dir, 'a', encoding='utf-8', errors='ignore')) as file:
            file.write(line)

    def get_word_vecs(self):
        vecs = []
        processed_words = self.__preprocess_words(self.words)
        for word in processed_words:
            vec = self.__get_word_vec(self.model, word)
            vecs = vecs + [vec]
        return np.array(vecs)

    def generate_save_vecs(self):
        processed_words = self.__preprocess_words(self.words)
        for i, word, proc_word in zip(range(len(self.words)), self.words, processed_words):
            vec = self.__get_word_vec(self.model, proc_word)
            if len(vec) > 0:
                mag = self.__get_vec_magnitude(vec)
                self.save(i, word, mag, vec)

    def save_unknown(self, word):
        res_dir = join(realpath('.'), 'results')
        assert_dir(res_dir)
        res_dir = join(res_dir, 'Unknown_keywords.csv')
        with(open(res_dir, 'a', encoding='utf-8', errors='ignore')) as file:
            file.write(word + '\n')

    # Element wise multiplication vector style
    def __get_word_vec(self, model, compound_word):
        compound_vec = np.ones(300,)
        words = compound_word.split("_")
        for word in words:
            try:
                vec = model.wv[word]
                compound_vec = np.multiply(compound_vec , vec)
            except Exception as ex:
                print(ex)
                print(word + " doesn't exist in Vocab!")
                self.save_unknown(word)

        if np.all(compound_vec == 1):
            print("No meaningfull word found!")
            return []
        return list(compound_vec)

    #Concatenation Style Vectors
    # def __get_word_vec(self, model, compound_word):
    #     compound_vec = []
    #
    #     words = compound_word.split("_")
    #     for word in words:
    #         try:
    #             vec = list(model.wv[word])
    #             compound_vec = compound_vec + [vec]
    #         except:
    #             print(word + " doesn't exist in Vocab!")
    #             self.save_unknown(word)
    #
    #     faltted_vec = [val for sublist in compound_vec for val in sublist]
    #
    #     return faltted_vec

    def __get_vec_magnitude(self, vec):
        x = np.array(vec)
        return np.linalg.norm(x)

if __name__ == '__main__':
    data_path  = join(realpath('.'), 'data', 'Keywords.csv')
    df = pd.read_csv(data_path)
    keywords = list(df['Keywords'])
    vecMang = VectorManager(keywords)
    vecMang.generate_save_vecs()