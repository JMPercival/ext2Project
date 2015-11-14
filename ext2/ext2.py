from math import log, ceil
from partHelp import *
import ext2.superblock
import ext2.groupDescriptor

class ext2:
    def __init__(self, part):
        self.part = part['start']*512
        self.sb = superblock.superblock(getLocation(0x200, self.part + 0x200))


    def iterateGroupGenerator(self):
        for group in range(self.sb.desc_block_num):
            pass

    #this is the lazy way of doing this, it will have to be upgraded to a generator later
    def buildGroupDescriptors(self):
        self.groupDescs = []
        index = 0x1200
        for groupDescInd in range(self.sb.desc_block_num):
            self.groupDescs.append(groupDescriptor.groupDescriptor(getLocation(0x20, self.part + index)))
            index+=0x20

    def getInodeTables(self):
        for x in self.groupDescs:
            print(int(x.bg_inode_table,16))

















