#!/usr/bin/env python
# -*- coding: utf-8 -*-

""" CONSTANTS """

sbox = [    0x63, 0x7C, 0x77, 0x7B, 0xF2, 0x6B, 0x6F, 0xC5, 0x30, 0x01, 0x67, 0x2B, 0xFE, 0xD7, 0xAB, 0x76,
			0xCA, 0x82, 0xC9, 0x7D, 0xFA, 0x59, 0x47, 0xF0, 0xAD, 0xD4, 0xA2, 0xAF, 0x9C, 0xA4, 0x72, 0xC0,
			0xB7, 0xFD, 0x93, 0x26, 0x36, 0x3F, 0xF7, 0xCC, 0x34, 0xA5, 0xE5, 0xF1, 0x71, 0xD8, 0x31, 0x15,
			0x04, 0xC7, 0x23, 0xC3, 0x18, 0x96, 0x05, 0x9A, 0x07, 0x12, 0x80, 0xE2, 0xEB, 0x27, 0xB2, 0x75,
			0x09, 0x83, 0x2C, 0x1A, 0x1B, 0x6E, 0x5A, 0xA0, 0x52, 0x3B, 0xD6, 0xB3, 0x29, 0xE3, 0x2F, 0x84,
			0x53, 0xD1, 0x00, 0xED, 0x20, 0xFC, 0xB1, 0x5B, 0x6A, 0xCB, 0xBE, 0x39, 0x4A, 0x4C, 0x58, 0xCF,
			0xD0, 0xEF, 0xAA, 0xFB, 0x43, 0x4D, 0x33, 0x85, 0x45, 0xF9, 0x02, 0x7F, 0x50, 0x3C, 0x9F, 0xA8,
			0x51, 0xA3, 0x40, 0x8F, 0x92, 0x9D, 0x38, 0xF5, 0xBC, 0xB6, 0xDA, 0x21, 0x10, 0xFF, 0xF3, 0xD2,
			0xCD, 0x0C, 0x13, 0xEC, 0x5F, 0x97, 0x44, 0x17, 0xC4, 0xA7, 0x7E, 0x3D, 0x64, 0x5D, 0x19, 0x73,
			0x60, 0x81, 0x4F, 0xDC, 0x22, 0x2A, 0x90, 0x88, 0x46, 0xEE, 0xB8, 0x14, 0xDE, 0x5E, 0x0B, 0xDB,
			0xE0, 0x32, 0x3A, 0x0A, 0x49, 0x06, 0x24, 0x5C, 0xC2, 0xD3, 0xAC, 0x62, 0x91, 0x95, 0xE4, 0x79,
			0xE7, 0xC8, 0x37, 0x6D, 0x8D, 0xD5, 0x4E, 0xA9, 0x6C, 0x56, 0xF4, 0xEA, 0x65, 0x7A, 0xAE, 0x08,
			0xBA, 0x78, 0x25, 0x2E, 0x1C, 0xA6, 0xB4, 0xC6, 0xE8, 0xDD, 0x74, 0x1F, 0x4B, 0xBD, 0x8B, 0x8A,
			0x70, 0x3E, 0xB5, 0x66, 0x48, 0x03, 0xF6, 0x0E, 0x61, 0x35, 0x57, 0xB9, 0x86, 0xC1, 0x1D, 0x9E,
			0xE1, 0xF8, 0x98, 0x11, 0x69, 0xD9, 0x8E, 0x94, 0x9B, 0x1E, 0x87, 0xE9, 0xCE, 0x55, 0x28, 0xDF,
			0x8C, 0xA1, 0x89, 0x0D, 0xBF, 0xE6, 0x42, 0x68, 0x41, 0x99, 0x2D, 0x0F, 0xB0, 0x54, 0xBB, 0x16]
   
rcon = [[0x01,0x02,0x04,0x08,0x10,0x20,0x40,0x80,0x1b,0x36],
		[0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00],
		[0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00],
		[0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00]]
		
rgfield = [[0x02,0x03,0x01,0x01],
		   [0x01,0x02,0x03,0x01],
		   [0x01,0x01,0x02,0x03],
		   [0x03,0x01,0x01,0x02]]
		   
cnst = 0b00011011   # Constant XOR multiplication value 

