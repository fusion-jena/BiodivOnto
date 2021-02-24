from os.path import realpath, join
import matplotlib.pyplot as plt
import pandas as pd
from string_util import assert_dir
from sklearn.cluster import KMeans
from config import  k, data_vec_path, ClusterCapacity
import numpy as np
from sklearn.manifold import TSNE
from config import iterations
import json
from anytree import Node, RenderTree
from anytree.exporter import DotExporter

class TreeManager():
    def __init__(self):
        self.keywords_path_dict = {}

    def load_dict(self):
        dir_path = join(realpath('.'), 'results')
        dir_path = join(dir_path, 'keywords_path.json')
        with(open(dir_path, 'r')) as file:
            self.keywords_path_dict = json.load(file)

    def get_deepest_branch(self):
        ln = 0
        for key, val in self.keywords_path_dict.items():
            if len(val) > ln:
                ln = len(val)
        return ln

    def construct_empty_tree(self, level, parent):

        if level == iterations:  # stoping condition
            return parent.root
        newIteration = level + 1
        for out_k in range(k):
            newParent = Node(str(out_k), parent=parent)
            self.construct_empty_tree(newIteration, newParent)
        return parent.root


if __name__ == '__main__':
    treeMang = TreeManager()
    treeMang.load_dict()
    print(treeMang.get_deepest_branch())
    root = treeMang.construct_empty_tree(0, Node('0'))
    for pre, fill, node in RenderTree(root):
        print("%s%s" % (pre, node.name))

    #is not working on windows!
    # it needs to execute cmd dot which is not found at normal CMD, dot is a command related to graphviz
    # DotExporter(root).to_picture("test.png")