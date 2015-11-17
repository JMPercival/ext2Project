import partData
from sys import exit
#not sure if this import is needed...
#import ext2.directory as directory

##
#THIS FILE WILL PROBABLY BE DEPRECATED... BUILDING THE TREE IS NOT POSSIBLE RIGHT NOW BECAUSE OF RAM CONSTRAINTS
##

class filetree:
    def __init__(self):
        #the root is '/'...
        self.root = filetreeObject('/')

    #public#
    def printTree(self):
        #TODO: make this print a graphical tree
        print(self.root.next)

    def addNodeStrPath(self):
        pass

    def addNodeDirPath(self, dirObjectList, directoryObject):
        dirObjectList = dirObjectList
        node_to_add = filetreeObject(directoryObject)
        node_to_add_to = self.getNode(dirObjectList)
        if node_to_add_to == None:
            #Todo: raise an exception... the directory path was not found...
            return None
        node_to_add_to.next.append(node_to_add)

    #private#
    def getNode(self, dirObjectList):
        return self.getNodeRecur(dirObjectList, self.root)

    def getNodeRecur(self, dirObjectList, current_node):
        if len(dirObjectList) == 0:
            return current_node

        for node in current_node.next:
            if node.inode_number == int(dirObjectList[0].inode,16) and node.name == dirObjectList[0].name.decode("hex"):
                return self.getNodeRecur(dirObjectList[1:], node)
            else:
                continue

        print("Directory Path Via Node Not Found")
        return None

class filetreeObject:
    def __init__(self, directoryObject):
        if directoryObject == '/':
            self.inode_number = None
            self.name  = '/'
            self.filetype = 'Directory'
            self.next=[]
            self.parent = None
        else:
            self.inode_number = int(directoryObject.inode,16)
            self.name = directoryObject.name.decode("hex")
            if directoryObject.isFiletype():
                self.filetype = partData.directory_type[int(directoryObject.file_type,16)]
            self.next=[]
            self.parent = ''


    def __hash__(self):
        return hash((self.name,self.inode_number))
    def __eq__(self, other):
        return (self.name, self.inode_number) == (other.name, other.inode_number)