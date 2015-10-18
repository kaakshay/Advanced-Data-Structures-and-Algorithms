'''
Created on Sep 30, 2014

@author: Akshay Ashwathanarayana
'''

class SinglyLinkedNode(object):

    def __init__(self, item=None, next_link=None):
        super(SinglyLinkedNode, self).__init__()
        self._item = item
        self._next = next_link

    @property
    def item(self):
        return self._item

    @item.setter
    def item(self, item):
        self._item = item

    @property
    def next(self):
        return self._next

    @next.setter
    def next(self, next):
        self._next = next

    def __repr__(self):
        return repr(self.item.__repr__())


class SinglyLinkedList(object):

    def __init__(self):
        super(SinglyLinkedList, self).__init__()
        self.head = None
        self.length = 0
        pass

    def __len__(self):
        return self.length

    def __iter__(self):
        """
    >>> list = SinglyLinkedList()
    >>> list.prepend(KeyValuePair(27,2))
    >>> iterator = list.__iter__()
    >>> iterator.next()
    [27, 2]
    """
        return ListIterator(self)

    def __contains__(self, key):
        """
    >>> list = SinglyLinkedList()
    >>> list.prepend(KeyValuePair(27,2))
    >>> print list.__contains__(27)
    True
    """
        if self.__get__(key) is not None:
            return True
        return False

    def remove(self, key):
        node = self.head
        if node.item.key == key:
            self.head = node.next
            self.length = self.length - 1
        else:
            while(node is not None and node.next is not None):
                if node.next.item.key == key:
                    if node.next.next is not None:
                        node.next = node.next.next
                    else:
                        node.next = None
                    self.length = self.length - 1
                node = node.next

    def prepend(self, item):
        """
    >>> list = SinglyLinkedList()
    >>> list.prepend(KeyValuePair(27,2))
    >>> list.prepend(KeyValuePair(40,5))
    >>> list.prepend(KeyValuePair(127,65))
    >>> list.prepend(KeyValuePair(128,54))
    >>> list.prepend(KeyValuePair(140,542))
    >>> print list
    List:->[140, 542][128, 54][127, 65][40, 5][27, 2]
    """
        node = SinglyLinkedNode(item, self.head)
        self.head = node
        self.length = self.length + 1

    def __repr__(self):
        s = "List:" + "->"
        node = self.head  # cant point to ll!
        while node is not None:
            s = s + (node._item.__str__())
            node = node._next
        return s

    def __get__(self, key):
        node = self.head
        while(node is not None):
            if node.item.key == key:
                return node.item
            node = node.next
        return None

    def list_print(self):
        node = self.head  # cant point to ll!
        while node is not None:
            print node._item
            node = node._next
        pass


class ListIterator(object):

    def __init__(self, singlyLinkedList):
        self.singlyLinkedList = singlyLinkedList
        self.currentNode = self.singlyLinkedList.head

    def hasNext(self):
        if self.currentNode is not None:
            return True
        return False

    def next(self):
        if self.hasNext():
            returnValue = self.currentNode.item
            self.currentNode = self.currentNode.next
            return returnValue


class ChainedHashDict(object):

    def __init__(self, bin_count=10, max_load=0.7, hashfunc=hash):
        super(ChainedHashDict, self).__init__()
        self.binCount = bin_count
        self.maxLoad = max_load
        self.hashFunction = hashfunc
        self.backingArray = []
        for i in range(self.binCount):
            self.backingArray.append(SinglyLinkedList())
        self.numberOfElements = 0
        pass

    @property
    def load_factor(self):
        return self.numberOfElements / self.bin_count

    @property
    def bin_count(self):
        return self.binCount

    def rebuild(self, bincount):
        self.binCount = bincount
        previousArray = self.backingArray
        self.numberOfElements = 0
        self.deletedElements = 0
        for i in range(self.binCount):
            self.backingArray.append(SinglyLinkedList())
        for list in previousArray:
            if list.head is not None:
                self.backingArray[self.hashFunction(list.head.item.key)] = list

    def __getitem__(self, key):
        hashedKey = self.hashFunction(key)
        return self.backingArray[hashedKey].__get__(key)

    def __setitem__(self, key, value):
        if self.load_factor > self.maxLoad:
            self.rebuild(self.binCount * 2)
        hashedKey = self.hashFunction(key)
        if not self.backingArray[hashedKey].__contains__(key):
            (self.backingArray[hashedKey]).prepend(KeyValuePair(key, value))
            self.numberOfElements = self.numberOfElements + 1
        else:
            self.backingArray[hashedKey].__get__(key).value = value

    def __delitem__(self, key):
        hashedKey = self.hashFunction(key)
        if self.backingArray[hashedKey].__contains__(key):
            self.numberOfElements = self.numberOfElements - 1
        self.backingArray[hashedKey].remove(key)

    def __contains__(self, key):
        hashedKey = self.hashFunction(key)
        return self.backingArray[hashedKey].__contains__(key)

    def __len__(self):
        return self.numberOfElements

    def display(self):
        for i in range(self.binCount):
            print i, " --- ", self.backingArray[i]


