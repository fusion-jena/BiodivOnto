from os.path import realpath, join
import matplotlib.pyplot as plt
import pandas as pd
from string_util import assert_dir
from sklearn.cluster import KMeans
from config import  k, data_vec_path, ClusterCapacity
import numpy as np
from sklearn.manifold import TSNE
from sklearn.decomposition import PCA
from config import iterations
import json

class RecursiveClustering():
    def __init__(self):
        self.keywords_path_dict = {}

    def read_data(self):
        dir_path = join(realpath('.'), data_vec_path)
        dir_path = join(dir_path, 'keywords_vecs.csv')
        dataset = pd.read_csv(dir_path, header=None)
        dataset = dataset.fillna(0)
        self.dataset = dataset
        arr = dataset.to_numpy()

        keywords = arr[:, 3]
        vecs = arr[:, 4:]

        # X_embedded = TSNE(n_components=2).fit_transform(vecs)
        X_embedded = PCA(n_components=2).fit_transform(vecs)

        return keywords, X_embedded

    def init_keywords_path(self, keywords):
        for keyword in keywords:
            self.keywords_path_dict[keyword] = ['0']

    def __update_keyword_path(self, keyword_lst, node):
        for keyword in keyword_lst:
            self.keywords_path_dict[keyword] = self.keywords_path_dict[keyword] + [str(node)]

    def save_keywords_path(self):
        #save json file for the dictionary
        dir_path = join(realpath('.'), 'results')
        dir_path = join(dir_path, 'keywords_path.json')
        with(open(dir_path, 'w')) as file:
            json.dump(self.keywords_path_dict, file)

    def get_deepest_branch(self):
        ln = 0
        for key, val in self.keywords_path_dict.items():
            if len(val) > ln:
                ln = len(val)
        return ln

    # core algorithm
    def fit_kmeans(self, X):
        if len(X) <= ClusterCapacity:
            return -1, None #No furthr clustering is applied!
        km = KMeans(k)
        k_clusters = km.fit_predict(X)
        return len(set(k_clusters)), k_clusters

    # recursive util
    def __save_labeled_data(self, X, keywords, y_hc, iterationPath):

        keywords = pd.Series(keywords)
        labels = pd.Series(y_hc)
        vecX0 = X[:,0]
        vecX1 = X[:,1]

        df = pd.DataFrame({'keywords':keywords, 'labels': labels,  'X0':vecX0, 'X1': vecX1})
        res_path = join(realpath('.'), 'results', 'clustered')
        assert_dir(res_path)
        df.to_csv(join(res_path, '{0}_keywords_vecs_clustered.csv'.format(iterationPath)))

    # recursive util
    def __filter_data(self, cluster, X, keywords, y_clustered):
        cnt = len([x for x in y_clustered if x == cluster])
        newKeywords = []
        newX = np.ndarray((cnt,2))
        j = 0
        for i, y in enumerate(y_clustered):
            if y == cluster:
                newX[j] = X[i]
                newKeywords =  newKeywords + [keywords[i]]
                j = j + 1

        return newX, newKeywords

    # main recursive method
    def run(self, X, keywords, iteration, iterationPath):
        out_ks, y_clustered = self.fit_kmeans(X)
        if out_ks == -1 or len(X) <= ClusterCapacity: #stoping condition
            self.__save_labeled_data(X, keywords, y_clustered, iterationPath)
            return
        if iteration == iterations: #stoping condition
            self.__save_labeled_data(X, keywords, y_clustered, iterationPath)
            return

        #Uncomment this if you want to save every single recursive call
        # self.__save_labeled_data(X, keywords, y_clustered, iterationPath)
        for out_k in range(out_ks):
            newX, newKeywords = self.__filter_data(out_k, X, keywords, y_clustered)
            self.__update_keyword_path(newKeywords, out_k)
            newIteration = iteration + 1
            newIterationPath = iterationPath + str(out_k)
            self.run(newX, newKeywords, newIteration, newIterationPath)


if __name__ == '__main__':
    recurs = RecursiveClustering()
    keywords, X = recurs.read_data()
    recurs.init_keywords_path(keywords)
    recurs.run(X, keywords, 0, '0')
    recurs.save_keywords_path()