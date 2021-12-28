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

    def set_encoding_number(self, number):
        intEncodingNumber = 0
        try:
            if number.startswith("0x"):
                intEncodingNumber = int(number, 16)
            else:
                intEncodingNumber = int(number)

        except ValueError:
            print("Invalid input number")
            exit()
        self.strEncodingNumber = \
            self._strEncoding + " " + str(intEncodingNumber)

    def set_font_format_parameters(self, dataFile):
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

    def set_font_farameters(self, bbx):
        self.tempList = bbx.split()
        self.width = int(self.tempList[1])
        self.height = int(self.tempList[2])
        self.xoffset = int(self.tempList[3])
        self.yoffset = int(self.tempList[4])

    def bitmap_array_zero_clear(self):
        self.bitmapArray = []
        for m in range(self.windowHeight):
            self.tempList = []
            for n in range(self.windowWidth):
                self.tempList.append(0)
            self.bitmapArray.append(self.tempList)
        return self.bitmapArray

    def bitmap_list2array(self, bitmapList):
        self.bitmap = []
        for m in range(len(bitmapList)):
            self.bitData = int(bitmapList[m], 16)
            self.temp = self.bitData
            self.tempList = []
            if self.width > 9:
                self.shiftBits = 16 - 1
            else:
                self.shiftBits = 8 - 1

            for n in range(self.width):
                self.bit = (1 << (self.shiftBits)) & self.temp
                self.temp = self.temp << 1
                if self.bit == (1 << (self.shiftBits)):
                    self.tempList.append(1)
                else:
                    self.tempList.append(0)
            self.bitmap.append(self.tempList)

    def print_bitmap(self, charBitOne="*", charBitZero="-"):
        if not self.flagEncodeExist:
            print("No Encode Number")
            return

        for m in range(self.height):
            self.temp = ""
            for n in range(self.width):
                if self.bitmap[m][n] == 1:
                    self.temp = self.temp + charBitOne
                else:
                    self.temp = self.temp + charBitZero
            print(self.temp)

    def print_shifted_bitmap(self, charBitOne="*", charBitZero="-"):
        if not self.flagEncodeExist:
            print("No Encode Number")
            return

        for m in range(self.windowHeight):
            self.temp = ""
            for n in range(self.windowWidth):
                if self.shiftedBitmap[m][n] == 1:
                    self.temp = self.temp + charBitOne
                else:
                    self.temp = self.temp + charBitZero
            print(self.temp)

    def get_font_bitmap(self, dataFile, encoding):
        self.set_encoding_number(encoding)
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
            self.set_font_farameters(self.extractedList[3])
            self.bitmap_list2array(self.extractedList[5:])
            self.flagEncodeExist = True
        else:
            self.bitmap = self.bitmap_array_zero_clear()
            self.flagEncodeExist = False
            # print(self.extractedList)

    def shift_bitmap(self):
        self.shiftedBitmap = self.bitmap_array_zero_clear()
        if not self.flagEncodeExist:
            return

        for m in range(self.windowHeight):
            for n in range(self.windowWidth):
                self.bitmap_x = n - self.xoffset + self.windowXoffset
                self.bitmap_y = \
                    m + self.yoffset \
                    - self.windowYoffset + (self.height - self.windowHeight)
                if self.bitmap_x >= 0 and self.bitmap_x < self.width:
                    if self.bitmap_y >= 0 and self.bitmap_y < self.height:
                        self.shiftedBitmap[m][n] = \
                            self.bitmap[self.bitmap_y][self.bitmap_x]

    def get_letter_array(self, letter, dataFile):
        self.get_font_bitmap(dataFile, str(ord(letter)).strip())
        self.shift_bitmap()

        if not self.flagEncodeExist:
            print("No Encode Number")
            return

        self.tempLetter = []
        for m in range(self.windowHeight):
            self.tempRow = []
            for n in range(self.windowWidth):
                self.tempRow.append(self.shiftedBitmap[m][n])
            self.tempLetter.append(self.tempRow)
        return self.tempLetter

    def get_word_array(self, word, dataFile, height=18):
        tempWord = height * [[]]
        for letter in word:
            letterArray = self.get_letter_array(letter, dataFile)
            for i in range(height):
                tempWord[i] = \
                    tempWord[i] + letterArray[i]
        return tempWord