class OpenAddressHashDict(object):

    def __init__(self, bin_count=10, max_load=0.7, hashfunc=hash):
        super(OpenAddressHashDict, self).__init__()
        self.binCount = bin_count
        self.maxLoad = max_load
        self.hashFunction = hashfunc
        self.backingArray = [None] * self.binCount
        self.numberOfElements = 0
        self.deletedElements = 0
        self.DELETED = -float("inf")
        pass

    @property
    def load_factor(self):
        return (self.numberOfElements + self.deletedElements) / self.bin_count

    @property
    def bin_count(self):
        return self.binCount

    def rebuild(self, bincount):
        """
    >>> openAddressHashDict = OpenAddressHashDict(bin_count=5)
    >>> openAddressHashDict.__setitem__(12, 1)
    >>> openAddressHashDict.__setitem__(22, 1)
    >>> openAddressHashDict.__setitem__(2, 5)
    >>> openAddressHashDict.__setitem__(3, 5)
    >>> openAddressHashDict.__setitem__(4, 5)
    >>> openAddressHashDict.__setitem__(8, 5)
    >>> openAddressHashDict.__setitem__(9, 5)
    >>> print openAddressHashDict.bin_count,",\
 ",openAddressHashDict.__contains__(12)
    10 ,  True
    """
        self.binCount = bincount
        previousArray = self.backingArray
        self.backingArray = [None] * bincount
        self.numberOfElements = 0
        self.deletedElements = 0
        for prevValue in previousArray:
            if prevValue is not None and prevValue != self.DELETED:
                self.__setitem__(prevValue.key, prevValue.value)

    def __getitem__(self, key):
        """
    >>> openAddressHashDict = OpenAddressHashDict(bin_count=5)
    >>> openAddressHashDict.__setitem__(12, 1)
    >>> print openAddressHashDict.__getitem__(12)
    1
    """
        for i in range(self.binCount):
            probedKey = self.__linearProbing(key, i)
            element = self.backingArray[probedKey]
            if element is not None:
                if element != self.DELETED and element.key == key:
                    return self.backingArray[probedKey].value
            else:
                return None
        return None

    def __setitem__(self, key, value):
        """
    >>> openAddressHashDict = OpenAddressHashDict(bin_count=5)
    >>> openAddressHashDict.__setitem__(12, 1)
    >>> print openAddressHashDict.__contains__(12)
    True
    """
        if self.load_factor > self.maxLoad:
            self.rebuild(self.binCount * 2)
        for i in range(self.binCount):
            probedKey = self.__linearProbing(key, i)
            probedElement = self.backingArray[probedKey]
            if probedElement is None:
                self.backingArray[probedKey] = KeyValuePair(key, value)
                self.numberOfElements = self.numberOfElements + 1
                return
            elif probedElement != self.DELETED and probedElement.key == key:
                self.backingArray[probedKey].value = value
                return
        pass

    def __delitem__(self, key):
        """
    >>> openAddressHashDict = OpenAddressHashDict(bin_count=5)
    >>> openAddressHashDict.__setitem__(10, 1)
    >>> openAddressHashDict.__delitem__(10)
    >>> print openAddressHashDict.__contains__(10)
    False
    """
        for i in range(self.binCount):
            probedKey = self.__linearProbing(key, i)
            element = self.backingArray[probedKey]
            if element is not None:
                if element != self.DELETED and element.key == key:
                    self.backingArray[probedKey] = self.DELETED
                    self.deletedElements = self.deletedElements + 1
                    return
            else:
                return

    def __contains__(self, key):
        for i in range(self.binCount):
            probedKey = self.__linearProbing(key, i)
            probedElement = self.backingArray[probedKey]
            if probedElement is not None and probedElement != self.DELETED:
                if probedElement.key == key:
                    return True
        return False

    def __len__(self):
        """
    >>> openAddressHashDict = OpenAddressHashDict(bin_count=5)
    >>> openAddressHashDict.__setitem__(12, 1)
    >>> openAddressHashDict.__setitem__(22, 1)
    >>> openAddressHashDict.__setitem__(2, 5)
    >>> openAddressHashDict.__setitem__(3, 5)
    >>> openAddressHashDict.__setitem__(4, 5)
    >>> openAddressHashDict.__setitem__(8, 5)
    >>> openAddressHashDict.__setitem__(9, 5)
    >>> print openAddressHashDict.__len__()
    7
    """
        return self.numberOfElements - self.deletedElements
        pass

    def display(self):
        for i in range(self.binCount):
            element = self.backingArray[i]
            if element is not None:
                if element == self.DELETED:
                    print i, "   ----  ", "Deleted"
                else:
                    print i, "   ----  ", element
            else:
                print i, "   ----  ", "Empty"

    def __linearProbing(self, k, i):
        return (self.hashFunction(k) + i) % self.bin_count


