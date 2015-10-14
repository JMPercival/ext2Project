

from partHelp import *
import partData

##
# MBR partioning:
#	part 1: 446 (16 bytes)
##

hexStr = getLocation(512, 0)

parts = []
#iterate the 4 partitions and push the bytes into parts
#TODO: add ability to parse extended partitions
for x in range(446,446+(16*4),16):
	parts.append(getHex(hexStr, x, x+16))

for part in parts:
	print 'Part Start: '+ str(int(littleEndian(getHex(part,8,12)), 16)) 
	print 'Part End: ' + str(int(littleEndian(getHex(part,8,12)), 16) + int(littleEndian(getHex(part,12,16)), 16)-1) 
	print 'Part Size ' + str(int(littleEndian(getHex(part,12,16)), 16)) 
	print 'Part Type: '+partData.partition_type[getHex(part, 4)]
	print '\n' 


#take the second partition and start ext4 work on it
