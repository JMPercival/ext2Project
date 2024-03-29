from partHelp import *
import time


class inode:
    def __init__(self, part):
        self.part = part
        self.i_mode= getHex(self.part, 0x0, 0x2, True)# /* File mode */
        self.i_uid= getHex(self.part, 0x2, 0x4, True)# /* Low 16 bits of Owner Uid */
        self.i_size= getHex(self.part, 0x4, 0x8, True)#/* Size in bytes */
        self.i_atime= getHex(self.part, 0x8, 0xc, True)#* Access time */
        self.i_ctime= getHex(self.part, 0xc, 0x10, True)#/* Creation time */
        self.i_mtime= getHex(self.part, 0x10, 0x14, True)#* Modification time */
        self.i_dtime= getHex(self.part, 0x14, 0x18, True)#* * Deletion Time */
        self.i_gid= getHex(self.part, 0x18, 0x1a, True)#* Low 16 bits of Group Id */
        self.i_links_count= getHex(self.part, 0x1a, 0x1c, True)#/* Links count */
        self.i_blocks= getHex(self.part, 0x1c, 0x20, True)#/* Blocks count */
        self.i_flags= getHex(self.part, 0x20, 0x24, True)#/* File flags */
        self.i_osd1= getHex(self.part, 0x24, 0x28, False)#/* OS dependent 1 */
        #TODO: emulate the union of structs for data in osd1
        #i_block big endian for now, I will flip the 32 bit values later
        self.i_block= getHex(self.part, 0x28, 0x64, False)#/* Pointers to blocks */
        self.i_generation= getHex(self.part, 0x64, 0x68, True)#/* File version (for NFS) */
        self.i_file_acl= getHex(self.part, 0x68, 0x7c, True)#/* File ACL */
        self.i_dir_acl= getHex(self.part, 0x7c, 0x80, True)#/* Directory ACL */
        self.i_faddr= getHex(self.part, 0x80, 0x84, True)#/* Fragment address */
        self.i_osd2= getHex(self.part, 0x84, 0x90, False)#/* OS dependent 2 */
        #TODO: emulate the union of structs for data in osd2

        ##MY VARS
        self.i_atime_date=time.ctime(int(self.i_atime,16))
        self.i_ctime_date=time.ctime(int(self.i_ctime,16))
        self.i_mtime_date=time.ctime(int(self.i_mtime,16))
        self.i_dtime_date=time.ctime(int(self.i_dtime,16))

        self.i_block_dict={
            'directBlock0' : getHex(self.i_block, 0x0, 0x4, True) if int(getHex(self.i_block, 0x0, 0x4, True),16) !=0 else False,
            'directBlock1' : getHex(self.i_block, 0x4, 0x8, True) if int(getHex(self.i_block, 0x4, 0x8, True),16) !=0 else False,
            'directBlock2' : getHex(self.i_block, 0x8, 0xc, True) if int(getHex(self.i_block, 0x8, 0xc, True),16) !=0 else False,
            'directBlock3' : getHex(self.i_block, 0xc, 0x10, True) if int(getHex(self.i_block, 0xc, 0x10, True),16) !=0 else False,            
            'directBlock4' : getHex(self.i_block, 0x10, 0x14, True) if int(getHex(self.i_block, 0x10, 0x14, True),16) !=0 else False,
            'directBlock5' : getHex(self.i_block, 0x14, 0x18, True) if int(getHex(self.i_block, 0x14, 0x18, True),16) !=0 else False,
            'directBlock6' : getHex(self.i_block, 0x18, 0x1c, True) if int(getHex(self.i_block, 0x18, 0x1c, True),16) !=0 else False,
            'directBlock7' : getHex(self.i_block, 0x1c, 0x20, True) if int(getHex(self.i_block, 0x1c, 0x20, True),16) !=0 else False,
            'directBlock8' : getHex(self.i_block, 0x20, 0x24, True) if int(getHex(self.i_block, 0x20, 0x24, True),16) !=0 else False,
            'directBlock9' : getHex(self.i_block, 0x24, 0x28, True) if int(getHex(self.i_block, 0x24, 0x28, True),16) !=0 else False,
            'directBlock10' : getHex(self.i_block, 0x28, 0x2c, True) if int(getHex(self.i_block, 0x28, 0x2c, True),16) !=0 else False,
            'directBlock11' : getHex(self.i_block, 0x2c, 0x30, True) if int(getHex(self.i_block, 0x2c, 0x30, True),16) !=0 else False,
            'singleIndirect' : getHex(self.i_block, 0x30, 0x34, True) if int(getHex(self.i_block, 0x30, 0x34, True),16) !=0 else False,
            'doubleIndirect' : getHex(self.i_block, 0x34, 0x38, True) if int(getHex(self.i_block, 0x34, 0x38, True),16) !=0 else False,
            'tripleIndirect' : getHex(self.i_block, 0x38, 0x3c, True) if int(getHex(self.i_block, 0x38, 0x3c, True),16) !=0 else False
        }
        self.i_block_list = [self.i_block_dict['directBlock0'], self.i_block_dict['directBlock1'],self.i_block_dict['directBlock2'],self.i_block_dict['directBlock3'],self.i_block_dict['directBlock4'],self.i_block_dict['directBlock5'],self.i_block_dict['directBlock6'],self.i_block_dict['directBlock7'],self.i_block_dict['directBlock8'],self.i_block_dict['directBlock9'],self.i_block_dict['directBlock10'],self.i_block_dict['directBlock11'],self.i_block_dict['singleIndirect'],self.i_block_dict['doubleIndirect'],self.i_block_dict['tripleIndirect']]

        self.reserved_inodes = {0:"Doesn't exist; there is no inode 0.",
                                1:"List of defective blocks.",
                                2:"Root directory.",
                                3:"User Quota",
                                4:"Group Quota",
                                5:"Boot Loader",
                                6:"Undelete Directory",
                                7:"Reserved Group Descriptors inode('resize inode')",
                                8:"Journal inode",
                                9:"The 'exclude' inode, for snapshots(?)",
                                10:'Replica inode, used for some non-upstream feature?'}

