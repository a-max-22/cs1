import random

class BinaryTreeNode:
    def __init__(self, left_color, right_color, left=None, right=None, parent=None):
        self.left_color = left_color
        self.left = left  

        self.right_color = right_color
        self.right = right
        self.parent = parent


class BinaryWeldedTree:
    def __init__(self, depth, num_colors, mirror_mode='random'):
        self.depth = depth
        self.num_colors = num_colors
        self.primary_root = self._build_tree(depth)
        self.mirror_root = self._build_tree(depth) if mirror_mode == 'random' else self._copy_tree(depth, self.primary_root)
        self.leaves_connections = {}
        self._connect_trees(self.primary_root, self.mirror_root)

    def _get_leaves(self, root):
        nodes_list = [root]
        leaves = []
        node_index = 0
        while node_index < len(nodes_list):
            current_node = nodes_list[node_index]
            if current_node.left is None and current_node.right is None:
                leaves.append(current_node)
            if current_node.left is not None: nodes_list.append(current_node.left)
            if current_node.left is not None: nodes_list.append(current_node.right)
            node_index += 1
        
        return leaves


    def randolmy_choose_elem_index(self, list_to_choose_from, forbidden_elem_index = None):
        if forbidden_elem_index is None:
            return random.randint(0, len(list_to_choose_from)-1)
        if forbidden_elem_index > 0:
            return random.randint(0, forbidden_elem_index-1)
        
        return random.randint(forbidden_elem_index, len(list_to_choose_from)-1)
        

    def _connect_trees(self, primary_tree, secondary_tree):
        primary_leaves = self._get_leaves(primary_tree)
        secondary_leaves = self._get_leaves(secondary_tree)

        for primary_leave in primary_leaves:
            firstConnectedLeaveIndex = self.randolmy_choose_elem_index(secondary_leaves)
            secondConnectedLeaveIndex = self.randolmy_choose_elem_index(secondary_leaves, forbidden_elem_index = firstConnectedLeaveIndex)               
            firstConnected = secondary_leaves[firstConnectedLeaveIndex]
            secondConnected = secondary_leaves[secondConnectedLeaveIndex]
            self.leaves_connections[primary_leave] = [firstConnected, secondConnected]
            
            if firstConnected not in self.leaves_connections:
                self.leaves_connections[firstConnected] = []
            
            self.leaves_connections[firstConnected].append(primary_leave)
            if len(self.leaves_connections[firstConnected]) == 2:
                del secondary_leaves[firstConnectedLeaveIndex]

            if secondConnected not in self.leaves_connections:
                self.leaves_connections[secondConnected] = []

            self.leaves_connections[secondConnected].append(primary_leave)
            if len(self.leaves_connections[firstConnected]) == 2:
                del secondary_leaves[secondConnectedLeaveIndex]

    def generate_color(self, forbidden_colors=None):
        all_colors = set(range(1, self.num_colors+1))
        if forbidden_colors is not None and set(forbidden_colors) == all_colors:
            return random.randint(1, self.num_colors)
        
        color = random.randint(1, self.num_colors)
        while forbidden_colors and color in forbidden_colors:
            color = random.randint(1, self.num_colors)
        return color

    def _build_tree(self, depth, parent=None, color_from_parent = None):
        if depth == 0:
            return None
        color =  self.generate_color() if color_from_parent is None else color_from_parent
        left_color = self.generate_color([color])
        right_color = self.generate_color([color, left_color])
        node = BinaryTreeNode(left_color, right_color, parent=parent)
        node.left = self._build_tree(depth - 1, node, left_color)
        node.right = self._build_tree(depth - 1, node, right_color)
        return node

    def _copy_tree(self, depth, node, node_parent = None):
        if depth == 0:
            return None
        node_copy = BinaryTreeNode(node.left_color, node.right_color, parent=node_parent)
        node_copy.left = self._copy_tree(depth - 1, node.left, node_copy)
        node_copy.right = self._copy_tree(depth - 1, node.right, node_copy)
        return node_copy


    def _print_tree_helper(self, root, reverse = False, initial_node_num = 0):
        if root is None: return
        nodes_list = [(root, 0)]
        levels_strings = [''] * self.depth
        node_index = 0

        while node_index < len(nodes_list):
            current_node, level = nodes_list[node_index]
            if current_node.left is not None: nodes_list.append((current_node.left, level + 1))
            if current_node.left is not None: nodes_list.append((current_node.right, level + 1))
            node_index += 1
            
            point_span = 8
            line_width = point_span * (2 ** (self.depth - level))
            if current_node.parent is None:
                color_str = ''
            else:
                color_str = f'({current_node.parent.left_color})' if current_node.parent.left == current_node \
                    else f'({current_node.parent.right_color})' 
            levels_strings[level] += (str(node_index + initial_node_num) + color_str).center(line_width)
        
        if reverse: levels_strings = levels_strings[::-1] 
        for s in levels_strings:
            print(s)

    def print_tree(self):
        self._print_tree_helper(self.primary_root, reverse = False)
        print('\n\n')
        self._print_tree_helper(self.mirror_root, reverse = True, initial_node_num = (2 ** self.depth + 1))


tree = BinaryWeldedTree(3, 4, 'match')
tree.print_tree()
