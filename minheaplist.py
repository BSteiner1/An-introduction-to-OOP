
class Node:
    def __init__(self,val,le,ri,pa):
        self.value = val
        self.left=le
        self.right=ri
        self.parent=pa

    # prints the whole tree below the current node
    def print(self):
        self.printrec(0)

    # recursively prints the values in the tree, indenting by depth
    def printrec(self,depth):
        print("    "*depth,end="") # right amount of indentation
        print(self.value)
        if self.left==None:
            print("    "*(depth+1),"None")
        else:
            self.left.printrec(depth+1)
        if self.right==None:
            print("    "*(depth+1),"None")
        else:
            self.right.printrec(depth+1)

class Item:
    def __init__(self,aroot,p,n):
        self.heap=aroot
        self.previous=p
        self.next=n

class MinHeaplist:
    def __init__(self):
        self.min = None

    # add an item to an empty rootlist and set pointers to itself
    
    def isEmpty(self, x):
        temp = Node(x, None, None, None)
        temp.parent = temp
        item = Item(temp, None, None)
        self.min = item
        self.min.next = self.min
        self.min.previous = self.min
     
    # add an item when the rootlist is not empty
    # we make the arbitrary choice to insert next to the current minimum item
    
    def regularInsert(self, x):
        temp = Node(x, None, None, None)
        temp.parent = temp
        item = Item(temp, self.min, self.min.next)
        self.min.next.previous = item
        self.min.next = item
        if x < self.min.heap.value:      # check if the new item is the minimum
            self.min = item
    
    # maintain the min-heap and binary tree properties when we call linkheaps()
    # we are recursively calling this function and sifting down the left tree
    
    def maintainHeap(self, lesser, greater):
        if lesser.left == None:         
            lesser.left = greater
            greater.parent = lesser
        elif lesser.left.value <= greater.value:
            self.maintainHeap(lesser.left, greater)
        else:
            removed = lesser.left
            removed.parent = None
            lesser.left = greater
            greater.parent = lesser
            self.maintainHeap(removed, lesser.left)
   
    # find the root we are moving
    
    def find_and_place(self, h1, h2):
        if h1 == None or h2 == None:   # if either trees are empty, we are done
            return 
        moved_heap = None
        stay = None
        # determining which tree has the minimal root value to stay in its place
        if h1.value < h2.value:     
            moved_heap = h2
            stay = h1
        else:
            moved_heap = h1
            stay = h2 

        # find the item which has the greater root value which we will move
        item = self.min
        while item.heap.value != moved_heap.value:
            item = item.next
        item.previous.next = item.next
        item.next.previous = item.previous
        
        # placing the moved root in its correct position
        if stay.left == None:   # place moved root to the left if None
            stay.left = moved_heap
            moved_heap.parent = stay 
        elif stay.right == None:   # place moved root to the right if None
            stay.right = moved_heap
            moved_heap.parent = stay   
        # place moved root on the right and sift removed branch to maintain
        # min-heap property
        elif stay.left.value <= stay.right.value:
            removed = stay.right
            removed.parent = None
            stay.right = moved_heap
            moved_heap.parent = stay
            self.maintainHeap(stay.left, removed)  
        # place moved root on the left and sift removed branch to maintain
        # min-heap property
        else:
            removed = stay.left
            removed.parent = None
            stay.left = moved_heap
            moved_heap.parent = stay
            self.maintainHeap(stay.right, removed)
        return stay
    
    # find new minimum item which is required when we call extractMin() 
    # and decreaseKey()
    # we recursively call this function until we find the minimum 
       
    def findMin(self, min_item, min_value, item):
        global minitem      #use a global variable as seen in lectures
        minitem = min_item
        global minvalue
        minvalue = min_value
        minimum_value = min_value
        minimum_item = min_item
        if min_item.next == min_item:   #minimum item of a list of size one
            minimum_value = min_value
            minimum_item = min_item
        elif item.heap.value < min_value:   # if compared item root value is less, update minimum item and value
            minimum_value = item.heap.value
            minimum_item = item
            self.findMin(minimum_item, minimum_value, minimum_item.next)
        # if compared item root value is larger, proceed to next comparison
        elif item.heap.value > min_value:
            self.findMin(min_item, min_value, item.next)
        # we have found new minimum
        elif item.heap.value == min_value and item == min_item:
            minvalue = min_value
            minitem = item
        return minvalue     

    def insert(self,x):
        if self.min == None:
            self.isEmpty(x)
        else:
            self.regularInsert(x)        
    
    def linkheaps(self,h1,h2):
        new_root = self.find_and_place(h1, h2)
        return new_root
     
    # extract and return minimum value of rootlist by disconnecting minimum and
    # adding children into the rootlist
    # we must also make sure we find the new minimum of the rootlist
    
    def extractMin(self):
        extracted_value = self.min.heap.value
        global minitem
        if self.min.heap.left == None and self.min.heap.right == None:      #root has no children
            self.min.previous.next = self.min.next
            self.min.next.previous = self.min.previous
        elif self.min.heap.left == None:        #root only has a right child
            right_item = Item(self.min.heap.right, self.min.previous, self.min.next)
            self.min.next.previous = right_item
            self.min.previous.next = right_item    
            self.findMin(self.min.previous, self.min.previous.heap.value, right_item)
            self.min = minitem
        elif self.min.heap.right == None:       #root only has a left child
            left_item = Item(self.min.heap.left, self.min.previous, self.min.next)
            self.min.next.previous = left_item
            self.min.previous.next = left_item
            self.findMin(self.min.previous, self.min.previous.heap.value, left_item)
            self.min = minitem
        else:           #placing both children into rootlist
            right_item = Item(self.min.heap.right, None, self.min.next)
            left_item = Item(self.min.heap.left, self.min.previous, right_item)
            right_item.previous = left_item
            self.min.next.previous = right_item
            self.min.previous.next = left_item
            self.findMin(self.min.previous, self.min.previous.heap.value, left_item)
            self.min = minitem
        
        # call linkheaps() on all other items in rootlist until we only have 
        # one item in the rootlist
        
        while self.min.next != self.min:
            self.linkheaps(self.min.heap, self.min.next.heap)
            
        return extracted_value
     
    # connect two min-heaplists by connecting their respective minima
    # to create a single min-heaplist
    # we do this by creating a 'cycle' so the pointers go in the correct direction
    
    def union(self,H):
        if H.min == None or self.min == None:   #one of the MHL's is empty           
            return None
        elif H.min == H.min.next and self.min == self.min.next:   # H and self are only one item
            H.min.next = self.min
            H.min.previous = self.min
            self.min.next = H.min
            self.min.previous = H.min
        elif H.min.next != H.min and self.min == self.min.next:     # self is only one item
            H.min.previous.next = self.min
            self.min.previous = H.min.previous
            self.min.next = H.min
            H.min.previous = self.min
        elif self.min.next != self.min and H.min == H.min.next:     # H is only one item
            self.min.previous.next = H.min
            H.min.next = self.min
            H.min.previous = self.min.previous
            self.min.previous = H.min          
        else:               # both rootlists have at least two items
            self.min.previous.next = H.min.next
            H.min.next.previous = self.min.previous
            H.min.next = self.min
            self.min.previous = H.min
            
        if H.min.heap.value < self.min.heap.value:  # compare minima of the two rootlists
            self.min = H.min  
        return self.min
    
    # decrease the value of a specific node 
    # we then disconnect it and place it as a single heap
    # we also place its children into the rootlist
    # we arbitrarily choose to place next to current self.min for ease
    # we must also rewire the pointers
    
    def decreaseKey(self,node,k):
        node.value = k
        
        if node.parent == node:     # we are decreasing the value of a root this will not violate the 
                                    # min-heap property but we may need to update self.min
            if k < self.min.heap.value:     
                global minitem
                self.findMin(self.min, self.min.heap.value, self.min.next)
                self.min = minitem                       
                    
            if node.right == None and node.left == None:
                None
                
            elif node.right == None:      # root only has a left child
                left = Item(node.left, self.min.previous, self.min)
                self.min.previous.next = left
                self.min.previous = left
            elif node.left == None:         # root only has a right child
                right = Item(node.right, self.min.previous, self.min)
                self.min.previous.next = left
                self.min.previous = left
            else:
                right = Item(node.right, None, self.min)
                left = Item(node.left, self.min.previous, right)
                right.previous = left
                self.min.previous.next = left
                self.min.previous = right
                
            return
    
        else:       # we are decreasing the value of a node that is not a root
            if node.right == None and node.left == None:    # node has no children 
                item = Item(node, self.min, self.min.next)
                item.heap.value = k
                self.min.next.previous = item
                self.min.next = item
                if k < self.min.heap.value:
                    self.min = item
            elif node.right == None:        # node has no right child
                item = Item(node, None, self.min.next)
                item.heap.value = k
                self.min.next.previous = item
                left_tree = Item(node.left, self.min, item)
                item.previous = left_tree
                self.min.next = left_tree
                left_tree.heap.parent = left_tree.heap
                if k < self.min.heap.value:
                    self.min = item
            elif node.left == None:         # node has no left child
                item = Item(node, None, self.min.next)
                item.heap.value = k
                self.min.next.previous = item
                right_tree = Item(node.right, self.min, item)
                item.previous = right_tree
                self.min.next = right_tree
                right_tree.heap.parent = right_tree.heap
                if k < self.min.heap.value:
                    self.min = item
            else:
                item = Item(node, None, self.min.next)
                item.heap.value = k
                self.min.next.previous = item
                right_tree = Item(node.right, None, item)
                item.previous = right_tree
                left_tree = Item(node.left, self.min, item)
                right_tree.previous = left_tree
                left_tree.heap.parent = left_tree.heap
                right_tree.heap.parent = right_tree.heap
                self.min.next = left_tree
                if k < self.min.heap.value:
                    self.min = item
            node.parent = node
            
        return self.min.heap.value


    def print(self):
        h=self.min
        if h != None:
            print("-----")
            h.heap.print()
            h = h.next
            while h != self.min:
                print("-----")
                h.heap.print()
                h = h.next
            print("-----")