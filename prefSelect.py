#! /usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue May 12 01:18:51 2015
Project	:Python-Project
Version	:0.0.1
@author	:macrobull (http://github.com/macrobull)

"""

#from math import log10
import numpy as np


def binsearch(s, t, ascend = True, idx = None):
	l = 0
	r = len(s) - 1
	while l<r:
		m = (l + r) >> 1
		mid = (s[m] if idx is None else s[m][idx])
		if (mid != t) and ((mid> t) ^ ascend):
			l = m + 1
		else:
			r = m
	return l


############## Test for Fun #####################################
def genESequence(e, acc):
	acc /=2
	r = np.logspace(0, 1, e, endpoint = False)
	for i in range(e):
		dec = 0
		while abs(round(r[i]*2, dec) - r[i]*2) / r[i] > acc*2: # .5 series
			dec +=1
		r[i] = round(r[i]*2, dec)/2
	return r

def testE6Series():
	print(genESequence(6, 0.2))
	print(genESequence(12, 0.1))
	print(genESequence(24, 0.05))
	print(genESequence(48, 0.02))
	print(genESequence(96, 0.01))
	print(genESequence(192, 0.005))

##############################

E24 = [10, 11, 12, 13, 15, 16, 18, 20, 22, 24, 27, 30, 33, 36, 39, 43, 47,
	51, 56, 62, 68, 75, 82, 91]
E24 = np.array(E24)
#E24 = np.array(E24)/10

E192 = [100, 101, 102, 104, 105, 106, 107, 109, 110, 111, 113, 114, 115,
       117, 118, 120, 121, 123, 124, 126, 127, 129, 130, 132, 133, 135,
       137, 138, 140, 142, 143, 145, 147, 149, 150, 152, 154, 156, 158,
       160, 162, 164, 165, 167, 169, 172, 174, 176, 178, 180, 182, 184,
       187, 189, 191, 193, 196, 198, 200, 203, 205, 208, 210, 213, 215,
       218, 221, 223, 226, 229, 232, 234, 237, 240, 243, 246, 249, 252,
       255, 258, 261, 264, 267, 271, 274, 277, 280, 284, 287, 291, 294,
       298, 301, 305, 309, 312, 316, 320, 324, 328, 332, 336, 340, 344,
       348, 352, 357, 361, 365, 370, 374, 379, 383, 388, 392, 397, 402,
       407, 412, 417, 422, 427, 432, 437, 442, 448, 453, 459, 464, 470,
       475, 481, 487, 493, 499, 505, 511, 517, 523, 530, 536, 542, 549,
       556, 562, 569, 576, 583, 590, 597, 604, 612, 619, 626, 634, 642,
       649, 657, 665, 673, 681, 690, 698, 706, 715, 723, 732, 741, 750,
       759, 768, 777, 787, 796, 806, 816, 825, 835, 845, 856, 866, 876,
       887, 898, 909, 920, 931, 942, 953, 965, 976, 988]
E192 = np.array(E192)
#E192 = np.array(E192)/100

E2ACC = [[6, 12, 24, 48, 96, 192], [0.2, 0.1, 0.05, 0.02, 0.01, 0.005]]

def acc2e(acc):
	i = binsearch(E2ACC[1], acc, False)
	return E2ACC[0][i]

def e2acc(e):
	i = binsearch(E2ACC[0], e)
	return E2ACC[1][i]

def getE6Series(e):
	if e>24:
		return E192[::192//e]
	else:
		return E24[::24//e]

def selector(mod, acc):

	target, rev, op = mod

	es = getE6Series(acc2e(acc))
	lut = []
	for i in range(len(es)):
		for j in range(i, len(es)):
			lut.append((op(es[i], es[j]), i, j))

	lut.sort()
	idx = binsearch(lut, target, idx = 0)
	high = low = idx
	while (low>=0) and (lut[low][0]/target>1 - acc): low -=1
	while (high<len(lut)) and (lut[high][0]/target<1 + acc): high +=1
	low +=1
	high -=1

	t0 = [(abs(i[0]-target), i[1], i[2]) for i in lut[low:high+1]]
	t0.sort()

	r = []
	for i in t0:
		if rev:
			r.append((es[i[2]], es[i[1]]))
		else:
			r.append((es[i[1]], es[i[2]]))

	return r

def dividor(target, acc):
	target = target / (1 - target)
	rev = False
	if target>1:
		target = True
		target = target/r
	return selector((target, rev, lambda a,b:a/b), acc)

def parallel(target, acc):
	low = getE6Series(acc2e(acc))[0]/2
	high = getE6Series(acc2e(acc))[0]*5
	while target<low: target *= 10
	while target>=high: target /= 10
	return selector((target, False, lambda a,b:1/(1/a+1/b)), acc)


#print(dividor(0.123, 0.1))
#print(parallel(234, 0.01))

if __name__ =='__main__':
	import sys
	if len(sys.argv) <3:
		print("Usage:")
		print("\tprefSelect div target [acc=0.1]")
		print("\tprefSelect par target [acc=0.1]")
	else:
		cmd = sys.argv[1]
		target = float(sys.argv[2])
		acc = 0.1
		if len(sys.argv)>3:
			acc = float(sys.argv[3])

		if cmd == 'div':
			r = dividor(target, acc)
		elif cmd == 'par':
			r = parallel(target, acc)
		print(r)
