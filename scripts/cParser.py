

def getEndBytes(inStr):
	num = ''
	le = False
	if 'le' in inStr:
		num = hex(int(int(inStr.split('le')[1])/8))
		le = True
	elif 'u' in inStr:
		num = hex(int(int(inStr.split('u')[1])/8))
	elif 'char' in inStr:
		num = hex(0x1)

	return [num,le]

x = open('fileToOpen', 'r')
f=x.readlines()
x.close()

print(f)
newFile = open('outfile','w')

currentHex = 0
for x in f:
    parts= x.split()
    hexPart = getEndBytes(parts[0])[0].split('x')[1]
    endHex = int(currentHex) + int(hexPart)
    #newFile.write
    newFile.write("self."+parts[1][:-1]+"= getHex(self.superblock, "+hex(currentHex)+", "+hex(endHex)+", "+str(getEndBytes(parts[0])[1])+")")
    newFile.write('#'+str(' '.join(parts[2:]))+'\n')
    currentHex = int(currentHex) + int( hexPart)

newFile.close()