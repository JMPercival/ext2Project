import binascii
from subprocess import Popen, PIPE 
from time import sleep

def littleEndian(hexStr):
	endStr = b''
	for x in range(0,len(hexStr), 2):
		#endStr = hexStr[x:x+2]
		endStr = hexStr[x:x+2] + endStr
	return endStr

def getHex(hexStr, start, end='', le=False):
	if end == '':
		end=start+1
	if le == False:
		return hexStr[start * 2 : end * 2]
	else:
		return littleEndian(hexStr[start * 2 : end * 2])

def getLocation(count, skip): #TODO: Add functionality to pass in the HDD I am looking at
	#hard coded as /dev/sda currently
	#bs is currently 1 because it lets me just around easier in the hard drive
	pro = Popen(['dd', 'if=ext2Copy', 'of=tmpfileForData', 'bs=1', 'count='+str(count), 'skip='+str(skip)], stderr=PIPE) #change this to take an input
	while pro.poll == None:
		sleep(.3)
	sleep(1)
	
	myoutput = open('tmpfileForData', 'rb')
	hexStr = binascii.hexlify(myoutput.read())

	return hexStr

#takes two integers and returns out a binary true/false list of numToReturn size
#!!RETURNS bitmap from low to high!!
def getBitmap(intToCheck, numToReturn):
    bitmap=bin(intToCheck)[::-1][:-2]
    newBitmap=[]
    for bit in bitmap:
        newBitmap.append(False if bit=='0' else True)
    leftOver = numToReturn - len(newBitmap)
    if leftOver > 0:
        while leftOver != 0:
            newBitmap.append(False)
            leftOver -= 1
    elif leftOver < 0:
        while leftOver != 0:
            newBitmap.pop()
            leftOver+=1
    return newBitmap