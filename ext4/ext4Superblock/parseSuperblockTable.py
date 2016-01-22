from bs4 import BeautifulSoup

r=open('ext4SuperBlock','r')
s = BeautifulSoup(r.read(), "html.parser")
r.close()

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

ps = ''
count = 0
for tr in s.find_all(['tr']):
	try:
		td = tr.find_all(['td'])
		ps += '#' + str(td[3].string).replace('\n', '')
		ps += '\n'
		ps += 'self.' + str(td[2].string) + '= getHex(self.superblock, ' + str(td[0].string) + ', '
		end = getEndBytes(td[1].string)
		firstHex = td[0].string.split('x')[1]
		firstHex = int(firstHex,16)
		firstHex = hex(firstHex)
		secondHex = end[0]
		totalHex = int(firstHex,16) + int(secondHex,16)
		ps += hex(totalHex)
		ps += ', ' + str(end[1]) + ')' + '\n'
		count +=1
	except IndexError as a:
		pass
print(ps)
