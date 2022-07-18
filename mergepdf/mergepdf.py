"""
   
   Merge pdfs into one pdf

   Wrote by Dong Cong 2019.9.17 Montreal,QC

   pip3 install PyPDF2

"""
import os
import sys, getopt
from PyPDF2 import PdfFileMerger

def mergePdf(src_path,save_path):
    target_path = src_path
    pdf_lst = [f for f in os.listdir(target_path) if f.endswith('.pdf')]
    pdf_lst = [os.path.join(target_path, filename) for filename in pdf_lst]

    file_merger = PdfFileMerger()
    for pdf in pdf_lst:
        file_merger.append(pdf)

    file_merger.write(save_path)

def main(argv):
    inputfilepath = ''
    outputfile = ''
    backgroundImage = ''
    start_time = 0
    try:
        opts, args = getopt.getopt(argv,"hi:o:",["ipath=","ofile="])
    except getopt.GetoptError:
        print('mergepdf.py -i <inputpath> -o <outputfile>')
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print('mergepdf.py -i <inputpath> -o <outputfile>')
            sys.exit()
        elif opt in ("-i", "--ipath"):
            inputfilepath = arg
        elif opt in ("-o", "--ofile"):
            outputfile = arg  

    mergePdf(inputfilepath,outputfile)     
    
 
if __name__ == "__main__":
    main(sys.argv[1:])