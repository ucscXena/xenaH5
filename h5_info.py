import h5py
import sys

def print_attrs(name, obj):
    print (name, len(obj), obj)
    if name[-6:] == "/shape":
        print (name, "shape", obj[0],obj[1])

def example_func(name, obj):
    if isinstance(obj, h5py.Dataset): # obj is a dataset
        print (name, len(obj), obj[:5])

def get_h5_info (h5_file):
    hF = h5py.File(h5_file)
    print ("name:", hF.name)
    print ("keys:", hF.keys())

    print 
    print ("attributes")
    hF.visititems(print_attrs)

    print
    print ("dataset example")
    hF.visititems(example_func)

    '''
    assembly = hF.keys()[0]
    print assembly
    print "data :5", hF[assembly+"/data"][:5]
    print "indices :5", hF[assembly+"/indices"][:5]
    print "indptr :3", hF[assembly+"/indptr"][0:3]
    '''

if __name__ == "__main__" and len(sys.argv[:])!=2:
    print ("python h5_xena_T.py h5file")
    sys.exit()

h5file = sys.argv[1]
get_h5_info (h5file)

