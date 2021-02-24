from os.path import realpath, join
import matplotlib.pyplot as plt
import pandas as pd
from string_util import assert_dir
from sklearn.cluster import KMeans
from config import  k, data_vec_path, ClusterCapacity
import numpy as np
from sklearn.decomposition import PCA
from config import iterations
import json
from scipy.spatial.distance import cosine
from vector_manager import VectorManager as VM

class SeedBasedClustering():
    def __init__(self):
        self.keywords_path_dict = {}

    def read_reduced_data(self):
        keywords, vecs = self.read_data()
        # X_embedded = TSNE(n_components=2).fit_transform(vecs)
        X_embedded = PCA(n_components=2).fit_transform(vecs)
        return keywords, X_embedded

    def read_data(self):
        dir_path = join(realpath('.'), data_vec_path)
        dir_path = join(dir_path, 'keywords_vecs.csv')
        dataset = pd.read_csv(dir_path, header=None)
        dataset = dataset.fillna(0)
        self.dataset = dataset
        arr = dataset.to_numpy()

        keywords = arr[:, 3]
        vecs = arr[:, 4:]

        return keywords, vecs

    def get_seeds(self):
        with(open(join(realpath('.'), 'data', 'seeds.csv'), 'r')) as file:
            content = file.read()
        seeds =  content.split('\n')

        vm = VM(seeds)
        seeds_vecs = vm.get_word_vecs()
        return seeds_vecs

    def classify_keyword(self, x_vec, seeds_vec):
        x_vec = np.array(x_vec,dtype="float64")
        seeds_vec = np.array(seeds_vec,dtype="float64")
        dists = np.empty(shape=(seeds_vec.shape[0]), dtype="float64")
        for i, seed in enumerate(seeds_vec):
            #calculate cosine
            dist = cosine(x_vec, seed)
            dists[i] = dist

        target = np.argmin(dists, axis=0)
        return target

    def save_labeled_data(self, keywords, labels, X):
        X_embedded = PCA(n_components=2).fit_transform(X)

        assert_dir(join(realpath('.'), 'results'))
        with(open(join(realpath('.'), 'results', 'seed_based_clutered.csv'), 'w')) as file:
            for i, keyword, label, x0, x1 in zip(range(len(keywords)), keywords, labels, X_embedded[:, 0], X_embedded[:, 1]):
                line = str(i) + ',' + keyword + ',' + str(label) + ',' + str(x0) + ',' + str(x1) + '\n'
                file.write(line)

    # main recursive method
    def run(self, X, keywords):
        seeds = self.get_seeds()
        print("Seeds = ", len(seeds))
        labels = []
        for i, keyword in enumerate(keywords):
            label = self.classify_keyword(X[i], seeds)
            labels = labels + [label]
        self.save_labeled_data(keywords, labels, X)

if __name__ == '__main__':
    clust = SeedBasedClustering()
    keywords, X = clust.read_data()
    clust.run(X, keywords)
