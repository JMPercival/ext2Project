from partHelp import *

class ext4:
	def __init__(self, part):
		#superblock is 1024 bytes
		#superblock is after 1024 bytes of padding and 512 bytes of MBR
		#TODO: GPT will be different, make this handle GPT
		self.superblock = getLocation(1024, part['start']*512+1024)

		#####################################################333
		#All entires below have been scraped from the ext4 wiki#
		########################################################
		#Total inode count.
		self.s_inodes_count= getHex(self.superblock, 0x0, 0x4, True)
		#Total block count.
		self.s_blocks_count_lo= getHex(self.superblock, 0x4, 0x8, True)
		#This number of blocks can only be allocated by the super-user.
		self.s_r_blocks_count_lo= getHex(self.superblock, 0x8, 0xc, True)
		#Free block count.
		self.s_free_blocks_count_lo= getHex(self.superblock, 0xC, 0x10, True)
		#Free inode count.
		self.s_free_inodes_count= getHex(self.superblock, 0x10, 0x14, True)
		#First data block.  This must be at least 1 for 1k-block filesystems and is typically 0 for all other block sizes.
		self.s_first_data_block= getHex(self.superblock, 0x14, 0x18, True)
		#Block size is 2 ^ (10 + s_log_block_size).
		self.s_log_block_size= getHex(self.superblock, 0x18, 0x1c, True)
		#Cluster size is (2 ^ s_log_cluster_size) blocks if bigalloc is enabled, zero otherwise.
		self.s_log_cluster_size= getHex(self.superblock, 0x1C, 0x20, True)
		#Blocks per group.
		self.s_blocks_per_group= getHex(self.superblock, 0x20, 0x24, True)
		#Clusters per group, if bigalloc is enabled.
		self.s_clusters_per_group= getHex(self.superblock, 0x24, 0x28, True)
		#Inodes per group.
		self.s_inodes_per_group= getHex(self.superblock, 0x28, 0x2c, True)
		#Mount time, in seconds since the epoch.
		self.s_mtime= getHex(self.superblock, 0x2C, 0x30, True)
		#Write time, in seconds since the epoch.
		self.s_wtime= getHex(self.superblock, 0x30, 0x34, True)
		#Number of mounts since the last fsck.
		self.s_mnt_count= getHex(self.superblock, 0x34, 0x36, True)
		#Number of mounts beyond which a fsck is needed.
		self.s_max_mnt_count= getHex(self.superblock, 0x36, 0x38, True)
		#Magic signature, 0xEF53
		self.s_magic= getHex(self.superblock, 0x38, 0x3a, True)
		#None
		self.s_state= getHex(self.superblock, 0x3A, 0x3c, True)
		#None
		self.s_errors= getHex(self.superblock, 0x3C, 0x3e, True)
		#Minor revision level.
		self.s_minor_rev_level= getHex(self.superblock, 0x3E, 0x40, True)
		#Time of last check, in seconds since the epoch.
		self.s_lastcheck= getHex(self.superblock, 0x40, 0x44, True)
		#Maximum time between checks, in seconds.
		self.s_checkinterval= getHex(self.superblock, 0x44, 0x48, True)
		#None
		self.s_creator_os= getHex(self.superblock, 0x48, 0x4c, True)
		#None
		self.s_rev_level= getHex(self.superblock, 0x4C, 0x50, True)
		#Default uid for reserved blocks.
		self.s_def_resuid= getHex(self.superblock, 0x50, 0x52, True)
		#Default gid for reserved blocks.
		self.s_def_resgid= getHex(self.superblock, 0x52, 0x54, True)
		#First non-reserved inode.
		self.s_first_ino= getHex(self.superblock, 0x54, 0x58, True)
		#Size of inode structure, in bytes.
		self.s_inode_size= getHex(self.superblock, 0x58, 0x5a, True)
		#Block group # of this superblock.
		self.s_block_group_nr= getHex(self.superblock, 0x5A, 0x5c, True)
		#None
		self.s_feature_compat= getHex(self.superblock, 0x5C, 0x60, True)
		#None
		self.s_feature_incompat= getHex(self.superblock, 0x60, 0x64, True)
		#None
		self.s_feature_ro_compat= getHex(self.superblock, 0x64, 0x68, True)
		#128-bit UUID for volume. [16]
		self.s_uuid= getHex(self.superblock, 0x68, 0x69, False)
		#Volume label. [16]
		self.s_volume_name= getHex(self.superblock, 0x78, 0x79, False)
		#Directory where filesystem was last mounted. [64]
		self.s_last_mounted= getHex(self.superblock, 0x88, 0x89, False)
		#For compression (Not used in e2fsprogs/Linux)
		self.s_algorithm_usage_bitmap= getHex(self.superblock, 0xC8 , 0xcc, True)
		## of blocks to try to preallocate for ... files? (Not used in e2fsprogs/Linux)
		self.s_prealloc_blocks= getHex(self.superblock, 0xCC, 0xcd, False)
		## of blocks to preallocate for directories. (Not used in e2fsprogs/Linux)
		self.s_prealloc_dir_blocks= getHex(self.superblock, 0xCD, 0xce, False)
		#Number of reserved GDT entries for future filesystem expansion.
		self.s_reserved_gdt_blocks= getHex(self.superblock, 0xCE, 0xd0, True)
		#UUID of journal superblock  [16]
		self.s_journal_uuid= getHex(self.superblock, 0xD0, 0xd1, False)
		#inode number of journal file.
		self.s_journal_inum= getHex(self.superblock, 0xE0, 0xe4, True)
		#Device number of journal file, if the external journal feature flag is set.
		self.s_journal_dev= getHex(self.superblock, 0xE4, 0xe8, True)
		#Start of list of orphaned inodes to delete.
		self.s_last_orphan= getHex(self.superblock, 0xE8, 0xec, True)
		#HTREE hash seed.  [4]
		self.s_hash_seed= getHex(self.superblock, 0xEC, 0xf0, True)
		#None
		self.s_def_hash_version= getHex(self.superblock, 0xFC, 0xfd, False)
		#None
		self.s_jnl_backup_type= getHex(self.superblock, 0xFD, 0xfe, False)
		#Size of group descriptors, in bytes, if the 64bit incompat feature flag is set.
		self.s_desc_size= getHex(self.superblock, 0xFE, 0x100, True)
		#None
		self.s_default_mount_opts= getHex(self.superblock, 0x100, 0x104, True)
		#First metablock block group, if the meta_bg feature is enabled.
		self.s_first_meta_bg= getHex(self.superblock, 0x104, 0x108, True)
		#When the filesystem was created, in seconds since the epoch.
		self.s_mkfs_time= getHex(self.superblock, 0x108, 0x10c, True)
		#None  [17]
		self.s_jnl_blocks= getHex(self.superblock, 0x10C, 0x110, True)
		#High 32-bits of the block count.
		self.s_blocks_count_hi= getHex(self.superblock, 0x150, 0x154, True)
		#High 32-bits of the reserved block count.
		self.s_r_blocks_count_hi= getHex(self.superblock, 0x154, 0x158, True)
		#High 32-bits of the free block count.
		self.s_free_blocks_count_hi= getHex(self.superblock, 0x158, 0x15c, True)
		#All inodes have at least # bytes.
		self.s_min_extra_isize= getHex(self.superblock, 0x15C, 0x15e, True)
		#New inodes should reserve # bytes.
		self.s_want_extra_isize= getHex(self.superblock, 0x15E, 0x160, True)
		#None
		self.s_flags= getHex(self.superblock, 0x160, 0x164, True)
		#RAID stride.  This is the number of logical blocks read from or written to the disk before moving to the next disk.  This affects the placement of filesystem metadata, which will hopefully make RAID storage faster.
		self.s_raid_stride= getHex(self.superblock, 0x164, 0x166, True)
		## seconds to wait in multi-mount prevention (MMP) checking.  In theory, MMP is a mechanism to record in the superblock which host and device have mounted the filesystem, in order to prevent multiple mounts.  This feature does not seem to be implemented...
		self.s_mmp_interval= getHex(self.superblock, 0x166, 0x168, True)
		#Block # for multi-mount protection data.
		self.s_mmp_block= getHex(self.superblock, 0x168, 0x170, True)
		#RAID stripe width.  This is the number of logical blocks read from or written to the disk before coming back to the current disk.  This is used by the block allocator to try to reduce the number of read-modify-write operations in a RAID5/6.
		self.s_raid_stripe_width= getHex(self.superblock, 0x170, 0x174, True)
		#None
		self.s_log_groups_per_flex= getHex(self.superblock, 0x174, 0x175, False)
		#Metadata checksum algorithm type.  The only valid value is 1 (crc32c).
		self.s_checksum_type= getHex(self.superblock, 0x175, 0x176, False)
		#
		self.s_reserved_pad= getHex(self.superblock, 0x176, 0x178, True)
		#Number of KiB written to this filesystem over its lifetime.
		self.s_kbytes_written= getHex(self.superblock, 0x178, 0x180, True)
		#inode number of active snapshot. (Not used in e2fsprogs/Linux.)
		self.s_snapshot_inum= getHex(self.superblock, 0x180, 0x184, True)
		#Sequential ID of active snapshot. (Not used in e2fsprogs/Linux.)
		self.s_snapshot_id= getHex(self.superblock, 0x184, 0x188, True)
		#Number of blocks reserved for active snapshot's future use. (Not used in e2fsprogs/Linux.)
		self.s_snapshot_r_blocks_count= getHex(self.superblock, 0x188, 0x190, True)
		#inode number of the head of the on-disk snapshot list. (Not used in e2fsprogs/Linux.)
		self.s_snapshot_list= getHex(self.superblock, 0x190, 0x194, True)
		#Number of errors seen.
		self.s_error_count= getHex(self.superblock, 0x194, 0x198, True)
		#First time an error happened, in seconds since the epoch.
		self.s_first_error_time= getHex(self.superblock, 0x198, 0x19c, True)
		#inode involved in first error.
		self.s_first_error_ino= getHex(self.superblock, 0x19C, 0x1a0, True)
		#Number of block involved of first error.
		self.s_first_error_block= getHex(self.superblock, 0x1A0, 0x1a8, True)
		#Name of function where the error happened.  [32]
		self.s_first_error_func= getHex(self.superblock, 0x1A8, 0x1a9, False)
		#Line number where error happened.
		self.s_first_error_line= getHex(self.superblock, 0x1C8, 0x1cc, True)
		#Time of most recent error, in seconds since the epoch.
		self.s_last_error_time= getHex(self.superblock, 0x1CC, 0x1d0, True)
		#inode involved in most recent error.
		self.s_last_error_ino= getHex(self.superblock, 0x1D0, 0x1d4, True)
		#Line number where most recent error happened.
		self.s_last_error_line= getHex(self.superblock, 0x1D4, 0x1d8, True)
		#Number of block involved in most recent error.
		self.s_last_error_block= getHex(self.superblock, 0x1D8, 0x1e0, True)
		#Name of function where the most recent error happened.  [32]
		self.s_last_error_func= getHex(self.superblock, 0x1E0, 0x1e1, False)
		#ASCIIZ string of mount options.  [64]
		self.s_mount_opts= getHex(self.superblock, 0x200, 0x201, False)
		#None
		self.s_usr_quota_inum= getHex(self.superblock, 0x240, 0x244, True)
		#None
		self.s_grp_quota_inum= getHex(self.superblock, 0x244, 0x248, True)
		#Overhead blocks/clusters in fs. (Huh? This field is always zero, which means that the kernel calculates it dynamically.)
		self.s_overhead_blocks= getHex(self.superblock, 0x248, 0x24c, True)
		#Block groups containing superblock backups (if sparse_super2) [2]
		self.s_backup_bgs= getHex(self.superblock, 0x24C, 0x250, True)
		#None  [4]
		self.s_encrypt_algos= getHex(self.superblock, 0x254, 0x255, False)
		#Salt for the string2key algorithm for encryption. [16]
		self.s_encrypt_pw_salt= getHex(self.superblock, 0x258, 0x259, False)
		#Inode number of lost+found
		self.s_lpf_ino= getHex(self.superblock, 0x268, 0x26c, True)
		#Checksum seed used for metadata_csum calculations.  This value is crc32c(~0, $orig_fs_uuid).
		self.s_checksum_seed= getHex(self.superblock, 0x26C, 0x270, True)
		#Padding to the end of the block. [99]
		self.s_reserved= getHex(self.superblock, 0x270, 0x274, True)
		#Superblock checksum.
		self.s_checksum= getHex(self.superblock, 0x3FC, 0x400, True)

		#My calculated Vars
		self.block_size = 2**(int(self.s_log_block_size,16)+10)
		self.block_desc_size = 32 if int(self.s_desc_size, 16) == 0 else self.s_desc_size
	

	def iterBlockGroups(self, blockGroup=''):
		if blockGroup == '':
			#return a generator of all the block groups to iterate
			for block in range(int(self.s_blocks_count_lo, 16)):
				pass
		else:
			#return the block group asked for
			pass	