class BinaryTreeNode(object):

    def __init__(self, data=None, left=None, right=None, parent=None):
        super(BinaryTreeNode, self).__init__()
        self.data = data
        self.left = left
        self.right = right
        self.parent = parent


class KeyValuePair(object):

    def __init__(self, key, value):
        object.__init__(self)
        self.key = key
        self.value = value

    def __repr__(self):
        return str([self.key, self.value])


class BinarySearchTreeDict(object):

    def __init__(self):
        super(BinarySearchTreeDict, self).__init__()
        self.root = None
        self.length = 0
        pass

    @property
    def height(self):
        """
    >>> bst = BinarySearchTreeDict()
    >>> bst.__setitem__(6, 1)
    >>> bst.__setitem__(5, 15)
    >>> bst.__setitem__(4, 15)
    >>> bst.__setitem__(3, 15)
    >>> bst.__setitem__(2, 15)
    >>> print bst.height
    5
    """
        return self.calculateMaximumHeightRecursive(self.root)

    def calculateMaximumHeightRecursive(self, node):
        if node is None:
            return 0
        else:
            return max(self.calculateMaximumHeightRecursive(node.left),
                       self.calculateMaximumHeightRecursive(node.right)) + 1

    def inorder_keys(self):
        return self.__inorderTraverseRecursive(self.root)

    def __inorderTraverseRecursive(self, binaryTreeNode):
        if binaryTreeNode.left is not None:
            for i in self.__inorderTraverseRecursive(binaryTreeNode.left):
                yield i

        yield binaryTreeNode.data.key

        if binaryTreeNode.right is not None:
            for i in self.__inorderTraverseRecursive(binaryTreeNode.right):
                yield i

    def postorder_keys(self):
        return self.__postTraverseRecursive(self.root)

    def __postTraverseRecursive(self, binaryTreeNode):
        if binaryTreeNode.left is not None:
            for i in self.__inorderTraverseRecursive(binaryTreeNode.left):
                yield i

        if binaryTreeNode.right is not None:
            for i in self.__inorderTraverseRecursive(binaryTreeNode.right):
                yield i

        yield binaryTreeNode.data.key

    def preorder_keys(self):
        return self.__preTraverseRecursive(self.root)

    def __preTraverseRecursive(self, binaryTreeNode):
        yield binaryTreeNode.data.key

        if binaryTreeNode.left is not None:
            for i in self.__inorderTraverseRecursive(binaryTreeNode.left):
                yield i

        if binaryTreeNode.right is not None:
            for i in self.__inorderTraverseRecursive(binaryTreeNode.right):
                yield i

    def items(self):
        self.__inorderTraverseRecursiveItems(self.root)

    def __inorderTraverseRecursiveItems(self, binaryTreeNode):
        if binaryTreeNode.left is not None:
            for i in self.__inorderTraverseRecursive(binaryTreeNode.left):
                yield i

        yield binaryTreeNode.data

        if binaryTreeNode.right is not None:
            for i in self.__inorderTraverseRecursive(binaryTreeNode.right):
                yield i

    def __getitem__(self, key):
        """
    >>> bst = BinarySearchTreeDict()
    >>> bst.__setitem__(5, 1)
    >>> print bst.__getitem__(5)
    1
    """
        searchNode = self.__search(self.root, key)
        if searchNode is not None:
            return searchNode.data.value
        return None

    def __setitem__(self, key, value):
        """
    >>> bst = BinarySearchTreeDict()
    >>> bst.__setitem__(5, 1)
    >>> print bst.__contains__(5)
    True
    """
        keyValuePair = KeyValuePair(key, value)
        if self.root is None:
            self.root = BinaryTreeNode(keyValuePair)
            self.length = self.length + 1
            return
        else:
            self.__recursiveInsert(self.root, keyValuePair)

    def __recursiveInsert(self, binaryTreeNode, keyValuePair):
        if(binaryTreeNode.data.key == keyValuePair.key):
            binaryTreeNode.data.value = keyValuePair.value
        if keyValuePair.key < binaryTreeNode.data.key:
            if binaryTreeNode.left is not None:
                self.__recursiveInsert(binaryTreeNode.left, keyValuePair)
            else:
                node = BinaryTreeNode(keyValuePair)
                binaryTreeNode.left = node
                node.parent = binaryTreeNode
                self.length = self.length + 1
        elif keyValuePair.key >= binaryTreeNode.data.key:
            if binaryTreeNode.right is not None:
                self.__recursiveInsert(binaryTreeNode.right, keyValuePair)
            else:
                node = BinaryTreeNode(keyValuePair)
                binaryTreeNode.right = node
                node.parent = binaryTreeNode
                self.length = self.length + 1

    def __delitem__(self, key):
        """
    >>> bst = BinarySearchTreeDict()
    >>> bst.__setitem__(5, 1)
    >>> bst.__setitem__(4, 15)
    >>> bst.__setitem__(3, 15)
    >>> bst.__delitem__(4)
    >>> print bst.__contains__(4)
    False
    """
        nodeForDeletion = self.__search(self.root, key)
        if nodeForDeletion is not None:
            if nodeForDeletion.left is None:
                self.__transplant(nodeForDeletion, nodeForDeletion.right)
            elif nodeForDeletion.right is None:
                self.__transplant(nodeForDeletion, nodeForDeletion.left)
            else:
                treeMinimum = self.__treeMinimum(nodeForDeletion.right)
                if treeMinimum.parent != nodeForDeletion:
                    self.__transplant(treeMinimum, treeMinimum.right)
                    treeMinimum.right = nodeForDeletion.right
                    treeMinimum.right.parent = treeMinimum
                self.__transplant(nodeForDeletion, treeMinimum)
                treeMinimum.left = nodeForDeletion.left
                treeMinimum.left.parent = treeMinimum
            self.length = self.length - 1

    def __contains__(self, key):
        """
    >>> bst = BinarySearchTreeDict()
    >>> bst.__setitem__(5, 1)
    >>> bst.__setitem__(4, 15)
    >>> bst.__setitem__(3, 15)
    >>> print bst.__contains__(4)
    True
    """
        if self.__search(self.root, key) is not None:
            return True
        return False

    def __len__(self):
        """
    >>> bst = BinarySearchTreeDict()
    >>> bst.__setitem__(5, 1)
    >>> bst.__setitem__(4, 15)
    >>> bst.__setitem__(6, 15)
    >>> bst.__setitem__(2, 15)
    >>> bst.__setitem__(3, 15)
    >>> bst.__len__()
    5
    """

        return self.length

    def display(self):
        inorder = preorder = ""
        for i in self.inorder_keys():
            inorder = inorder + str(i) + " , "
        print "inorder: ", inorder
        for i in self.preorder_keys():
            preorder = preorder + str(i) + " , "
        print "pre order", preorder

    def __treeMinimum(self, binaryTreeNode):
        if binaryTreeNode.left is not None:
            return self.__treeMinimum(binaryTreeNode.left)
        else:
            return binaryTreeNode

    def __transplant(self, u, v):
        if u.parent is None:
            self.root = v
        elif u == u.parent.left:
            u.parent.left = v
        else:
            u.parent.right = v
        if v is not None:
            v.parent = u.parent

    def __search(self, node, key):
        if node is None or key == node.data.key:
            return node
        elif key < node.data.key:
            return self.__search(node.left, key)
        else:
            return self.__search(node.right, key)
        return None


