import h5py
import os, sys

if __name__ == "__main__" and len(sys.argv[:])!= 3:
    print "pyton 10x_h5_merge.py inputdir namepatten(e.g filtered_gene_bc_matrices_h5.h5)"
    sys.exit()

h5filedir = sys.argv[1]
namepatten = sys.argv[2]
for root, dirs, files in os.walk(h5filedir):
	for file in files:
		if file == namepatten:
			print file, root