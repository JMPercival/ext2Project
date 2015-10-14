from partHelp import *

class ext4:
	def __init__(self):
		#superblock is 1024 bytes
		#superblock is after 1024 bytes of padding and 512 bytes of MBR
		#TODO: GPT will be different, make this handle GPT
		self.superblock = getLocation(1024, 1024+512)
		#toal inode count
		self.s_inodes_count = getHex(self.superblock, 0, 4, True)
		#total block count
		self.s_blocks_count_lo = getHex(self.superblock, 4, 8, True)
		
		self.s_r_blocks_count_lo = getHex(self.superblock, 0, 4, True)

