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

        self.directBlock0 = getHex(self.i_block, 0x0, 0x4, True)
        self.directBlock1 = getHex(self.i_block, 0x4, 0x8, True)
        self.directBlock2 = getHex(self.i_block, 0x8, 0xc, True)
        self.directBlock3 = getHex(self.i_block, 0xc, 0x10, True)
        self.directBlock4 = getHex(self.i_block, 0x10, 0x14, True)
        self.directBlock5 = getHex(self.i_block, 0x14, 0x18, True)
        self.directBlock6 = getHex(self.i_block, 0x18, 0x1c, True)
        self.directBlock7 = getHex(self.i_block, 0x1c, 0x20, True)
        self.directBlock8 = getHex(self.i_block, 0x20, 0x24, True)
        self.directBlock9 = getHex(self.i_block, 0x24, 0x28, True)
        self.directBlock10 = getHex(self.i_block, 0x28, 0x2c, True)
        self.directBlock11 = getHex(self.i_block, 0x2c, 0x30, True)
        self.singleIndirect = getHex(self.i_block, 0x30, 0x34, True)
        self.doubleIndirect = getHex(self.i_block, 0x34, 0x38, True)
        self.tripleIndirect = getHex(self.i_block, 0x38, 0x3c, True)



        self.reserved_inodes = {0:"Doesn't exist; there is no inode 0.",1:"List of defective blocks.",
                                2:"Root directory.",
                                3:"User Quota",
                                4:"Group Quota",
                                5:"Boot Loader",
                                6:"Undelete Directory",
                                7:"Reserved Group Descriptors inode('resize inode')",
                                8:"Journal inode",
                                9:"The 'exclude' inode, for snapshots(?)",
                                10:'Replica inode, used for some non-upstream feature?'}
