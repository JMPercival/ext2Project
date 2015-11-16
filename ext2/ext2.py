from math import log, ceil
from partHelp import *
import ext2.superblock as superblock
import ext2.groupDescriptor as groupDescriptor
import ext2.inode as inode
import ext2.directory as directory

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
        descGroupHex = getLocation(0x20 * (self.sb.desc_block_num), 0x1200)
        for groupDescInd in range(self.sb.desc_block_num):
            self.groupDescs.append(groupDescriptor.groupDescriptor(getHex(descGroupHex, 0x20*groupDescInd, 0x20+0x20*groupDescInd)))

    def buildLocations(self):
        self.inode_tables_location_to_groups = {}
        self.block_bitmaps = {}
        self.inode_bitmaps = {}
        counter = 0
        print(len(self.groupDescs))
        for groupDesc in self.groupDescs:
            #print(self.part)
            #print(int(groupDesc.bg_inode_table, 16), self.sb.block_size)
            self.inode_tables_location_to_groups[counter] = self.part + (int(groupDesc.bg_inode_table,16) * self.sb.block_size)
            self.inode_bitmaps[counter] = self.part + (int(groupDesc.bg_inode_table,16) * self.sb.block_size)
            self.block_bitmaps[counter] = self.part + (int(groupDesc.bg_inode_table,16) * self.sb.block_size)
            counter+=1

    def getInode(self, num):
        num = num - 1 #there is not 0 inode so we shift what we asked for down to comply with FS
        inode_block_group = int(num/int(self.sb.s_inodes_per_group,16))
        inode_block_group_location = self.inode_tables_location_to_groups[inode_block_group]
        inode_inside_block_group = int(num%int(self.sb.s_inodes_per_group,16))
        inode_inside_block_group_location = inode_inside_block_group * int(self.sb.s_inode_size,16)
        inode_final_location = int(inode_block_group_location + inode_inside_block_group_location)

        print(self.inode_tables_location_to_groups)
        print(inode_block_group, inode_block_group_location, inode_inside_block_group, inode_inside_block_group_location)
        print(inode_final_location, self.sb.block_size)
        
        newInode = inode.inode(getLocation(self.sb.s_inode_size, inode_final_location))
        #print(a.i_atime_date)
        #print(a.i_block)
        #print(int(a.directBlock0,16))
        print(newInode.part)
        return newInode

    def buildFileTree(self):
        #print('here2')
        root_directory_inode = self.getInode(2)
        #print(root_directory_inode.i_block_dict)
        #print(root_directory_inode.i_block)
        root_directory_list = self.getDirectoryList(root_directory_inode)
        print(root_directory_list)

    def getDirectoryList(self, inode):
        blocksNeeded = []
        for single_i_block in inode.i_block_list:
            if single_i_block != False:
                blocksNeeded.append(int(single_i_block,16))
            else:
                break

        print(inode.i_block)
        print(inode.i_block_list) 
        print(blocksNeeded)

        directoryList = []
        for blockNeeded in blocksNeeded:
            directoryList += self.getDirectoryBlock(blockNeeded)

        return directoryList

    def getDirectoryBlock(self, blockNeeded):
        #print('here')
        directoryList = []
        raw_block = getLocation(self.sb.block_size, self.part + blockNeeded * self.sb.block_size)
        count=0
        while raw_block != '':
            print(len(raw_block))
            print(raw_block[:90])
            count+=1
            newDir = directory.directory(raw_block,self.sb)
            directoryList.append(newDir)
            raw_block = raw_block[int(newDir.rec_len, 16)*2:]
        return directoryList














