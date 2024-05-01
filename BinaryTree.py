class BinaryTree:
    def __init__(self):
        self.__root = Node(None)
        self.__current = self.__root

    def insert_data(self, data):
        self.__current.insert_data(data)

    def add_left(self):
        self.__current.set_left(Node(None, self.__current))
        self.__current = self.__current.get_left()
        return True

    def add_right(self):
        self.__current.set_right(Node(None, self.__current))
        self.__current = self.__current.get_right()
        return True

    def get_left(self):
        return self.__current.get_left()

    def get_right(self):
        return self.__current.get_right()

    def set_current(self, node):
        self.__current = node

    def get_current(self):
        return self.__current

    def back_to_root(self):
        self.__current = self.__root
        return True

    def back_to_parent(self):
        if self.__current.get_parent() is not None:
            self.__current = self.__current.get_parent()
            return True
        else:
            return False

    def get_tree(self):
        result = []  # Создаем пустой список для сбора значений
        self._view_inorder(self.__root, result)
        return result

    def _view_inorder(self, node, result):
        if node:
            # Рекурсивно обходим левое поддерево
            self._view_inorder(node.get_left(), result)
            # Добавляем значение текущего узла в список
            result.append(node.get_data())
            # Рекурсивно обходим правое поддерево
            self._view_inorder(node.get_right(), result)

    def get_leaf_values(self):
        result = []
        self._get_leaf_values(self.__root, result)
        return result

    def _get_leaf_values(self, node, result):
        if node:
            if not node.get_left() and not node.get_right():
                result.append(node.get_data())
            self._get_leaf_values(node.get_left(), result)
            self._get_leaf_values(node.get_right(), result)
class Node:
    def __init__(self, data=None, parent=None):
        self.__data = data
        self.__parent = parent
        self.__left = None
        self.__right = None

    def get_parent(self):
        return self.__parent

    def get_right(self):
        return self.__right

    def get_left(self):
        return self.__left

    def set_right(self, node):
        self.__right = node

    def set_left(self, node):
        self.__left = node

    def get_data(self):
        return self.__data

    def insert_data(self, data):
        self.__data = data
