from os.path import realpath, join
from vector_manager import VectorManager as VM
from sklearn.decomposition import PCA
import matplotlib.pyplot as plt
from config import figSize, figFormat, dist_threshold
from string_util import assert_dir
import numpy as np
import pandas as pd
from scipy.spatial.distance import cosine
import seaborn as sns

class SeedsManager():
    def load_seeds_candidates(self):
        with(open(join(realpath('.'), 'data', 'seeds_candidates.csv'), 'r')) as file:
            content = file.read()
        seeds = content.split('\n')
        return [s for s in seeds if s != '']

    def seeds_to_vectos(self, seeds):
        vm = VM(seeds)
        seeds_vecs = vm.get_word_vecs()
        ln = len(seeds_vecs)
        vecs = np.zeros((ln,300))
        for i, sVec in enumerate(seeds_vecs):
            vecs[i:] = sVec
        seeds_vec_embed = PCA(n_components=2).fit_transform(vecs)
        return seeds_vec_embed


    def __get_cmap(self, n, name='hsv'):
        '''Returns a function that maps each index in 0, 1, ..., n-1 to a distinct
        RGB color; the keyword argument name must be a standard mpl colormap name.'''
        return plt.cm.get_cmap(name, n)

    def visualize_seeds(self, X, seeds):
        fig, ax = plt.subplots(figsize=figSize)

        cmap = self.__get_cmap(1)

        # also working but gives a warning about the color shape!
        ax.scatter(X[:,0], X[:,1], c=cmap(1), s=100, label='Seeds Candidates')
        # ax.scatter(x_axis, y_axis, c=np.array(cmap(i)).reshape(1,-1), s=100, label='Cluster {0}'.format(i))
        for j, txt in enumerate(seeds):
            ax.annotate(txt, (X[j,0], X[j,1]))

        plt.title('Seeds Candidates')
        plt.xlabel('Word X0')
        plt.ylabel('Word X1')
        dir_path = join(realpath('.'), 'results', 'figs')
        assert_dir(dir_path)
        # plt.show()
        plt.savefig(join(dir_path, 'seeds.{0}'.format(figFormat)), bbox_inches='tight')

    def plot_distances_heatmap(self, df, distance_file_path, cmap='coolwarm'):
        # plt.rcParams['figure.figsize'] = (20.0, 15.0)
        plt.rcParams['figure.figsize'] = (15.0, 10.0)
        # sns.heatmap(df, cmap='coolwarm', vmin=0, vmax=1)
        svm = sns.heatmap(df, cmap=cmap, vmin=0, vmax=1)
        plt.show()

        figure = svm.get_figure()
        print(join(realpath('.'), distance_file_path))
        figure.savefig(join(realpath('.'), distance_file_path), bbox_inches='tight',
                       dpi=400)

    def calculate_distances(self, X):
        dist_Mat = np.zeros(shape=(X.shape[0], X.shape[0]))
        for i in range(X.shape[0]):
            for j in range(X.shape[0]):
                dist = cosine(X[i], X[j])
                dist_Mat[i][j] = dist
        return dist_Mat

    def calculate_distances_full_view(self, X, seeds):
        distance_file_path = join(realpath('.'), 'results', 'figs', 'seed_distances_heatmap.{0}'.format(figFormat))
        dist_matrix = self.calculate_distances(X)
        df = pd.DataFrame(dist_matrix, index=seeds, columns=seeds)
        self.plot_distances_heatmap(df, distance_file_path)
        df.to_csv(join(realpath('.'), 'results', 'seed_distances.csv'))
        return df

    def binarize(self, df):
        df_bin = df > dist_threshold
        distance_file_path = join(realpath('.'), 'results', 'figs', 'seed_distances_heatmap_bin.{0}'.format(figFormat))
        self.plot_distances_heatmap(df_bin, distance_file_path,cmap='Greys')
        df_bin.to_csv(join(realpath('.'), 'results', 'seed_distances_bin.csv'))
        return df
    def run(self):
        seeds = self.load_seeds_candidates()
        vecs = self.seeds_to_vectos(seeds)

        # self.visualize_seeds(vecs, seeds)
        distances = self.calculate_distances_full_view(vecs, seeds)
        self.binarize(distances)



if __name__ == '__main__':
    SeedsManager().run()