import uuid, sys, os
import h5py

def print_attrs(name, obj):
    print name, len(obj)

def get_h5_info (h5_file):
    hF = h5py.File(h5_file)
    print hF.keys()
    hF.visititems(print_attrs)


if __name__ == "__main__" and len(sys.argv[:]) not in [4, 5]:
    print "pyton 10x_h5_xena_fast.py transposed_h5_input group_name tsv_output barcode_prefix(optional)"
    sys.exit()

matrix_h5 = sys.argv[1]
output = sys.argv[3]
group = sys.argv[2]
get_h5_info (matrix_h5)

hF = h5py.File(matrix_h5)
indptr = hF[group +"/indptr"]
indices = hF[group + "/indices"]
data = hF[group + "/data"]
genes = hF[group + "/genes"]
gene_names = hF[group + "/gene_names"]
barcodes = hF[group + "/barcodes"]
shape = hF[group + "/shape"]
rowN = shape[0]
colN = shape[1]
print "row", rowN
print "col", colN

assert(len(indptr) -1 == colN)

counter_indptr_size = rowN

N = len(indptr) -1 ### total
K = 1000  #one segment
tmpDir = output + '_'+ str(uuid.uuid4())
os.system("mkdir "+ tmpDir)
count =0

hF.close()

if len(sys.argv[:] == 5):
    barcode_prefix = sys.argv[4]
    barcodes = map(lambda x: barcode_prefix + '_' + x, barcodes)

for i in range(0, N, K):
    count = count +1
    start =i
    end = min(i+K,N)
    output = tmpDir +"/" + str(count)
    print start, end
    os.system("python " + os.path.dirname(os.path.realpath(__file__)) + "/10x_h5_xena.py " + matrix_h5 + ' ' + group +' ' + output +' ' +str(start)+' '+str(end) + ' ' + barcode_prefix + ' ' + "&")

print "outputs are being generated in directory", tmpDir, "combine them when all done"
print ""
print " cat $(ls -v dir/*) > tsv_output"
