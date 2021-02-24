from Tutorial.clustering_manger import ClusteringManager
from os.path import realpath, join
import pandas as pd
from vector_manager import VectorManager
from dfs_clustering import RecursiveClustering
from vis_manager import Visualizer

def init_vectors():
    data_path = join(realpath('.'), 'data', 'Keywords.csv')
    df = pd.read_csv(data_path)
    keywords = list(df['Keywords'])
    vecMang = VectorManager(keywords)
    vecMang.generate_save_vecs()

def cluster():
    recurs = RecursiveClustering()
    keywords, X = recurs.read_data()
    recurs.init_keywords_path(keywords)
    recurs.run(X, keywords, 0, '0')
    recurs.save_keywords_path()

def visualize():
    Visualizer().run()

if __name__ == '__main__':
    init_vectors()
    cluster()
    visualize()