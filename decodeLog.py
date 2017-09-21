#!/usr/bin/env python
# coding: utf-8 -*-

#[[
 # @brief:		解压客户端日志
 # @author:		kun si
 # @email:	  	627795061@qq.com
 # @date:		2017-09-20
#]]

import os
import zlib
import base64
import sys


def decompress(infile, dst):
    infile = open(infile, 'rb')
    dst = open(dst, 'wb')
    decompress = zlib.decompressobj()
    data = infile.read(1024)
    while data:
        dst.write(decompress.decompress(data))
        data = infile.read(1024)
    dst.write(decompress.flush())
    infile.close()
    dst.close()

def unpackLogs(packFileDir, unpackFileDir):   
	for root, dirs, files in os.walk(packFileDir):  
		for fileName in files:
			print("unpack fileName", fileName)
			packFile = packFileDir + fileName
			packFileObject = open(packFile, "r")
			tempFile = packFileDir + "temp.log"
			try:
				decompress(packFile, tempFile)
				tempFileObject = open(tempFile, "r")
				zlibDecodeLog = tempFileObject.read()
				unpackFile = unpackFileDir + fileName
				if os.path.exists(unpackFile):
					os.remove(unpackFile)
				unpackFileObject = open(unpackFile, "w+")
				#print(base64.b64decode(zlibDecodeLog))
				try:
					for line in zlibDecodeLog.split("\n")[:-1]:
						#print(line)
						rawLog = base64.b64decode(line)
						if type(rawLog) != type("a") :
							rawLog = rawLog.decode('utf-8')
						unpackFileObject.write(rawLog+'\n')
				finally:
					tempFileObject.close()
					unpackFileObject.close()
				os.remove(tempFile)
			finally:
				packFileObject.close()
				print("unpackLogs error!")

if __name__ == "__main__":
	packFileDir = "./pack/"
	unpackFileDir = "./unpack/"
	if len(sys.argv) >= 2 :
		if sys.argv[1]!=None:
			packFileDir = sys.argv[1]
		if sys.argv[2]!=None:
			unpackFileDir = sys.argv[2]

	print("sss unpack debugLog file run.")

	unpackLogs(packFileDir, unpackFileDir)

	print("sss unpack debugLog file done!")