def terrible_hash(bin):
    """A terrible hash function that can be used for testing.

    A hash function should produce unpredictable results,
    but it is useful to see what happens to a hash table when
    you use the worst-possible hash function.  The function
    returned from this factory function will always return
    the same number, regardless of the key.

    :param bin:
        The result of the hash function, regardless of which
        item is used.

    :return:
        A python function that can be passes into the constructor
        of a hash table to use for hashing objects.
    """
    def hashfunc(item):
        return bin
    return hashfunc


def main():
    # Thoroughly test your program and produce useful out.
    #
    # Do at least these kinds of tests:
    #  (1)  Check the boundary conditions (empty containers,
    #       full containers, etc)
    #  (2)  Test your hash tables for terrible hash functions
    #       that map to keys in the middle or ends of your
    #       table
    #  (3)  Check your table on 100s or randomly generated
    #       sets of keys to make sure they function
    #
    #  (4)  Make sure that no keys / items are lost, especially
    #       as a result of deleting another key
#     chainedHashDict = ChainedHashDict(bin_count=10)
    def hashingFunction(bin):
        def hashFunc(item):
            return item % bin
        return hashFunc
    chainedHashDict = ChainedHashDict(
        bin_count=10, hashfunc=hashingFunction(10))
    chainedHashDict.__setitem__(12, 15)
    chainedHashDict.__setitem__(12, 15)
    chainedHashDict.__setitem__(12, 1)
    chainedHashDict.__setitem__(22, 1)
    chainedHashDict.display()
    chainedHashDict.__setitem__(2, 5)
    chainedHashDict.__delitem__(12)
    chainedHashDict.__setitem__(3, 5)
    chainedHashDict.__setitem__(4, 5)
    chainedHashDict.__setitem__(8, 5)
    chainedHashDict.__setitem__(9, 5)
    print chainedHashDict.__getitem__(3)
    chainedHashDict.display()
