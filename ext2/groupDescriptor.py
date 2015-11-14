from partHelp import *

class groupDescriptor:
    def __init__(self, part):
        self.part = part
        self.bg_block_bitmap= getHex(self.part, 0x0, 0x4, True)#/* Block address of block usage bitmap */
        self.bg_inode_bitmap= getHex(self.part, 0x4, 0x8, True)#/* Block address of inode usage bitmap */
        self.bg_inode_table= getHex(self.part, 0x8, 0xc, True)#/* Starting block address of inode table */
        self.bg_free_blocks_count= getHex(self.part, 0xc, 0xe, True)#/* Number of unallocated blocks in group */
        self.bg_free_inodes_count= getHex(self.part, 0xe, 0x10, True)#/* Number of unallocated inodes in group */
        self.bg_used_dirs_count= getHex(self.part, 0x10, 0x12, True)#/* Number of directories in group */
        self.bg_pad= getHex(self.part, 0x12, 0x14, False)#/* pad */
        self.bg_reserved= getHex(self.part, 0x14, 0x20, False)#/* unused */
