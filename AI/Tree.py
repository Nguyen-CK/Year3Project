from AI.Node import Node


class Tree:
    def __init__(self, root: Node =None):
        self.root = root

    def build_tree(self):
        self.root.get_all_possible_moves() # Expand the tree
