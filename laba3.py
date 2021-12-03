import struct


class BdfFont():
    _strFontBoundingBox = "FONTBOUNDINGBOX"
    _strStartChar = "STARTCHAR"
    _strEndChar = "ENDCHAR"
    _strBitMap = "BITMAP"
    _strEncoding = "ENCODING"

    def __init__(self):
        self.strEncodingNumber = self._strEncoding + " "
        self.bitmap = []
        self.shiftedBitmap = []
        self.width = 0
        self.height = 0
        self.xoffset = 0
        self.yoffset = 0
        self.flagEncodeExist = False

    def setEncodingNumber(self, number):
        try:
            if number.startswith("0x"):
                self.intEncodingNumber = int(number, 16)
            else:
                self.intEncodingNumber = int(number)

        except ValueError:
            print("Invalid input number")
            exit()
        self.strEncodingNumber = \
            self._strEncoding + " " + str(self.intEncodingNumber)

    def setFontFormatParameters(self, dataFile):
        for self.extractLine in dataFile:
            self.extractLine = self.extractLine.strip()
            if self.extractLine.startswith(self._strFontBoundingBox):
                self.tempFontBoundBox = self.extractLine
                break
        self.listFontBoundingBox = self.tempFontBoundBox.split()
        self.windowWidth = int(self.listFontBoundingBox[1])
        self.windowHeight = int(self.listFontBoundingBox[2])
        self.windowXoffset = int(self.listFontBoundingBox[3])
        self.windowYoffset = int(self.listFontBoundingBox[4])

    def setFontParameters(self, bbx):
        self.tempList = bbx.split()
        self.width = int(self.tempList[1])
        self.height = int(self.tempList[2])
        self.xoffset = int(self.tempList[3])
        self.yoffset = int(self.tempList[4])

    def bitmapArrayZeroClear(self):
        self.bitmapArray = []
        for self.m in range(self.windowHeight):
            self.tempList = []
            for self.n in range(self.windowWidth):
                self.tempList.append(0)
            self.bitmapArray.append(self.tempList)
        return self.bitmapArray

    def bitmapList2Array(self, bitmapList):
        self.bitmap = []
        for self.m in range(len(bitmapList)):
            self.bitData = int(bitmapList[self.m], 16)
            self.temp = self.bitData
            self.tempList = []
            if self.width > 9:
                self.shiftBits = 16 - 1
            else:
                self.shiftBits = 8 - 1

            for self.n in range(self.width):
                self.bit = (1 << (self.shiftBits)) & self.temp
                self.temp = self.temp << 1
                if self.bit == (1 << (self.shiftBits)):
                    self.tempList.append(1)
                else:
                    self.tempList.append(0)
            self.bitmap.append(self.tempList)

    def printBitmap(self, charBitOne="*", charBitZero="-"):
        if not self.flagEncodeExist:
            print("No Encode Number")
            return

        for self.m in range(self.height):
            self.temp = ""
            for self.n in range(self.width):
                if self.bitmap[self.m][self.n] == 1:
                    self.temp = self.temp + charBitOne
                else:
                    self.temp = self.temp + charBitZero
            print(self.temp)

    def printShiftedBitmap(self, charBitOne="*", charBitZero="-"):
        if not self.flagEncodeExist:
            print("No Encode Number")
            return

        for self.m in range(self.windowHeight):
            self.temp = ""
            for self.n in range(self.windowWidth):
                if self.shiftedBitmap[self.m][self.n] == 1:
                    self.temp = self.temp + charBitOne
                else:
                    self.temp = self.temp + charBitZero
            print(self.temp)

    def getFontBitmap(self, dataFile, encoding):
        self.setEncodingNumber(encoding)
        self.extractedList = []
        self.flagFound = False
        self.flagNeverFound = True
        for self.extractLine in dataFile:
            self.extractLine = self.extractLine.strip()
            if self.extractLine == self.strEncodingNumber:
                self.flagFound = True
                self.flagNeverFound = False
            if self.extractLine == self._strEndChar:
                self.flagFound = False
            if self.flagFound:
                self.extractedList.append(self.extractLine)
        if not self.flagNeverFound:
            self.setFontParameters(self.extractedList[3])
            self.bitmapList2Array(self.extractedList[5:])
            self.flagEncodeExist = True
        else:
            self.bitmap = self.bitmapArrayZeroClear()
            self.flagEncodeExist = False
            # print(self.extractedList)

    def shiftBitmap(self):
        self.shiftedBitmap = self.bitmapArrayZeroClear()
        if not self.flagEncodeExist:
            return

        for self.m in range(self.windowHeight):
            for self.n in range(self.windowWidth):
                self.bitmap_x = self.n - self.xoffset + self.windowXoffset
                self.bitmap_y = \
                    self.m + self.yoffset\
                    - self.windowYoffset + (self.height - self.windowHeight)
                if self.bitmap_x >= 0 and self.bitmap_x < self.width:
                    if self.bitmap_y >= 0 and self.bitmap_y < self.height:
                        self.shiftedBitmap[self.m][self.n] = \
                            self.bitmap[self.bitmap_y][self.bitmap_x]

    def getLetterArray(self, letter, dataFile):
        self.getFontBitmap(dataFile, str(ord(letter)).strip())
        self.shiftBitmap()

        if not self.flagEncodeExist:
            print("No Encode Number")
            return

        self.tempLetter = []
        for self.m in range(self.windowHeight):
            self.tempRow = []
            for self.n in range(self.windowWidth):
                self.tempRow.append(self.shiftedBitmap[self.m][self.n])
            self.tempLetter.append(self.tempRow)
        return self.tempLetter

    def getWordArray(self, word, dataFile, height=18):
        self.tempWord = height * [[]]
        for self.letter in word:
            self.letterArray = self.getLetterArray(self.letter, dataFile)
            for self.i in range(height):
                self.tempWord[self.i] = \
                    self.tempWord[self.i] + self.letterArray[self.i]
        return self.tempWord


