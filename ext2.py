from math import log, ceil
from partHelp import *

class ext2:
    def compatFeatures(self):
        self.s_feature_compat_dict={}
        # Block pre-allocation for new directories
        #(Preallocate some number of (contiguous?) blocks (see byte 205 in the superblock)
        #   to a directory when creating a new one (to reduce fragmentation?))
        self.s_feature_compat_dict['EXT2_FEATURE_COMPAT_DIR_PREALLOC'], \
        # AFS server inodes exist
        self.s_feature_compat_dict['EXT2_FEATURE_COMPAT_IMAGIC_INODES'], \
        # File system has a journal (Ext3)
        self.s_feature_compat_dict['EXT3_FEATURE_COMPAT_HAS_JOURNAL'], \
        # Inodes have extended attributes
        self.s_feature_compat_dict['EXT2_FEATURE_COMPAT_EXT_ATTR'], \
        # Non-standard inode size used (File system can resize itself for larger partitions)
        self.s_feature_compat_dict['EXT2_FEATURE_COMPAT_RESIZE_INO'], \
        # Directory indexing (HTree) (Directories use hash index) 
        self.s_feature_compat_dict['EXT2_FEATURE_COMPAT_DIR_INDEX']  \
        = getBitmap(int(self.s_feature_compat, 16), 6)

    def incompatFeatures(self):
        self.s_feature_incompat_dict={}
        # Disk/File compression is used
        self.s_feature_incompat_dict['EXT2_FEATURE_INCOMPAT_COMPRESSION'], \
        # Directory entries contain a type field
        self.s_feature_incompat_dict['EXT2_FEATURE_INCOMPAT_FILETYPE'], \
        # File system needs to replay its journal
        self.s_feature_incompat_dict['EXT3_FEATURE_INCOMPAT_RECOVER'], \
        # File system uses a journal device
        self.s_feature_incompat_dict['EXT3_FEATURE_INCOMPAT_JOURNAL_DEV'], \
        # None (Possibly not supported?)
        self.s_feature_incompat_dict['EXT2_FEATURE_INCOMPAT_META_BG'], \
        = getBitmap(int(self.s_feature_incompat, 16), 5) 

    def roFeatures(self): 
        self.s_feature_ro_compat_dict={}
        # Sparse superblocks and group descriptor tables
        self.s_feature_ro_compat_dict['EXT2_FEATURE_RO_COMPAT_SPARSE_SUPER'], \
        # Large file support, 64-bit file size
        self.s_feature_ro_compat_dict['EXT2_FEATURE_RO_COMPAT_LARGE_FILE'], \
        # Binary tree sorted directory files 
        self.s_feature_ro_compat_dict['EXT2_FEATURE_RO_COMPAT_BTREE_DIR'], \
        = getBitmap(int(self.s_feature_ro_compat, 16), 3)

    def __init__(self, part):
        #superblock is 1024 bytes
        #superblock is after 1024 bytes of padding and 512 bytes of MBR
        #TODO: GPT will be different, make this handle GPT
        self.superblock = getLocation(1024, part['start']*512+1024)

        #####################################################333
        #All entires below have been scraped from the ext4 wiki#
        ########################################################
        #Total inode count.
        self.s_inodes_count= getHex(self.superblock, 0x0, 0x4, True)#/* Inodes count */
        self.s_blocks_count= getHex(self.superblock, 0x4, 0x8, True)#/* Blocks count */
        self.s_r_blocks_count= getHex(self.superblock, 0x8, 0xc, True)#/* Reserved blocks count */
        self.s_free_blocks_count= getHex(self.superblock, 0xc, 0x10, True)#/* Free blocks count */
        self.s_free_inodes_count= getHex(self.superblock, 0x10, 0x14, True)#/* Free inodes count */
        self.s_first_data_block= getHex(self.superblock, 0x14, 0x18, True)#/* First Data Block */
        self.s_log_block_size= getHex(self.superblock, 0x18, 0x1c, True)#/* Block size */
        self.s_log_frag_size= getHex(self.superblock, 0x1c, 0x20, True)#/* Fragment size */
        self.s_blocks_per_group= getHex(self.superblock, 0x20, 0x24, True)#/* # Blocks per group */
        self.s_frags_per_group= getHex(self.superblock, 0x24, 0x28, True)#/* # Fragments per group */
        self.s_inodes_per_group= getHex(self.superblock, 0x28, 0x2c, True)#/* # Inodes per group */
        self.s_mtime= getHex(self.superblock, 0x2c, 0x30, True)#/* Mount time */
        self.s_wtime= getHex(self.superblock, 0x30, 0x34, True)#/* Write time */
        self.s_mnt_count= getHex(self.superblock, 0x34, 0x36, True)#/* Mount count */
        self.s_max_mnt_count= getHex(self.superblock, 0x36, 0x38, True)#/* Maximal mount count */
        self.s_magic= getHex(self.superblock, 0x38, 0x3a, True)#/* Magic signature */
        self.s_state= getHex(self.superblock, 0x3a, 0x3c, True)#/* File system state */
        self.s_errors= getHex(self.superblock, 0x3c, 0x3e, True)#/* Behaviour when detecting errors */
        self.s_minor_rev_level= getHex(self.superblock, 0x3e, 0x40, True)#/* minor revision level */
        self.s_lastcheck= getHex(self.superblock, 0x40, 0x44, True)#/* time of last check */
        self.s_checkinterval= getHex(self.superblock, 0x44, 0x48, True)#/* max. time between checks */
        self.s_creator_os= getHex(self.superblock, 0x48, 0x4c, True)#/* OS */
        self.s_rev_level= getHex(self.superblock, 0x4c, 0x50, True)#/* Revision level */
        self.s_def_resuid= getHex(self.superblock, 0x50, 0x52, True)#/* Default uid for reserved blocks */
        self.s_def_resgid= getHex(self.superblock, 0x52, 0x54, True)#/* Default gid for reserved blocks */
        self.s_first_ino= getHex(self.superblock, 0x54, 0x58, True)#/* First non-reserved inode */
        self.s_inode_size= getHex(self.superblock, 0x58, 0x5a, True)#/* size of inode structure */
        self.s_block_group_nr= getHex(self.superblock, 0x5a, 0x5c, True)#/* block group # of this superblock */
        self.s_feature_compat= getHex(self.superblock, 0x5c, 0x60, True)#/* compatible feature set */
        self.s_feature_incompat= getHex(self.superblock, 0x60, 0x64, True)#/* incompatible feature set */
        self.s_feature_ro_compat= getHex(self.superblock, 0x64, 0x68, True)#/* readonly-compatible feature set */
        self.s_uuid= getHex(self.superblock, 0x68, 0x78, False)#/* 128-bit uuid for volume */
        self.s_volume_name= getHex(self.superblock, 0x78, 0x88, False)#/* volume name */
        self.s_last_mounted= getHex(self.superblock, 0x88, 0xc8, False)#/* directory where last mounted */
        self.s_algorithm_usage_bitmap= getHex(self.superblock, 0xc8, 0xcc, True)#/* For compression */ [NOTE: also called s_also_bitmap]
        self.s_prealloc_blocks= getHex(self.superblock, 0xcc, 0xcd, False)#/* Nr of blocks to try to preallocate*/
        self.s_prealloc_dir_blocks= getHex(self.superblock, 0xcd, 0xce, False)#/* Nr to preallocate for dirs */
        self.s_padding1= getHex(self.superblock, 0xce, 0xd0, False)#
        self.s_journal_uuid= getHex(self.superblock, 0xd0, 0xe0, False)#/* uuid of journal superblock */
        self.s_journal_inum= getHex(self.superblock, 0xe0, 0xe4, False)#/* inode number of journal file */
        self.s_journal_dev= getHex(self.superblock, 0xe4, 0xe8, False)#/* device number of journal file */
        self.s_last_orphan= getHex(self.superblock, 0xe8, 0xec, False)#/* start of list of inodes to delete */
        self.s_hash_seed= getHex(self.superblock, 0xec, 0xfc, False)#/* HTREE hash seed */
        self.s_def_hash_version= getHex(self.superblock, 0xfc, 0xfd, False)#/* Default hash version to use */
        self.s_reserved_char_pad= getHex(self.superblock, 0xfd, 0x100, False)#/* None */ #These two are the same?
        self.s_reserved_word_pad= getHex(self.superblock, 0xfd, 0x100, False)#/* None */ #These two are the same?
        self.s_default_mount_opts= getHex(self.superblock, 0x100, 0x104, True)#/* None */
        self.s_first_meta_bg= getHex(self.superblock, 0x104, 0x108, True)#/* First metablock block group */
        self.s_reserved= getHex(self.superblock, 0x108, 0x400, False)#/* Padding to the end of the block [190]? */

        ##MY VARS##
        self.desc_block_num=int(self.s_blocks_count,16) / int(self.s_blocks_per_group, 16)
        self.desc_blocks_with_super = set([0,1]+[3**x for x in range(1,int(ceil(log(self.desc_block_num,3))))] +\
            [5**x for x in range(1,int(ceil(log(self.desc_block_num,5))))] + \
            [7**x for x in range(1,int(ceil(log(self.desc_block_num,7))))])

        self.compatFeatures()
        self.incompatFeatures()
        self.roFeatures()



