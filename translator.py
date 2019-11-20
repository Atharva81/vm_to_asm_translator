import argparse
import os
import sys
from vals import clean_lines
from vals import valid
from push_pop import process_push_pop
from arithmetic import process_arithmetic
from processes import process_call
from processes import process_file
from processes import process_function
from processes import process_line
from processes import process_return
from processes import translate_vm_to_asm
from processes import initialization
    

parser = argparse.ArgumentParser(description="Enter path of directory or file to translate")
parser.add_argument('filename', action="store")
parser.add_argument('-o', '--outfile' , action="store", default=None, dest='outname')
args = parser.parse_args()
fname = args.filename
outname = args.outname
if not os.path.exists(fname):
    print("Path doesn't exist")
    sys.exit()
translate_vm_to_asm(fname, outname)
print("File has been translated.")
    