from math import log, ceil
from partHelp import *
from sys import exit
import partData
import ext2.superblock as superblock
import ext2.groupDescriptor as groupDescriptor
import ext2.inode as inode
import ext2.directory as directory
import dataStructures.filetree as filetree

class ext2:
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
        #print(len(self.groupDescs))
        for groupDesc in self.groupDescs:
            #print(self.part)
            #print(int(groupDesc.bg_inode_table, 16), self.sb.block_size)
            self.inode_tables_location_to_groups[counter] = self.part + (int(groupDesc.bg_inode_table,16) * self.sb.block_size)
            self.inode_bitmaps[counter] = self.part + (int(groupDesc.bg_inode_table,16) * self.sb.block_size)
            self.block_bitmaps[counter] = self.part + (int(groupDesc.bg_inode_table,16) * self.sb.block_size)
            counter+=1

    def buildRootDir(self):
        root_directory_inode = self.getInode(2)
        self.current_dir_list = self.getDirectoryList(root_directory_inode)

    def getInode(self, num):
        num = num - 1 #there is not 0 inode so we shift what we asked for down to comply with FS
        inode_block_group = int(num/int(self.sb.s_inodes_per_group,16))
        inode_block_group_location = self.inode_tables_location_to_groups[inode_block_group]
        inode_inside_block_group = int(num%int(self.sb.s_inodes_per_group,16))
        inode_inside_block_group_location = inode_inside_block_group * int(self.sb.s_inode_size,16)
        inode_final_location = int(inode_block_group_location + inode_inside_block_group_location)

        #print(self.inode_tables_location_to_groups)
        #print(inode_block_group, inode_block_group_location, inode_inside_block_group, inode_inside_block_group_location)
        #print(inode_final_location, self.sb.block_size)
        
        newInode = inode.inode(getLocation(self.sb.s_inode_size, inode_final_location))
        #print(a.i_atime_date)
        #print(a.i_block)
        #print(int(a.directBlock0,16))
        #print(newInode.part)
        return newInode

    #pretty sure I am going to not do this... takes too much ram to build the full tree...
    def buildFileTree(self):
        #print('here2')
        root_directory_inode = self.getInode(2)
        #print(root_directory_inode.i_block_dict)
        #print(root_directory_inode.i_block)
        #builds tree root
        root_directory_list = self.getDirectoryList(root_directory_inode)

        tree_dict = self.recurBuildFileTree(root_directory_list)
        print(tree_dict)

    #since I am not building the tree... this gets to be deprecated....
    def recurBuildFileTree(self, dirs):
        files = []
        dir_dict = {}
        for dir in dirs:
            if dir.isFiletype() and partData.directory_type[int(dir.file_type,16)] == "Directory":
                newDirs = self.getDirectoryList(self.getInode(int(dir.inode,16)))
                dir_dict[dir] = self.recurBuildFileTree(newDirs)
            elif dir.isFiletype() == False:
                #TODO: handle if the directory has no filetype
                print("The directory has no filetype, this isn't handled yet.")
                sys.exit(0)
            else:
                files.append(dir)

        dir_dict['files'] = files
        return dir_dict

    def getDirectoryList(self, inode):
        blocksNeeded = []
        for single_i_block in inode.i_block_list:
            if single_i_block != False:
                blocksNeeded.append(int(single_i_block,16))
            else:
                break

        #print(inode.i_block)
        #print(inode.i_block_list) 
        #print(blocksNeeded)

        #TODO: URGENT: Add single, double, and triple redirects
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
            #print(len(raw_block))
            #print(raw_block[:90])
            count+=1
            newDir = directory.directory(raw_block,self.sb)
            directoryList.append(newDir)
            raw_block = raw_block[int(newDir.rec_len, 16)*2:]
        return directoryList

    def __init__(self, part):
        self.part = part['start']*512
        self.sb = superblock.superblock(getLocation(0x400, self.part + 0x400))
        self.my_filetree = filetree.filetree()
        self.buildGroupDescriptors()
        self.buildLocations()
        self.buildRootDir()

    #Here starts the things I can ask the filesystem after all this building
    def userCD(self, dir):
        if dir == '':
            self.buildRootDir()
            return 0 #operation successful return code

        for dir_object in self.current_dir_list:
            if dir == dir_object.decoded_name and dir_object.isFiletype() and partData.directory_type[int(dir_object.file_type, 16)] == 'Directory':
                self.userCDSwitchDir(dir_object)
                return 0 #operation successful return code
            elif dir_object.isFiletype() == False:
                return 1 #filetype operation not supported... your in trouble
            elif dir == dir_object.decoded_name and dir_object.isFiletype() and partData.directory_type[int(dir_object.file_type, 16)] != 'Directory':
                return 2 #Can not cd into file return code
        return 3 #can not find file return code

    def userCDSwitchDir(self, dir_object):
        new_directory_inode = self.getInode(int(dir_object.inode,16))
        self.current_dir_list = self.getDirectoryList(new_directory_inode)

    def userLS(self, long=False, inode=False):
        if long or inode:
            for dir_object in self.current_dir_list:
                if inode:
                    print(int(dir_object.inode,16), end='\t')
                if long:
                    dir_object_inode = self.getInode(int(dir_object.inode,16))
                    file_type = int(dir_object.file_type,16)
                    permission_bitmap = getBitmap(int(dir_object_inode.i_mode, 16), 12)
                    permission_string = 'x' if permission_bitmap[0] else '-'
                    permission_string += 'w' if permission_bitmap[1] else '-'
                    permission_string += 'r' if permission_bitmap[2] else '-'
                    permission_string += 'x' if permission_bitmap[3] else '-'
                    permission_string += 'w' if permission_bitmap[4] else '-'
                    permission_string += 'r' if permission_bitmap[5] else '-'
                    permission_string += 'x' if permission_bitmap[6] else '-'
                    permission_string += 'w' if permission_bitmap[7] else '-'
                    permission_string += 'r' if permission_bitmap[8] else '-'
                    permission_string += partData.directory_type_letter[file_type]
                    permission_string = permission_string[::-1]
                    permission_string = list(permission_string)
                    if permission_bitmap[9]:permission_string[0] = 'S'
                    if permission_bitmap[10]:permission_string[4] = 'S' 
                    if permission_bitmap[11]:permission_string[1] = 'S' 
                    permission_string = ''.join(permission_string)
                    uid = int(dir_object_inode.i_uid, 16)
                    gid = int(dir_object_inode.i_gid, 16)
                    size = int(dir_object_inode.i_size, 16)
                    i_atime = dir_object_inode.i_atime_date.split()
                    overall_time = ' '.join(i_atime[1:4])
                    print('{0}\t{1}\t{2}\t{3}\t{4}\t'.format(permission_string, uid, gid, size, overall_time) ,end='')
                print(dir_object.decoded_name)

        else:
            newline_counter = 0
            for dir_object in self.current_dir_list:
                if newline_counter >= 5:
                    print('')
                    newline_counter = 0
                print(dir_object.decoded_name+'\t\t', end='')
                newline_counter += 1
            print('')





