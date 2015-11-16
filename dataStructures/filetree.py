import partData
#not sure if this import is needed...
#import ext2.directory as directory


class filetree:
    def __init__(self, first):
        self.root = filetreeObject

    def addLeaves(self, branch, leaves):
        pass

class filetreeObject:
    def __init__(self, directoryObject):
        self.inode_number = int(directoryObject.inode,16)
        self.name = directoryObject.name.decode("hex")
        if directoryObject.isFiletype():
            self.filetype = partData.directory_type[int(directoryObject.file_type,16)]
        self.next=[]
        self.parent = ''

