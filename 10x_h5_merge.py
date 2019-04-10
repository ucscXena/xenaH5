import h5py
import os, sys

if __name__ == "__main__" and len(sys.argv[:])!=2:
    print "pyton 10x_h5_merge.py dir"
    sys.exit()

h5filedir = sys.argv[1]
for root, dirs, files in os.walk(h5filedir):
	for file in files:
		ext =os.path.splitext(file)[1]
		if ext == '.h5':
			print file