class libutils:
	
	## Example of use libutils._changecolumn(antKey,[0x09,0xcf,0x4f,0x3c],0) ##
	@staticmethod
	def _changecolumn(block,column,n): 
		for i in xrange(4):
			block[i][n] = column[i]
		return block
		
	## PRECONDITION n<=col(block) ##
	@staticmethod
	def _getcolumn(block,n):
		return [block[i][n] for i in xrange(len(block))]
	
	@staticmethod
	def _getallcolumns(block):
		return [libutils._getcolumn(block,n) for n in xrange(len(block))]
		
	@staticmethod
	## Change first byte at last byte of the column ##
	def _rotword(column):
		tmp = column[0]
		for i in xrange(len(column)-1):
			column[i] = column[i+1]
		column[len(column)-1] = tmp
		return column
	
	@staticmethod
	## Make SubBytes process applied to column ##
	def _subbytes(column):
		return [sbox[i] for i in column]
	
	@staticmethod
	## Make SubBytes process applied to matrix ##
	def _subbytesmatrix(matrix):
		for i in xrange(len(matrix)):
			for j in xrange(len(matrix)):
				matrix[i][j] = sbox[matrix[i][j]]
		return matrix
		
	@staticmethod
	## Xor 3 columns -> key schedule col1 xor col2 xor Rcon[i] ##
	## PRECONDITION len(col1) == len(col2) == len(col3) ##
	def _xor3columns(col1,col2,col3):
		return [col1[i] ^ col2[i] ^ col3[i] for i in xrange(len(col1))]
		
	@staticmethod
	## Xor 2 columns ##
	## PRECONDITION: len(col1) == len(col2) ##
	def _xor2columns(col1,col2):
		return [col1[i] ^ col2[i] for i in xrange(len(col1))]
	
	@staticmethod
	## Build matrix by columns ##
	def _buildmatrixcol(*args):
		matrix = [[0x00]*len(args) for i in xrange(len(args))]
		for i in xrange(len(args)):
			libutils._changecolumn(matrix,args[i],i)
		return matrix
	
	@staticmethod
	## AddRoundKey process ##
	## PRECONDITION: Square matrices (4x4 in this case)
	def _addroundkey(matrix1,matrix2):
		matrix = [[0x00]*4 for i in xrange(len(matrix1))]
		for i in xrange(len(matrix1)):
			matrix = libutils._changecolumn(matrix,libutils._xor2columns(libutils._getcolumn(matrix1,i),libutils._getcolumn(matrix2,i)),i)
		return matrix
	
	@staticmethod
	## Rotate fil n of matrix i times ##
	## Trick: << i -> pos[0] = pos[i], pos[1] = pos[(1+i)%3], pos[2] = pos[(2+i)%3], pos[3] = pos[(3+i)%3]
	def _rotate(fil,n,i):
		auxfil = [p for p in fil]
		for j in xrange(len(fil)):
			fil[j] = 0x00 | auxfil[(j+i)%len(fil)]
		return fil
		
	@staticmethod
	## ShiftRows process   ##
	def _shiftrows(matrix):
		for i in xrange(len(matrix)):
			# Rotate fil i, i times #
			matrix[i] = libutils._rotate(matrix[i],i,i)
		return matrix


	@staticmethod
	## MixColumns process ##
	## PRECONDITION: 8-bits elements in matrix, else it will be truncated at 8-bits or filled with zeros ##
	def _mixcolumns(matrix):
		actCol  = []
		acum    = 0x00
		endCol  = [0x00]*4
		tmp     = 0x00
		for i in xrange(len(matrix)):
			actCol = libutils._getcolumn(matrix,i)
			for j in xrange(len(rgfield)):
				for x in xrange(len(rgfield[j])):
					actCol[x] = actCol[x] & 0x000000FF   # If it has more than 8-bits truncate it
					xored = actCol[x] & 0x00000080
					if rgfield[j][x] == 0x01:
						tmp = actCol[x]					
					elif rgfield[j][x] == 0x02:
						tmp = actCol[x] << 1
						if xored != 0x00000080:
							tmp = tmp ^ cnst											
					else:	
						tmp = actCol[x] << 1
						if xored != 0x00000080:
							tmp = tmp ^ cnst	
						tmp = tmp ^ actCol[x]				
					acum = acum ^ tmp
					acum &= 0x000000FF
					tmp = 0x00
				endCol[j] = acum
				acum 	  = 0x00
			matrix = libutils._changecolumn(matrix,endCol,i)
		return matrix
		
		
	@staticmethod
	## Extract round key n from schedule ##
	## 
	def _extractroundkey(schedule,n):
		roundKey = [[],[],[],[]]
		for i in xrange(len(schedule)):
			for j in range(n*4,(n*4)+4):
				roundKey[i].append(schedule[i][j])
		return roundKey
					
	
