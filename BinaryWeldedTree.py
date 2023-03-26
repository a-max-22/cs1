import random
from future.utils import viewitems 

class BinaryTreeNode:
    def __init__(self, left_color, right_color, left=None, right=None, parent=None):
        self.left_color = left_color
        self.left = left  

        self.right_color = right_color
        self.right = right
        self.parent = parent
        self.value = None


class BinaryWeldedTree:
    def __init__(self, depth, num_colors, mirror_mode='random'):
        self.depth = depth
        self.num_colors = num_colors
        self.primary_root = self._build_tree(depth)
        self.mirror_root = self._build_tree(depth) if mirror_mode == 'random' else self._copy_tree(depth, self.primary_root)
        self.leaves_connections = {}

        self._assign_values_to_nodes(self.primary_root)
        self._assign_values_to_nodes(self.mirror_root, initial_value = 10)
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
    
    def _assign_values_to_nodes(self, root, initial_value = 0):
        nodes_list = [root]
        node_index = 0
        while node_index < len(nodes_list):
            current_node = nodes_list[node_index]
            current_node.value = node_index + initial_value
            if current_node.left is not None: nodes_list.append(current_node.left)
            if current_node.left is not None: nodes_list.append(current_node.right)
            node_index += 1

    def randolmy_choose_elem_index(self, list_to_choose_from, forbidden_elem_index = None):
        if forbidden_elem_index is None:
            return random.randint(0, len(list_to_choose_from)-1)
        if forbidden_elem_index > 0:
            return random.randint(0, forbidden_elem_index-1)
        
        if forbidden_elem_index + 1 == len(list_to_choose_from):
            return None
        
        if forbidden_elem_index + 1 == len(list_to_choose_from) - 1:
            return forbidden_elem_index + 1
        
        return random.randint(forbidden_elem_index + 1, len(list_to_choose_from)-1)
        

    def print_connections(self, connections):
        for node in connections:
            print('conn:', node.value, [v.value for v in connections[node]])            
            
    def _connect_trees(self, primary_tree, secondary_tree):
        primary_leaves_init = self._get_leaves(primary_tree)
        secondary_leaves_init = self._get_leaves(secondary_tree)
        i = 0

        couldBuildConnections = False
        while not couldBuildConnections:
            couldBuildConnections = True
            self.leaves_connections = {}
            primary_leaves = primary_leaves_init.copy()
            secondary_leaves = secondary_leaves_init.copy()
            
            for primary_leave in primary_leaves:
                i += 1
                firstConnectedLeaveIndex = self.randolmy_choose_elem_index(secondary_leaves)
                secondConnectedLeaveIndex = self.randolmy_choose_elem_index(secondary_leaves, forbidden_elem_index = firstConnectedLeaveIndex)               
                if secondConnectedLeaveIndex is None:
                    print("Couldn't build connections, trying again")
                    couldBuildConnections = False
                    break
                
                assert firstConnectedLeaveIndex != secondConnectedLeaveIndex,\
                        "Indices must not be equal %d - %d"%(firstConnectedLeaveIndex, secondConnectedLeaveIndex)

                firstConnected = secondary_leaves[firstConnectedLeaveIndex]
                secondConnected = secondary_leaves[secondConnectedLeaveIndex]

                self.leaves_connections[primary_leave] = [firstConnected, secondConnected]
                
                if firstConnected not in self.leaves_connections:
                    self.leaves_connections[firstConnected] = []            
                self.leaves_connections[firstConnected].append(primary_leave)

                if secondConnected not in self.leaves_connections:
                    self.leaves_connections[secondConnected] = []
                self.leaves_connections[secondConnected].append(primary_leave)

                indicesToDel = []
                if len(self.leaves_connections[firstConnected]) == 2:
                    indicesToDel.append(firstConnectedLeaveIndex)

                if len(self.leaves_connections[secondConnected]) == 2:
                    indicesToDel.append(secondConnectedLeaveIndex)
                
                for index in sorted(indicesToDel, reverse=True):
                    del secondary_leaves[index]

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
            levels_strings[level] += (str(current_node.value) + color_str).center(line_width)
        
        if reverse: levels_strings = levels_strings[::-1] 
        for s in levels_strings:
            print(s)

    def print_tree(self):
        self._print_tree_helper(self.primary_root, reverse = False)
        print('\n\n')
        self._print_tree_helper(self.mirror_root, reverse = True, initial_node_num = (2 ** self.depth + 1))


    def _count_colors_in_path_from_root_leaf(self, node, color, num_colors, accumulator_dict):
        is_leaf = node.left is None and node.right is None
        if is_leaf:
            accumulator_dict[node] = num_colors
            return
        
        if node.left is not None:
            num_colors_left = num_colors + 1 if node.left_color == color else num_colors
            self._count_colors_in_path_from_root_leaf(node.left, color, num_colors_left, accumulator_dict)

        if node.right is not None:
            num_colors_right = num_colors + 1 if node.right_color == color else num_colors
            self._count_colors_in_path_from_root_leaf(node.right, color, num_colors_right, accumulator_dict)


    def find_paths_max_edges_count_of_specific_color(self, color):
        primary_tree_leaves_colors_dict = {}
        self._count_colors_in_path_from_root_leaf(tree.primary_root, color, 0, primary_tree_leaves_colors_dict)
        mirror_tree_leaves_colors_dict = {}
        self._count_colors_in_path_from_root_leaf(tree.mirror_root, color, 0, mirror_tree_leaves_colors_dict)
        max_path_leaves = None,None
        max_edges_of_color = 0 
        for leaf_node, num_edges in viewitems(primary_tree_leaves_colors_dict):
            mirror_node_1 = tree.leaves_connections[leaf_node][0]
            mirror_node_2 = tree.leaves_connections[leaf_node][1]

            edges_count_1 = num_edges + mirror_tree_leaves_colors_dict[mirror_node_1]
            edges_count_2 = num_edges + mirror_tree_leaves_colors_dict[mirror_node_2]
            if edges_count_1 > max_edges_of_color:
                max_path_leaves = (leaf_node, mirror_node_1)

            if edges_count_2 > max_edges_of_color:
                max_path_leaves = (leaf_node, mirror_node_2)

        return max_path_leaves


tree = BinaryWeldedTree(3, 4, 'match')
tree.print_tree()

color = 1
max_path_leaves = tree.find_paths_max_edges_count_of_specific_color(color = color)
if max_path_leaves == (None, None):
    print('no path with specified color')
else:
    print('path with most edges of color = %d: ' % color, max_path_leaves[0].value, max_path_leaves[1].value)
