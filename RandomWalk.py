
import random
from BinaryWeldedTree import BinaryWeldedTree, BinaryTreeNode

class RandomWalk:
    def __init__(self, tree:BinaryWeldedTree) -> None:
        self.tree = tree

    def make_single_random_step_for_particle(self, node:BinaryTreeNode):
        possible_next_nodes = []
        connected_nodes = self.tree.get_connected_nodes(node)
        if  connected_nodes is not None:
            possible_next_nodes += connected_nodes

        if node.parent is not None: possible_next_nodes.append(node.parent) 
        if node.left is not None: possible_next_nodes.append(node.left) 
        if node.right is not None: possible_next_nodes.append(node.right) 

        nextNodeIndex = random.randint(0, len(possible_next_nodes) - 1)
        return possible_next_nodes[nextNodeIndex]

    def find_node_with_value(self, value, max_steps = 100):
        node = tree.primary_root
        for i in range(0, max_steps):
            if node.value == value:
                return node, i
            node = walk.make_single_random_step_for_particle(node)
        
        return None, max_steps

    def make_single_random_step_for_particles(self, particles, max_particles = 2**5):
        new_particles = set()
        num_particles_to_duplicate = max_particles - len(particles)
        if num_particles_to_duplicate < 0: num_particles_to_duplicate = 0

        num_duplicated_particles = 0
        for particle in particles:
            node = particle
            new_node_1 = self.make_single_random_step_for_particle(node)
            new_particles.add(new_node_1)

            if num_duplicated_particles >= num_particles_to_duplicate: continue 
            new_node_2 = self.make_single_random_step_for_particle(node)
            new_particles.add(new_node_2)
            num_duplicated_particles += 1
        return new_particles

    def _find_node_with_val_in_particles(self, particles, value):
        for node in particles:
            if node.value == value:
                return node 
        return None

    def find_node_multiple_particles(self, value, max_steps = 100):
        node = tree.primary_root
        particles = set([node])
        for i in range(0, max_steps):
            found_node = self._find_node_with_val_in_particles(particles = particles, value = value)
            if found_node is not None: return found_node, i
            particles = walk.make_single_random_step_for_particles(particles)
        
        return None, max_steps


tree = BinaryWeldedTree(3, 4, 'match')
walk = RandomWalk(tree)
node = tree.primary_root

node, steps_num = walk.find_node_with_value(value = 10)
if node is not None:
    print(node.value, node, steps_num)
else:
    print(node, steps_num)

node, steps_num = walk.find_node_multiple_particles(value = 10)
if node is not None:
    print(node.value, node, steps_num)
else:
    print(node, steps_num)