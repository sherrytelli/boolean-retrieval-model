class Node:
    def __init__(self, data):
        self.data = data
        self.next = None
        self.__positions = []
        
    def add_position(self, pos):
        self.__positions.append(pos)
        
    def get_positions(self):
        return self.__positions

class Linked_list:
    def __init__(self):
        self.__head = None
        self.__tail = None
        self.__size = 0
    
    def get_head(self):
        """get head of linked list"""
        return self.__head
    
    def get_tail(self):
        """get tail of linked list"""
        return self.__tail
    
    def insert(self, new_data):
        """insert data at end of list"""
        if(self.__head == None):
            new_Node = Node(new_data)
            self.__head = new_Node
            self.__tail = new_Node
        else:
            new_Node = Node(new_data)
            self.__tail.next = new_Node
            self.__tail = new_Node
        self.__size += 1
    
    def size(self):
        "get the current size of linked list"
        return self.__size
    
    def print_list(self):
        """print the list"""
        current = self.__head
        while current != None:
            print(f"{current.data} ", end="")
            current = current.next
        print()
        