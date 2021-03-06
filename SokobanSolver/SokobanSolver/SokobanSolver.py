print("Begin program")

# ----- Classes -------------------------------------------------------------------------

class Node:
    def __init__(self, name, direction, coord, nBox, nGoal, parent = None):
        self.name = name
        self.direction = direction
        self.coord = coord
        self.nBox = nBox
        self.nGoal = nGoal
        self.up = None
        self.left = None
        self.down = None
        self.right = None
        self.parent = parent

    def isRoot(self):
        return not self.parent

    def isLeaf(self):
        return not ( self.left or self.right or self.down or self.up)

    def hasAllChildren(self):
        return (self.left and self.right and self.down and self.up)

    def createChildren(self):
        if self.isLeaf():
            temp = Node(getNameForNode(),LEFT,[],self.nBox,self.nGoal,self)
            illegal,isGoal,boxPush = isIllegalMove(self.coord,LEFT)
            if not illegal:
                temp.coord = self.coord[:]
                if isGoal:    
                    temp.nGoal +=1
                if boxPush:
                    if sokobanMap[temp.coord[0]][temp.coord[1]-1] == GOAL:
                        temp.nGoal -= 1

                self.left = temp
                Openlist.append(temp)
            else:
                self.left = DEAD

            temp = Node(getNameForNode(),DOWN,[],None,self.nGoal,self)
            illegal,isGoal,boxPush = isIllegalMove(self.coord,DOWN)
            if not illegal:
                temp.coord = self.coord[:]
                if isGoal:    
                    temp.nGoal +=1
                if boxPush:
                    if sokobanMap[temp.coord[0]+1][temp.coord[1]] == GOAL:
                        temp.nGoal -= 1

                self.down = temp
                Openlist.append(temp)
            else:
                self.down = DEAD

            temp = Node(getNameForNode(),RIGHT,[],None,self.nGoal,self)
            illegal,isGoal,boxPush = isIllegalMove(self.coord,RIGHT)
            if not illegal:
                temp.coord = self.coord[:]
                if isGoal:    
                    temp.nGoal +=1
                if boxPush:
                    if sokobanMap[temp.coord[0]][temp.coord[1]+1] == GOAL:
                        temp.nGoal -= 1

                self.right = temp
                Openlist.append(temp)
            else:
                self.right = DEAD

            temp = Node(getNameForNode(),UP,[],None,self.nGoal,self)
            illegal,isGoal,boxPush = isIllegalMove(self.coord,UP)
            if not illegal:
                temp.coord = self.coord[:]
                if isGoal:    
                    temp.nGoal +=1
                if boxPush:
                    if sokobanMap[temp.coord[0]-1][temp.coord[1]] == GOAL:
                        temp.nGoal -= 1

                self.up = temp
                Openlist.append(temp)
            else:
                self.up = DEAD



class Tree:
     def __init__(self):
         self.root = None
         self.size = 0

     def length(self):
         return self.size

     def insert(self, direction):
         return 0



# ----- Variables and lists -----------------------------------------------------------------------

Openlist=[]
ClosedList = []
GoalList = []
BoxList = []

initMap = []
sokobanMap = []



iterator = 1



WALL = '#'
GOAL = 'G'
PLAYER = 'M'
DIAMOND = 'J'
FLOOR = '.'
NOTHING = ' '

UP  = 'u'
LEFT = 'l'
DOWN = 'd'
RIGHT = 'r'

DEAD = 0


hashTable = {} # Hashtable for holding the sorted positions of boxes


# Should implement a solution list instead of only the sokoban map



# ----- Hash functions -------------------------------------------------------------------------

def hashing(listoflist):
    hashval = 0
    for i in listoflist:
        for j in i:
            hashval = hashval * 53 + j

    return hashval

def insertInHashtable(hashtable, listoflists, key):
    if not hashtable.get(key, 0):
        hashtable[key] = listoflists
    else:
        print('overwrite', listoflists, key)


# ----- Map functions -----
def readMap(nameOfFile): #Reads the map and outputs the layout to a list of strings and to the terminal. 
    print("Reading the map")

    testMapObject = open(nameOfFile+(".txt"))
    tempList = []
    for line in testMapObject:
        tempList = []
        for elem in range(len(line)-1):
            tempList.append(line[elem])
        sokobanMap.append(tempList)    
        print (line,end = "")


def visualizeMap():
    for i in range(len(sokobanMap)):
        for j in range(len(sokobanMap[i])):
            print(sokobanMap[i][j],end="")
        print("\n",end="")
    print("\n")


def visualizeMap2():
    for i in sokobanMap:
        print(i)



# ----- Random functions -----
def li():
    print('--------------------------------------------------------')



def sortCoord(listoflists): 
    #It will first sort on the y value and if that's equal then it will sort on the x value. 
    #I would also advise to not use list as a variable because it is a built-in data structure.
    temp = sorted(listoflists , key=lambda k: [k[5], k[1]])
    return temp


