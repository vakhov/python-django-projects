def build_tree(nodes, parent_key='parent_id'):
    # create empty tree to fill
    tree = {}
    # fill in tree starting with roots (those with no parent)
    build_tree_recursive(tree, None, nodes, parent_key)
    return tree

def build_tree_recursive(tree, parent_id, nodes, parent_key):
    # find children
    children = [n for n in nodes if n[parent_key] == parent_id]
    # build a subtree for each child
    for child in children: 
        id = child['id']
        # start new subtree
        tree[id] = child
        tree[id]['nodes'] = {}
        # call recursively to build a subtree for current node
        build_tree_recursive(tree[id]['nodes'], id, nodes, parent_key)