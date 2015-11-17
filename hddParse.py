from partHelp import *
import partData
from ext2.ext2 import ext2
from sys import exit

class hddParse:
    def __init__(self):
        ##
        # MBR partioning:
        #	part 1: 446 (16 bytes)
        ##
        print("Welcome to James Percival's ext2 filesystem parser")
        print("Please type 'help' for further information")
        self.currentDir = '/'
        self.parts = []
        self.partsFrame = []
        #iterate the 4 partitions and push the bytes into parts
        #TODO: add ability to parse extended partitions
        hexStr = getLocation(512, 0)
        for x in range(446,446+(16*4),16):
            self.parts.append(getHex(hexStr, x, x+16))
        for index, part in enumerate(parts):
            tempPartFrame = {}
            tempPartFrame['start']=int(littleEndian(getHex(part,8,12)), 16)
            tempPartFrame['end']=int(littleEndian(getHex(part,8,12)), 16) + int(littleEndian(getHex(part,12,16)), 16)-1
            tempPartFrame['size']=int(littleEndian(getHex(part,12,16)), 16)
            tempPartFrame['part_type']=partData.partition_type[getHex(part, 4)]
            self.partsFrame.append(tempPartFrame)
        self.filesystem = ext2(self.partsFrame[0])

    def acceptUserInput(self):
        while(1):
            print('>',end='')
            user_input = raw_input()
            self.parseInput(user_input)

    def parseInput(self, user_input):
        user_input = user_input.lower().lstrip()
        user_input_options = user_input.rstrip().split()[1:]
        user_input_options_len = len(user_input_options)
        if user_input == 'help':
            self.printHelp()
        elif user_input[:2] == 'cd':
            self.userCD(user_input_options[0]) if user_input_options_len > 0 else self.userCD()
        elif user_input[:2] == 'ls':
            self.userLS(user_input_options[0]) if user_input_options_len > 0 else self.userLS()
        elif user_input[:3] == 'pwd':
            self.userPWD()
        elif user_input[:4] == 'quit':
            self.userQUIT()

    def printHelp(self):
        print('help:\n\t\tPrints this message')
        print('cd:\t\tcd [dir]\n\t\tChange the shell working directory')
        print('ls:\t\tls [FILE]\n\t\tList information about the FILEs(current dir by default)')
        print('pwd:\t\tpwd\n\t\tPrints the name of the current working directory')
        print('quit:\t\tquit\n\t\tQuits out of the program')

    def userCD(self, dir='/'):
        dir = dir.replace('/', '').replace('\\', '').lower()
        returnCode = self.filesystem.userCD(dir)

        if returnCode == 0:
            self.currentDir += ''+ dir +'/'
        elif returnCode == 1:
            print('filetype operation not supported... your in trouble')
        elif returnCode == 2:
            print('Can not CD into file')
        elif returnCode == 3:
            print('Can not find file')

        if dir == '':
            self.currentDir = '/'

    def userLS(self, dir='/'):
        self.filesystem.userCD(dir)

    def userPWD(self):
        print(self.currentDir)

    def userQUIT(self):
        exit(0)