from partHelp import *
import partData
from ext2.ext2 import ext2

##
# MBR partioning:
#	part 1: 446 (16 bytes)
##

hexStr = getLocation(512, 0)

parts = []
partsFrame = []
#iterate the 4 partitions and push the bytes into parts
#TODO: add ability to parse extended partitions
for x in range(446,446+(16*4),16):
	parts.append(getHex(hexStr, x, x+16))

for index, part in enumerate(parts):
	tempPartFrame = {}
	tempPartFrame['start']=int(littleEndian(getHex(part,8,12)), 16)
	tempPartFrame['end']=int(littleEndian(getHex(part,8,12)), 16) + int(littleEndian(getHex(part,12,16)), 16)-1
	tempPartFrame['size']=int(littleEndian(getHex(part,12,16)), 16)
	tempPartFrame['part_type']=partData.partition_type[getHex(part, 4)]
	partsFrame.append(tempPartFrame)

print(partsFrame)
a = ext2(partsFrame[1])
#a.buildGroupDescriptors()
#a.getInodeTables()
#a.getInode(2)
a.buildFileTree()
#print(a.s_last_error_block)

#take the second partition and start ext4 work on it
