# xenaH5
Python scripts for converting 10x genomics single cell RNAseq data to Xena dense matrix file, particular for handling the large HDF5 Gene-Barcode Matrix Format.

---------

#### What is 10x genomics HDF5 Gene-Barcode Matrix Format

https://support.10xgenomics.com/single-cell/software/pipelines/latest/advanced/h5_matrices


#### xenaH5 Requirement
    python 2

    python modules
        h5py
        numpy
        uuid


#### xenaH5 Usage

    1. Get a basic information about the h5 file, find out group name
    python h5_info.py your_h5file

    2. Slow and simple convertion
    python h5_xena.py Gene-Barcode_Matrix_h5 groupname output_tsv_file

    3. Fast convertion
        3.1 python h5_transpose.py Gene-Barcode_Matrix_h5 groupname output_transposed_h5
        3.2 python h5_xena_fast.py output_transposed_h5 groupname output_tsv_file


#### Load xena dense matrix file (tsv) into your xena hub

[http://xena.ucsc.edu/private-hubs/](http://xena.ucsc.edu/private-hubs/)
