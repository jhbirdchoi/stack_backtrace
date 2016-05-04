#!/usr/bin/python
# coding=utf-8
# 
# Author: @RandomAtom
# 说明：
#     在嵌入式系统里，尤其是小系统中，死机之后，很多情况下无法定位死机的地址，给调试带来非常多的不便；
# 	  这里利用ARM异常后dump下来的stack数据，和rvds生成的symdefs文件，得到stack的bacetrace数据
# 原理：
#	  1. 在rvds 2.2 下stack的布局：
#      high addr
#        --------------------------
#        frame1
#              <R0, .. R10>  (可选)
#              R14  (返回地址)
#        frame2
#               <R0, .. R10>  (可选)
#              R14   (返回地址)
#            ...............
#        --------------------------
#      low addr
#     2. 由于这样的stack信息不足，无SP信息，这里用近似的做法，dump的数据，数值只要 .text段地址范围内，就认为是返回地址。


import os
import sys
import string


def lower_bound(data, find, lo=0, hi=None):
	hi = hi if hi is not None else len(data)
	if find < data[0] or data[-1] < find:
		return -1
	while lo < hi:
		mid = (lo+hi) / 2
		midval = data[mid]
		if midval < find:
			lo = mid +1
		elif midval > find:
			hi = mid
		else:
			return mid
	return hi - 1


def InitSymbArr(file):	
	fd = open(file, 'r')
	symb_arr = []  # [[name, addr, size]...]
	for line in fd.readlines():
		if not line: continue
		if line.find('ARM Code') != -1:
			parts = line.split()
			if len(parts) == 6:
				name = parts[0]
				addr = parts[1]
				size = parts[4]
				symb_arr.append([name, int(addr, 16), int(size, 16)])
			else:
				continue

	symb_arr.sort(key=lambda x:x[1])
	start = 0
	for e in symb_arr:
		if e[0] == '__main':
			break
		start += 1
	del symb_arr[:start]
	return symb_arr

def InitBacktrace(file):
	fd = open(file, 'r')
	backtrace = []
	for line in fd.readlines():
		line = line.strip()
		if not line: continue
		try:
			backtrace.append(int(line, 16))
		except:
			backtrace.append(line)
			continue
	return backtrace


################### main ###################

if len(sys.argv) != 3:
	print 'backtrace map.txt statck.txt'
	sys.exit(1)

symb_arr = InitSymbArr(sys.argv[1])
backtrace = InitBacktrace(sys.argv[2])
code_start = symb_arr[0][1]
code_end = symb_arr[-1][1]


# print '0x%x, 0x%x' % (code_start, code_end)
symb_arr_addr = [ e[1] for e in symb_arr ]
for frame in backtrace:
	if type(frame) == str:
		print frame
	elif code_start <= frame and frame <= code_end:
		idx = lower_bound(symb_arr_addr, frame)
		if idx != -1 and frame <= symb_arr[idx][1] + symb_arr[idx][2]:
			print '0x%x, [%s, 0x%x, 0x%x]' % (frame, symb_arr[idx][0], symb_arr[idx][1], symb_arr[idx][2])
