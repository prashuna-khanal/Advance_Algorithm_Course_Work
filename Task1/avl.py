from city import City

class AVLNode:
    def __init__(self, city):
        self.city = city
        self.left = None
        self.right = None
        self.height = 1

class AVLTree:
    def __init__(self):
        self.root = None

    def insert(self, city):
        self.root = self._insert(self.root, city)

    def _insert(self, node, city):
        if not node: return AVLNode(city)
        elif city.name < node.city.name: node.left = self._insert(node.left, city)
        elif city.name > node.city.name: node.right = self._insert(node.right, city)
        else: return node 
        
        node.height = 1 + max(self._get_height(node.left), self._get_height(node.right))
        balance = self._get_balance(node)

        if balance > 1 and city.name < node.left.city.name: return self._right_rotate(node)
        if balance < -1 and city.name > node.right.city.name: return self._left_rotate(node)
        if balance > 1 and city.name > node.left.city.name:
            node.left = self._left_rotate(node.left)
            return self._right_rotate(node)
        if balance < -1 and city.name < node.right.city.name:
            node.right = self._right_rotate(node.right)
            return self._left_rotate(node)
        return node

    def _left_rotate(self, z):
        y = z.right
        T2 = y.left
        y.left = z
        z.right = T2
        z.height = 1 + max(self._get_height(z.left), self._get_height(z.right))
        y.height = 1 + max(self._get_height(y.left), self._get_height(y.right))
        return y

    def _right_rotate(self, z):
        y = z.left
        T3 = y.right
        y.right = z
        z.left = T3
        z.height = 1 + max(self._get_height(z.left), self._get_height(z.right))
        y.height = 1 + max(self._get_height(y.left), self._get_height(y.right))
        return y

    def _get_height(self, node):
        if not node: return 0
        return node.height

    def _get_balance(self, node):
        if not node: return 0
        return self._get_height(node.left) - self._get_height(node.right)

    def search(self, name):
        return self._search(self.root, name)
    
    def _search(self, node, name):
        if node is None or node.city.name == name: return node
        if name < node.city.name: return self._search(node.left, name)
        return self._search(node.right, name)

    def delete(self, name):
        self.root = self._delete(self.root, name)

    def _delete(self, node, name):
        if not node: return node
        elif name < node.city.name: node.left = self._delete(node.left, name)
        elif name > node.city.name: node.right = self._delete(node.right, name)
        else:
            if node.left is None:
                temp = node.right
                node = None
                return temp
            elif node.right is None:
                temp = node.left
                node = None
                return temp
            temp = self._min_value_node(node.right)
            node.city = temp.city
            node.right = self._delete(node.right, temp.city.name)

        if node is None: return node
        node.height = 1 + max(self._get_height(node.left), self._get_height(node.right))
        balance = self._get_balance(node)
        if balance > 1 and self._get_balance(node.left) >= 0: return self._right_rotate(node)
        if balance < -1 and self._get_balance(node.right) <= 0: return self._left_rotate(node)
        if balance > 1 and self._get_balance(node.left) < 0:
            node.left = self._left_rotate(node.left)
            return self._right_rotate(node)
        if balance < -1 and self._get_balance(node.right) > 0:
            node.right = self._right_rotate(node.right)
            return self._left_rotate(node)
        return node

    def _min_value_node(self, node):
        if node is None or node.left is None: return node
        return self._min_value_node(node.left)