def write_hex_string(f_param, hex_param):
    while hex_param != '':
        num = int(hex_param[0:2], 16)
        f_param.write(struct.pack('>B', num))
        hex_param = hex_param[2:]


def write_with_offset(f_param, offset_param):
    f_param.write(struct.pack('>B', ((offset_param & 0xff000000) // 16777216)))
    f_param.write(struct.pack('>B', ((offset_param & 0x00ff0000) // 65536)))
    f_param.write(struct.pack('>B', ((offset_param & 0x0000ff00) // 256)))
    f_param.write(struct.pack('>B', ((offset_param & 0x000000ff))))


def write_TIFF(wordArray):
    f = open('temp.tiff', 'wb')

    offset = 0
    nx = len(wordArray[0])
    ny = len(wordArray)
    write_hex_string(f, "4d4d002a")
    offset = nx * ny * 3 + 8
    write_with_offset(f, offset)

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

    write_hex_string(f, "000e")

    write_hex_string(f, "0100000300000001")
    f.write(struct.pack('>B', ((nx & 0xff00) // 256)))
    f.write(struct.pack('>B', ((nx & 0x00ff))))
    write_hex_string(f, "0000")

    write_hex_string(f, "0101000300000001")
    f.write(struct.pack('>B', ((ny & 0xff00) // 256)))
    f.write(struct.pack('>B', ((ny & 0x00ff))))
    write_hex_string(f, "0000")

    write_hex_string(f, "0102000300000003")
    offset = nx * ny * 3 + 182
    write_with_offset(f, offset)

    write_hex_string(f, "010300030000000100010000")

    write_hex_string(f, "010600030000000100020000")

    write_hex_string(f, "011100040000000100000008")

    write_hex_string(f, "011200030000000100010000")

    write_hex_string(f, "011500030000000100030000")

    write_hex_string(f, "0116000300000001")
    f.write(struct.pack('>B', ((ny & 0xff00) // 256)))
    f.write(struct.pack('>B', ((ny & 0x00ff))))
    write_hex_string(f, "0000")

    write_hex_string(f, "0117000400000001")
    offset = nx * ny * 3
    write_with_offset(f, offset)

    write_hex_string(f, "0118000300000003")
    offset = nx * ny * 3 + 188
    write_with_offset(f, offset)

    write_hex_string(f, "0119000300000003")
    offset = nx * ny * 3 + 194
    write_with_offset(f, offset)

    write_hex_string(f, "011c00030000000100010000")

    write_hex_string(f, "0153000300000003")
    offset = nx * ny * 3 + 200
    write_with_offset(f, offset)

    write_hex_string(f, "00000000")

    write_hex_string(f, "000800080008")

    write_hex_string(f, "000000000000")

    write_hex_string(f, "00ff00ff00ff")

    write_hex_string(f, "000100010001")

    f.close()


#### main body ###
dataFile = open('I-pixel-u.bdf').readlines()
bdfFontData = BdfFont()
bdfFontData.set_font_format_parameters(dataFile)

word = input()
wordArray = bdfFontData.get_word_array(word, dataFile)

write_TIFF(wordArray)

########## Workspace ###########
# word = input()
# for letter in word:
#     bdfFontData.get_font_bitmap(dataFile, str(ord(letter)).strip())
#     bdfFontData.print_bitmap(" ", "#")
#     bdfFontData.shift_bitmap()
#     bdfFontData.print_shifted_bitmap("#", " ")
#     print(bdfFontData.get_letter_array())
