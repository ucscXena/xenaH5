import h5py
from array import *
import array
import os, sys

def output_h5 (output, group, data, indices, indptr, shape, genes, gene_names, barcodes):
    f = h5py.File(output,'w')
    g = f.create_group(group)
    g.create_dataset('data', data= data, compression="gzip")
    g.create_dataset('indptr',data= indptr, compression="gzip")
    g.create_dataset('indices',data= indices, compression="gzip")
    g.create_dataset('genes', data = genes, compression="gzip")
    g.create_dataset('gene_names', data = gene_names, compression="gzip")
    g.create_dataset('barcodes', data = barcodes, compression="gzip")
    g.create_dataset('shape', data = shape)
    g.attrs['shape'] = shape
    f.close()

def same(genes, this_genes):
	if len(genes) != len(this_genes):
		return False
	for i in range(0, len(genes)):
		if genes[i] != this_genes[i]:
			return False
	return True

def addH5file(h5file, group, g, counter_data, counter_indptr):
	hF = h5py.File(h5file)

	this_indptr = hF[group +"/indptr"]
	this_indices = hF[group + "/indices"]
	this_data = hF[group + "/data"]
	this_genes = hF[group + "/genes"]
	this_gene_names = hF[group + "/gene_names"]
	this_barcodes = hF[group + "/barcodes"]
	this_shape = hF[group + "/shape"]
	rowN = this_shape[0]
	colN = this_shape[1]

	if len(g['data']) == 0:
		g.create_dataset('genes', data = this_genes, compression="gzip")
		g.create_dataset('gene_names', data = this_gene_names, compression="gzip")
    
	'''
	else:
		# check genes
		if not same(g['genes'], this_genes):
			print h5file, "different genes, skip"
			return
		print "chk"
    '''
	#the standard CSC representation
	#where the row indices for column i are stored in indices[indptr[i]:indptr[i+1]] and
	#their corresponding values are stored in data[indptr[i]:indptr[i+1]].
	#If the shape parameter is not supplied, the matrix dimensions are inferred from the index arrays.

	# indptr
	indptr_offset = g['indptr'][counter_indptr]
	for i in range (0, len(this_indptr)):
		g['indptr'][counter_indptr + i] = this_indptr[i] + indptr_offset
	print "indptr offset", indptr_offset
	counter_indptr = counter_indptr + len(this_indptr) - 1

	for i in range (0, len(this_data)):
		g['data'][counter_data + i ] = this_data[i]
	counter_data = counter_data + len(this_data)
	
	return counter_data,  counter_indptr

def getSizeH5file(h5file, group):
	hF = h5py.File(h5file)
	this_indptr = hF[group +"/indptr"]
	this_data = hF[group + "/data"]
	return len(this_indptr), len(this_data)

if __name__ == "__main__" and len(sys.argv[:])!= 5:
    print "pyton 10x_h5_merge.py inputdir namepatten(e.g filtered_gene_bc_matrices_h5.h5) group_name output_h5"
    sys.exit()

h5filedir = sys.argv[1]
namepatten = sys.argv[2]
group = sys.argv[3]
output = sys.argv[4]

size_indptr = 1
size_data = 0

for root, dirs, files in os.walk(h5filedir):
	for file in files:
		if file == namepatten:
			h5file = root + '/' +  file
			this_size_indptr, this_size_data = getSizeH5file(h5file, group)
			size_data = size_data + this_size_data
			size_indptr = size_indptr + this_size_indptr - 1

print size_indptr, size_data

#output initiation
f = h5py.File(output,'w')
g = f.create_group(group)
g.create_dataset('indptr', (size_indptr,), dtype='i8', compression="gzip")
g.create_dataset('data', (size_data,), dtype='i4', compression="gzip")
g.create_dataset('indices', (size_data,), dtype='i8', compression="gzip")
g.create_dataset('barcodes', (size_indptr-1,),  dtype='S18', compression="gzip")
g['indptr'][0] = 0

count = 0
counter_data = 0
counter_indptr = 0
for root, dirs, files in os.walk(h5filedir):
	for file in files:
		if file == namepatten:
			h5file = root + '/' +  file
			count = count +1
			counter_data,  counter_indptr = addH5file(h5file, group, g, counter_data, counter_indptr)
			if count == 2:
				sys.exit()

#output_h5 (output, group, data, indices, indptr, shape, genes, gene_names, barcodes)