#     oahd = OpenAddressHashDict(bin_count=5)
    oahd = OpenAddressHashDict(bin_count=10, hashfunc=terrible_hash(10))
    oahd.__setitem__(12, 1)
    oahd.__delitem__(12)
    oahd.__setitem__(2, 5)
    oahd.__delitem__(2)
    oahd.__setitem__(3, 5)
    oahd.__setitem__(4, 5)
    oahd.__setitem__(8, 5)
    oahd.__setitem__(9, 5)
    print oahd.__getitem__(3)
    oahd.display()

    ll = SinglyLinkedList()
    ll.prepend(KeyValuePair(33, 12))
    ll.prepend(KeyValuePair(78, 3))
    ll.prepend(KeyValuePair(40, 3))
    ll.prepend(KeyValuePair(13, 32))
    ll.prepend(KeyValuePair(18, 54))
    ll.prepend(KeyValuePair(16, 12))
    print "******************"
    ll.list_print()
    ll.remove(40)
    print "******************"
    ll.list_print()
    iterator = ll.__iter__()
    while iterator.hasNext():
        print "iter ", iterator.next()

    bst = BinarySearchTreeDict()
    bst.__setitem__(5, 15)
    bst.__setitem__(1, 15)
    bst.__setitem__(0, 15)
    bst.__setitem__(3, 15)
    bst.__setitem__(2, 15)
    bst.__setitem__(10, 15)
    bst.__setitem__(7, 15)
    bst.__setitem__(12, 15)
    bst.__delitem__(5)
    print bst.__getitem__(2)
    print bst.height
    bst.display()
    print bst.root.data.key
    print bst.root.left.data.key
    for i in bst.inorder_keys():
        print i

    pass


if __name__ == '__main__':
    main()
