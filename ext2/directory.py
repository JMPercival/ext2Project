from partHelp import *

#takes in the part we need and the superblock
class directory:
    def __init__(self, part, sb):
        self.part = part
        self.inode= getHex(self.part, 0x0, 0x4, True)#Inode
        self.rec_len= getHex(self.part, 0x4, 0x6, True)#Total size of this entry (Including all subfields)
        if sb.s_feature_incompat_dict['EXT2_FEATURE_INCOMPAT_FILETYPE'] == True:
            self.name_len= getHex(self.part, 0x6, 0x7, True)#Name Length least-significant 8 bits
            self.file_type= getHex(self.part, 0x7, 0x8, True)#Type indicator (only if the feature bit for "directory entries have file type byte" is set, else this is the most-significant 8 bits of the Name Length)
            self.filetype_is_on = True
        else:
            self.name_len= getHex(self.part, 0x6, 0x8, True) #Name Length
            self.filetype_is_on = False
        self.name= getHex(self.part, 0x8, 0x8 + int(self.name_len,16), True)#Name characters

    def isFiletype(self):
        return True if self.filetype_is_on == True else False

    def __hash__(self):
        return hash((self.name,self.inode))
    def __eq__(self, other):
        return (self.name, self.inode) == (other.name, other.inode)