def WriteHexString(f_param, hex_param):
    while hex_param != '':
        num = int(hex_param[0:2], 16)
        f_param.write(struct.pack('>B', num))
        hex_param = hex_param[2:]


def writeTIFF(wordArray):
    f = open('temp.tiff', 'wb')

    offset = 0
    nx = len(wordArray[0])
    ny = len(wordArray)
    WriteHexString(f, "4d4d002a")
    offset = nx * ny * 3 + 8
    f.write(struct.pack('>B', ((offset & 0xff000000) // 16777216)))
    f.write(struct.pack('>B', ((offset & 0x00ff0000) // 65536)))
    f.write(struct.pack('>B', ((offset & 0x0000ff00) // 256)))
    f.write(struct.pack('>B', ((offset & 0x000000ff))))

    for j in range(ny):
        for i in range(nx):
            if (wordArray[j][i] == 0):
                f.write(struct.pack('>B', (255)))
                f.write(struct.pack('>B', (255)))
                f.write(struct.pack('>B', (255)))
            else:
                f.write(struct.pack('>B', (0)))
                f.write(struct.pack('>B', (0)))
                f.write(struct.pack('>B', (0)))

    WriteHexString(f, "000e")

    WriteHexString(f, "0100000300000001")
    f.write(struct.pack('>B', ((nx & 0xff00) // 256)))
    f.write(struct.pack('>B', ((nx & 0x00ff))))
    WriteHexString(f, "0000")

    WriteHexString(f, "0101000300000001")
    f.write(struct.pack('>B', ((ny & 0xff00) // 256)))
    f.write(struct.pack('>B', ((ny & 0x00ff))))
    WriteHexString(f, "0000")

    WriteHexString(f, "0102000300000003")
    offset = nx * ny * 3 + 182
    f.write(struct.pack('>B', ((offset & 0xff000000) // 16777216)))
    f.write(struct.pack('>B', ((offset & 0x00ff0000) // 65536)))
    f.write(struct.pack('>B', ((offset & 0x0000ff00) // 256)))
    f.write(struct.pack('>B', ((offset & 0x000000ff))))

    WriteHexString(f, "010300030000000100010000")

    WriteHexString(f, "010600030000000100020000")

    WriteHexString(f, "011100040000000100000008")

    WriteHexString(f, "011200030000000100010000")

    WriteHexString(f, "011500030000000100030000")

    WriteHexString(f, "0116000300000001")
    f.write(struct.pack('>B', ((ny & 0xff00) // 256)))
    f.write(struct.pack('>B', ((ny & 0x00ff))))
    WriteHexString(f, "0000")

    WriteHexString(f, "0117000400000001")
    offset = nx * ny * 3
    f.write(struct.pack('>B', ((offset & 0xff000000) // 16777216)))
    f.write(struct.pack('>B', ((offset & 0x00ff0000) // 65536)))
    f.write(struct.pack('>B', ((offset & 0x0000ff00) // 256)))
    f.write(struct.pack('>B', ((offset & 0x000000ff))))

    WriteHexString(f, "0118000300000003")
    offset = nx * ny * 3 + 188
    f.write(struct.pack('>B', ((offset & 0xff000000) // 16777216)))
    f.write(struct.pack('>B', ((offset & 0x00ff0000) // 65536)))
    f.write(struct.pack('>B', ((offset & 0x0000ff00) // 256)))
    f.write(struct.pack('>B', ((offset & 0x000000ff))))

    WriteHexString(f, "0119000300000003")
    offset = nx * ny * 3 + 194
    f.write(struct.pack('>B', ((offset & 0xff000000) // 16777216)))
    f.write(struct.pack('>B', ((offset & 0x00ff0000) // 65536)))
    f.write(struct.pack('>B', ((offset & 0x0000ff00) // 256)))
    f.write(struct.pack('>B', ((offset & 0x000000ff))))

    WriteHexString(f, "011c00030000000100010000")

    WriteHexString(f, "0153000300000003")
    offset = nx * ny * 3 + 200
    f.write(struct.pack('>B', ((offset & 0xff000000) // 16777216)))
    f.write(struct.pack('>B', ((offset & 0x00ff0000) // 65536)))
    f.write(struct.pack('>B', ((offset & 0x0000ff00) // 256)))
    f.write(struct.pack('>B', ((offset & 0x000000ff))))

    WriteHexString(f, "00000000")

    WriteHexString(f, "000800080008")

    WriteHexString(f, "000000000000")

    WriteHexString(f, "00ff00ff00ff")

    WriteHexString(f, "000100010001")

    f.close()


#### main body ###
dataFile = open('I-pixel-u.bdf').readlines()
bdfFontData = BdfFont()
bdfFontData.setFontFormatParameters(dataFile)

word = input()
wordArray = bdfFontData.getWordArray(word, dataFile)

writeTIFF(wordArray)

########## Workspace ###########
# word = input()
# for letter in word:
#     bdfFontData.getFontBitmap(dataFile, str(ord(letter)).strip())
#     bdfFontData.printBitmap(" ", "#")
#     bdfFontData.shiftBitmap()
#     bdfFontData.printShiftedBitmap("#", " ")
#     print(bdfFontData.getLetterArray())
