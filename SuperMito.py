import subprocess as sp
import sys, getopt
import pandas as pd
import numpy as np

def main(argv):
    inputfile = ''
    outputfile = ''
    try:
        opts, args = getopt.getopt(argv,"hi:o:",["ifile=","ofile="])
    except getopt.GetoptError:
        print ('test.py -i <inputfile> -o <outputfile>')
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print ('test.py -i <inputfile> -o <outputfile>')
            sys.exit()
        elif opt in ("-i", "--ifile"):
            inputfile = arg
        elif opt in ("-o", "--ofile"):
            outputfile = arg
    
    return inputfile, outputfile

if __name__ == "__main__":
    country, disease = main(sys.argv[1:])
    print(country)
    print(disease)

    
    # country = "Germany"
    # disease = "Altered brain pH / sCJD patients"


    whole = pd.read_csv('whole_meta.csv', sep=',', index_col=0)
    df = whole[(whole['country'] == country) & (whole['mitopatho_diseases'] == disease)]
    IDs = np.unique(df.index)

    ofile = open("my_fasta.txt", "w")

    for i, ID in enumerate(IDs):
        age = df.loc[ID]['age'][0]
        sex = df.loc[ID]['sex'][0]
        new_ID = ID + '_' + age + '_' + sex
        ofile.write(">" + new_ID + "\n" + df.loc[ID]['TextSeq'][0]  + "\n")

            #do not forget to close it
    ofile.close()

    fn_in = 'my_fasta.txt'
    fn_out = 'my_fasta_aligned.fasta'
    sp.run(f'muscle -in {fn_in} -out {fn_out} -diags', shell=True, check=True)

    aln_in = 'my_fasta_aligned.fasta'
    tree_out = 'tree.nwk'
    sp.run(f'FastTree -nt {aln_in} > {tree_out}', shell=True, check=True)




    
