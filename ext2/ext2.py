from math import log, ceil
from partHelp import *
import ext2.superblock as superblock
import ext2.groupDescriptor as groupDescriptor
import ext2.inode as inode

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
        descGroupHex = getLocation(0x20 * (self.sb.desc_block_num+1), 0x1200)
        for groupDescInd in range(self.sb.desc_block_num):
            self.groupDescs.append(groupDescriptor.groupDescriptor(getHex(descGroupHex, 0x20*groupDescInd, 0x20+0x20*groupDescInd)))

    def getInodeTables(self):
        for x in self.groupDescs:
            print(x.part)
            print([int(x.bg_inode_table,16), int(x.bg_inode_bitmap, 16)])

    def getInode(self, num):
        inodeCreation = getLocation(256, 0x143300)
        a = inode.inode(inodeCreation)
        print(a.i_atime_date)
        print(a.i_block)
        print(int(a.directBlock0,16))















