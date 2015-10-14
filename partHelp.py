import binascii
from subprocess import Popen, PIPE 
from time import sleep

def littleEndian(hexStr):
	endStr = ''
	for x in range(0,len(hexStr), 2):
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
	pro = Popen(['dd', 'if=/dev/sda', 'of=tmpfileForData', 'bs=1', 'count='+str(count), 'skip='+str(skip)], stderr=PIPE)
	while pro.poll == None:
		sleep(.3)
	sleep(1)
	
	myoutput = open('tmpfileForData', 'rb')
	hexStr = binascii.hexlify(myoutput.read())

	return hexStr
