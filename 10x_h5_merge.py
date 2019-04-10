import h5py
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

def addH5file(h5file, data, indices, indptr, genes, gene_names, barcodes):
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

	if len(data) == 0:
		genes = this_genes
		gene_names = this_gene_names
	
	# check genes
	if not same(genes, this_genes):
		print "bad genes"

	# check gene_names
	if not same(gene_names, this_gene_names):
		print "bad gene names"

	


	#data = this_data
	#indptr = this_indptr
	#indices = this_indices
	#indptr = this_indptr
	#shape = this_shape



if __name__ == "__main__" and len(sys.argv[:])!= 5:
    print "pyton 10x_h5_merge.py inputdir namepatten(e.g filtered_gene_bc_matrices_h5.h5) group_name output_h5"
    sys.exit()

h5filedir = sys.argv[1]
namepatten = sys.argv[2]
group = sys.argv[3]
output = sys.argv[4]

#output initiation
indptr = array.array('i')
indices = array.array('i')
data = array.array('f')
genes = [] #string
gene_names = [] #string
barcodes = [] #string
shape = array.array('i') # two integers

for root, dirs, files in os.walk(h5filedir):
	for file in files:
		if file == namepatten:
			h5file = root + '/' +  file
			addH5file(h5file, data, indices, indptr, genes, gene_names, barcodes)
			sys.exit()


output_h5 (output, group, data, indices, indptr, shape, genes, gene_names, barcodes)