class cipheralgorithms:
	
	@staticmethod
	def _aes(*args):
		cipherText = [[0x32,0x88,0x31,0xe0],[0x43,0x5a,0x31,0x37],[0xf6,0x30,0x98,0x07],[0xa8,0x8d,0xa2,0x34]]
		cipherKey  = [[0x2b,0x28,0xab,0x09],[0x7e,0xae,0xf7,0xcf],[0x15,0xd2,0x15,0x4f],[0x16,0xa6,0x88,0x3c]]
		auxBlock   = [[0x00]*4]
		if args != ():
			cipherText = args[0]
			if len(args) == 2:
				cipherKey  = args[1]
		# Set schedule -> we can obtain later all round keys by this matrix #
		schedule  = cipheralgorithms.__keyschedule(cipherKey)
		
		###################### Show ###################### 
		def _showBlock(auxBlock):
			for i in auxBlock:
				for j in i:
					print hex(j)," ",
				print "\n"
		###################### End Show ######################
		 
		# Make init AddRoundKey with cipherKey #
		auxBlock = libutils._addroundkey(cipherText,libutils._extractroundkey(schedule,0))
		print "First AddRoundKey: \n"
		_showBlock(auxBlock)
		# Make 9 main rounds #
		for x in range(1,10):	
			## SubBytes      ##
			auxBlock = libutils._subbytesmatrix(auxBlock)
			print "Round " + str(x) + " SubBytes: \n"
			_showBlock(auxBlock)
			## ShiftRows     ##
			auxBlock = libutils._shiftrows(auxBlock)
			print "Round " + str(x) + " ShiftRows: \n"
			_showBlock(auxBlock)
			## MixColumns    ##
			auxBlock = libutils._mixcolumns(auxBlock)
			print "Round " + str(x) + " MixColumns: \n"
			_showBlock(auxBlock)
			## AddRoundKey   ##
			print "Round " + str(x) + " Key to cipher in this round: \n"
			_showBlock(libutils._extractroundkey(schedule,x))
			print "Round " + str(x) + " Keyed: \n"
			auxBlock = libutils._addroundkey(auxBlock,libutils._extractroundkey(schedule,x))
			_showBlock(auxBlock)
			
		## Make final round  ##	
		## SubBytes      ##
		auxBlock = libutils._subbytesmatrix(auxBlock)
		print "Final subbytes: \n"
		_showBlock(auxBlock)
		## ShiftRows     ##
		auxBlock = libutils._shiftrows(auxBlock)
		print "Final shiftrows: \n"
		_showBlock(auxBlock)
		## AddRoundKey   ##
		auxBlock = libutils._addroundkey(auxBlock,libutils._extractroundkey(schedule,10))
		print "Final keyed: \n"
		_showBlock(auxBlock)
			
	@staticmethod
	def __keyschedule(cipherKey):				
		antKey,schedule,actCol,i,actPos,actPosRcon = cipherKey,[],None,0,0,0
		## Fill schedule 4x40 ##
		schedule = [[0x00]*44 for i in xrange(4)]
		## Set initial status of schedule ##
		for col in libutils._getallcolumns(antKey):
			schedule = libutils._changecolumn(schedule,col,actPos)
			actPos += 1
		for i in xrange(40):
			## Take ant col ##
			actCol = libutils._getcolumn(schedule,actPos-1)
			## If is word in multiple of 4, rotword and subbytes ##
			if(actPos%4==0):
				actCol = libutils._rotword(actCol)
				actCol = libutils._subbytes(actCol)
				actCol = libutils._xor3columns(libutils._getcolumn(schedule,actPos-4),actCol,libutils._getcolumn(rcon,actPosRcon))
				actPosRcon += 1
			else:
				actCol = libutils._xor2columns(libutils._getcolumn(schedule,actPos-4),actCol)
			libutils._changecolumn(schedule,actCol,actPos)
			actPos += 1
		return schedule
		
	
if __name__ == "__main__":
	# If there isn't arguments, values are set by default #
	# 1º -> CipherText (128bits Block)
	# 2º -> CipherKey  (128bits Block)
	cipheralgorithms._aes()
	

