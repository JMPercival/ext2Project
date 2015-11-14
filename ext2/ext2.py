from math import log, ceil
from partHelp import *
import ext2.superblock as superblock
import ext2.groupDescriptor as groupDescriptor

class ext2:
    def __init__(self, part):
        self.part = part['start']*512
        self.sb = superblock.superblock(getLocation(0x400, self.part + 0x400))


    def iterateGroupGenerator(self):
        for group in range(self.sb.desc_block_num):
            pass

    #this is the lazy way of doing this, it will have to be upgraded to a generator later
    def buildGroupDescriptors(self):
        self.groupDescs = []
        #need to pull out the location first for speed purposes
        descGroupHex = getLocation(0x20 * self.sb.desc_block_num, self.part + 0x1200)
        for groupDescInd in range(self.sb.desc_block_num):
            self.groupDescs.append(groupDescriptor.groupDescriptor(getHex(descGroupHex, 0x20*groupDescInd, 0x20+0x20*groupDescInd)))

    def getInodeTables(self):
        for x in self.groupDescs:
            print(int(x.bg_inode_table,16))

















