from os import listdir
from os.path import realpath, join
import matplotlib.pyplot as plt
import pandas as pd
from string_util import assert_dir
import numpy as np
from  config import figFormat, figSize

class Visualizer():
    def __init__(self):
        pass

    def read_clustered_data(self, filename):
        dir_path = join(realpath('.'), 'results', 'clustered')
        dir_path = join(dir_path, filename)
        dataset = pd.read_csv(dir_path)
        dataset = dataset.fillna(0)
        self.dataset = dataset
        arr = dataset.to_numpy()

        keywords = arr[:, 1]
        y = arr[:,2]
        X = arr[:, 3:]
        return keywords, X, y

    def __get_cmap(self, n, name='hsv'):
        '''Returns a function that maps each index in 0, 1, ..., n-1 to a distinct
        RGB color; the keyword argument name must be a standard mpl colormap name.'''
        return plt.cm.get_cmap(name, n)

    def __visiualize_annotate(self, X, y, keywords, clustername):

        fig, ax = plt.subplots(figsize=figSize)
        classes = set(y)
        cmap = self.__get_cmap(2*len(classes))
        for i in classes:
            x_axis, y_axis, keys = [], [], []
            for l in range(len(y)):
                if y[l] == i:
                    x_axis = x_axis + [X[l, 0]]
                    y_axis = y_axis + [X[l, 1]]
                    keys = keys + [keywords[l]]

            #also working but gives a warning about the color shape!
            ax.scatter(x_axis, y_axis, c=cmap(i*2), s=100, label='Cluster {0}'.format(i))
            # ax.scatter(x_axis, y_axis, c=np.array(cmap(i)).reshape(1,-1), s=100, label='Cluster {0}'.format(i))
            for j, txt in enumerate(keys):
                ax.annotate(txt, (x_axis[j], y_axis[j]))

        plt.title('Clusters of Words')
        plt.xlabel('Word X0')
        plt.ylabel('Word X1')
        plt.legend(classes)
        dir_path = join(realpath('.'), 'results', 'figs', 'seed_based_clusters')
        assert_dir(dir_path)
        plt.savefig(join(dir_path, '{0}_clusters.{1}'.format(clustername, figFormat)), bbox_inches='tight')


    def __visiualize(self, X, y):
        fig, ax = plt.subplots(figsize=figSize)
        classes = set(y)
        for i in classes:
            ax.scatter(X[y == i, 0], X[y == i, 1], c=np.random.rand(3, ),
                        label='Cluster {0}'.format(i))

        plt.title('Clusters of Words')
        plt.xlabel('Word X0')
        plt.ylabel('Word X1')
        plt.show()

    def run(self):
        dir_path = join(realpath('.'), 'results', 'clustered')
        clusteredfiles = listdir(dir_path)
        for file in clusteredfiles:
            clustername = file.split('_')[0]
            keywords, X, y = self.read_clustered_data(file)
            # self.__visiualize(X, y)
            self.__visiualize_annotate(X, y, keywords, clustername)

    def get_seeds(self):
        with(open(join(realpath('.'), 'data', 'seeds.csv'), 'r')) as file:
            content = file.read()
        seeds = content.split('\n')
        return seeds
    def visualize_seed_based(self):
        file = join(realpath('.'), 'results', 'seed_based_clutered.csv')
        keywords, X, y = self.read_clustered_data(file)
        self.__visiualize_annotate(X, y, keywords, "Seed-based Clusters")
    def visualize_individual_cluster(self):
        file = join(realpath('.'), 'results', 'seed_based_clutered.csv')
        keywords, X, y = self.read_clustered_data(file)

        seeds = self.get_seeds()

        for si, s in enumerate(seeds):
            indexes = [i for i, e in enumerate(y) if e == si]
            cKeywords = [e for i, e in enumerate(keywords) if i in indexes ]
            cY = [si for i in range(len(indexes))]
            self.__visiualize_annotate(X, cY,cKeywords, s)

if __name__ == '__main__':
    # Visualizer().run()
    # Visualizer().visualize_seed_based()
    Visualizer().visualize_individual_cluster()