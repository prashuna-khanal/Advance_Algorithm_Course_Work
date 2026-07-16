from city import City

class BSTNode:
    def __init__(self, city):
        self.city = city
        self.left = None
        self.right = None

class BST:
    def __init__(self):
        self.root = None

    def insert(self, city):
        if not self.root:
            self.root = BSTNode(city)
        else:
            self._insert_recursive(self.root, city)

    def _insert_recursive(self, node, city):
        if city.name < node.city.name:
            if node.left is None: node.left = BSTNode(city)
            else: self._insert_recursive(node.left, city)
        elif city.name > node.city.name:
            if node.right is None: node.right = BSTNode(city)
            else: self._insert_recursive(node.right, city)

    def search(self, name):
        return self._search_recursive(self.root, name)

    def _search_recursive(self, node, name):
        if node is None or node.city.name == name: return node
        if name < node.city.name: return self._search_recursive(node.left, name)
        return self._search_recursive(node.right, name)

    def delete(self, name):
        self.root = self._delete_recursive(self.root, name)

    def _delete_recursive(self, node, name):
        if node is None: return node
        if name < node.city.name:
            node.left = self._delete_recursive(node.left, name)
        elif name > node.city.name:
            node.right = self._delete_recursive(node.right, name)
        else:
            if node.left is None: return node.right
            elif node.right is None: return node.left
            temp = self._min_value_node(node.right)
            node.city = temp.city
            node.right = self._delete_recursive(node.right, temp.city.name)
        return node

    def _min_value_node(self, node):
        current = node
        while current.left is not None: current = current.left
        return current