def getNameForNode():
    global iterator
    iterator+=1
    return iterator-1


def isIllegalMove(coord, dir): # Returns two variables: first being illegal move, Second being whether the diamond is placed on a goal
    # This function takes the current map as a reference for box positions but this should be changed to the list with box coordinates
    x = coord[0]
    y = coord[1]
    if dir == LEFT:
        if sokobanMap[x][y -1] == DIAMOND:
            if sokobanMap[x][y -2] == FLOOR:
                if sokobanMap[x][y -2] == GOAL:
                    return False,True, True               #Returns legal 
                else:
                    return False, False,True
            else: 
                return True,False, True
        else:
            if sokobanMap[x][y -1] == FLOOR:
                return False, False, False
            else:
                return True,False,False
    elif dir == UP:
        if sokobanMap[x-1][y ] == DIAMOND:
            if sokobanMap[x-2][y ] == FLOOR:
                if sokobanMap[x-2][y ] == GOAL:
                    return False,True, True               #Returns legal 
                else:
                    return False, False,True
            else: 
                return True,False, True
        else:
            if sokobanMap[x-1][y ] == FLOOR:
                return False, False, False
            else:
                return True,False,False
    elif dir == RIGHT:
        if sokobanMap[x][y +1] == DIAMOND:
            if sokobanMap[x][y +2] == FLOOR:
                if sokobanMap[x][y+2 ] == GOAL:
                    return False,True, True               #Returns legal 
                else:
                    return False, False,True
            else: 
                return True,False, True
        else:
            if sokobanMap[x][y +1] == FLOOR:
                return False, False, False
            else:
                return True,False,False
    elif dir == DOWN:
        if sokobanMap[x+1][y] == DIAMOND:
            if sokobanMap[x+2][y] == FLOOR:
                if sokobanMap[x+2][y ] == GOAL:
                    return False,True, True               #Returns legal 
                else:
                    return False, False,True
            else: 
                return True,False, True
        else:
            if sokobanMap[x+1][y] == FLOOR:
                return False, False, False
            else:
                return True,False,False




#def solveSokoban():

#def insert(self,data):
#    if self.data:




#    # Insert method to create nodes
#    def insert(self, data):

#        if self.data:
#            if data < self.data:
#                if self.left is None:
#                    self.left = Node(data)
#                else:
#                    self.left.insert(data)
#            elif data > self.data:
#                if self.right is None:
#                    self.right = Node(data)
#                else:
#                    self.right.insert(data)
#        else:
#            self.data = data
## findval method to compare the value with nodes
#    def findval(self, lkpval):
#        if lkpval < self.data:
#            if self.left is None:
#                return str(lkpval)+" Not Found"
#            return self.left.findval(lkpval)
#        elif lkpval > self.data:
#            if self.right is None:
#                return str(lkpval)+" Not Found"
#            return self.right.findval(lkpval)
#        else:
#            print(str(self.data) + ' is found')
## Print the tree
#    def PrintTree(self):
#        if self.left:
#            self.left.PrintTree()
#        print( self.data),
#        if self.right:
#            self.right.PrintTree()

#def move(direction):
    #if direction == "u" or direction == "U":
        



# ----- Program ------------------------------------------------------------------------

readMap("testMap")
print("\n")
print(len(sokobanMap[0]))
print(len(sokobanMap[1]))
print(len(sokobanMap[4]))
visualizeMap()
print('visualizeMap2')
visualizeMap2()



for i in range(len(sokobanMap)):
    for j in range(len(sokobanMap[i])):
        if sokobanMap[i][j] == GOAL:
            GoalList.append(sokobanMap[i][j])
        if sokobanMap[i][j] == DIAMOND:
            BoxList.append(sokobanMap[i][j])

for i in range(len(sokobanMap)):
    for j in range(len(sokobanMap[i])):
        if sokobanMap[i][j] == PLAYER or sokobanMap[i][j] == DIAMOND:
            





print(".",sokobanMap[0][1],".")
        

print(sokobanMap[4][0],sokobanMap[4][1],sokobanMap[4][2],end="")

print(sokobanMap[4][3])

root = Node(getNameForNode(),'init',[1,1],1,0)

mytree = Tree()

mytree = root
Openlist.append(root)
#print(mytree.coord)

#print('is leaf', root.isLeaf())
#print('left', mytree.left)
#print('up',mytree.up)
#print('down', mytree.down)
#print('right', mytree.right)


#print(mytree.parent)
#for i in Openlist:
#    print(Openlist[i.name])

    
#print('node has all children', root.hasAllChildren())


li()

print(root.isLeaf())

print(isIllegalMove(root.coord,LEFT))

print(Openlist)

root.createChildren()

print(len(Openlist))

for i in Openlist:
    print(i.name)
    
