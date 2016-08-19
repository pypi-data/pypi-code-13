#!/bin/python
from __future__ import absolute_import
from __future__ import print_function
import argparse
from builtins import bytes
from io import open
import os
import sys
import zlib
from oclminifier.minify import DEFAULT_PREPROCESSOR_COMMAND, _do_minify
from oclminifier.build import try_build


# TODO: Test against all Nvidia and AMD examples.
# TODO: Benchmark compile times to see if this actually helps at all.
# TODO: Conform to PEP8.

# TODO: Fix these issues.
# oclNbodyKernel.cl has weird defines. REAL...?
# oclReduction_kernel.cl another weird defines? T...?
# sweep_kernels.cl parse error

# TODO:
#10. Write readme.rst.
#5. Start adding CmakeLists examples.
# TODO: Rename all of this to oclminify instead of oclminifier.


def main():
	# Compatibility check to make sure an old version of pycparser was not
	# installed by accident. This won't be required once a version of pycparser
	# newer than 2.14 is released.
	from pycparser import c_ast
	if "Pragma" not in dir(c_ast):
		print("Your version of pycparser is too old.\nRun \"pip uninstall pycparser && pip install git+https://github.com/eliben/pycparser.git@ffd8cb7dfc4b80c79a500e27736db8f7bfc1186e#egg=pycparser-2.14\"",file=sys.stderr)
		sys.exit(-1)

	parser = argparse.ArgumentParser(formatter_class=argparse.RawDescriptionHelpFormatter,description="Version 0.6.0\nMinify OpenCL source files.",epilog="OpenCL is a trademark of Apple Inc., used under license by Khronos.\nCopyright (c) 2016 StarByte Software, Inc. All rights reserved.")
	parser.add_argument("--preprocessor-command",type=str,default=DEFAULT_PREPROCESSOR_COMMAND,help="Command to preprocess input source before minification. Defaults to \"%s\"" % DEFAULT_PREPROCESSOR_COMMAND)
	parser.add_argument("--no-preprocess",action="store_true",default=False,help="Skip preprocessing step. Implies --no-minify.")
	parser.add_argument("--no-minify",action="store_true",default=False,help="Skip minification step. Useful when debugging.")
	parser.add_argument("--compress",action="store_true",default=False,help="Compress output using zlib. The two byte header will be stripped.")
	parser.add_argument("--strip-zlib-header",action="store_true",default=False,help="Strips the two byte zlib header from the compressed output when --compress is used.")
	parser.add_argument("--header",action="store_true",default=False,help="Embed output in a C header file.")
	parser.add_argument("--header-function-args",action="store_true",default=False,help="Include function argument mappings in C header file.")
	parser.add_argument("--minify-kernel-names",action="store_true",default=False,help="Replace kernel function names with shorter names.")
	parser.add_argument("--global-postfix",type=str,default="",help="Postfix appended to each symbol name in the global scope. Used for preventing name collisions when minifying multiple source files separately. Implies --minify-kernel-names.")
	parser.add_argument("--try-build",action="store_true",default=True,help="Try to build the input using an OpenCL compiler before minifying. The compiled output is discarded. Requires pyopencl.")
	parser.add_argument("--output-file",type=str,default="",help="File path where output shuld be saved. Omit to write to stdout.")
	parser.add_argument("input",help="File path to OpenCL file that should be minified. A \"-\" indicates that input should be read from stdin.")
	args = parser.parse_args()

	if args.input == "-":
		data = ""
		while True:
			c = sys.stdin.read(1)
			if len(c) == 0:
				break
			data += c
	else:
		# Read entire file into memory.
		fd = open(args.input,"r")
		if not fd:
			print("Could not open input file.",file=sys.stderr)
			sys.exit(-1)
		data = "".join(fd.readlines())
		fd.close()

	if args.try_build:
		if not try_build(data):
			sys.exit(-1)

	original_size = len(data)
	if not args.no_preprocess:
		minifier, data = _do_minify(data,
			preprocessor_command=args.preprocessor_command,
			minify=not args.no_minify,
			minify_kernel_names=args.minify_kernel_names or len(args.global_postfix) > 0,
			global_postfix=args.global_postfix
		)
	compiled_size = len(data)

	if args.compress:
		compressed_data = zlib.compress(data,9)
		if args.strip_zlib_header:
			# Strip header: 0x78 0xDA
			data = compressed_data[2:]
		else:
			data = compressed_data

	compressed_size = len(data)
	print("Original Size: %i, Compiled Size: %i, Compressed Size: %i" % (original_size,compiled_size,compressed_size),file=sys.stderr)

	if args.header:
		# Convert data to a C header file.
		guard_name = os.path.split(args.input)[-1].upper().replace(".","_") + "_DATA_H"
		var_base_name = os.path.split(args.input)[-1].lower()
		var_base_name = var_base_name[:var_base_name.find(".")].capitalize()
		header_text = "#ifndef %s\n#define %s\n\n" % (guard_name,guard_name)
		header_text += "static const size_t %s_SIZE = %i;\n" % (var_base_name.upper(),len(data))
		header_text += "static const unsigned char %s_DATA[] = {" % var_base_name.upper()
		for (i,byte) in enumerate(data):
			header_text += str(hex(ord(byte)))
			if i != (len(data) - 1):
				header_text += ","
		header_text += "};\n\n"
		for (old_name,new_name) in minifier.functions.items():
			if old_name not in minifier.kernel_functions:
				continue # Not a kernel, no need to make available.
			header_text += "#define %s_FUNCTION_%s \"%s\"\n" % (var_base_name.upper(),old_name.upper(),new_name)
			if args.header_function_args:
				for (old_arg,new_arg) in minifier.functions_args[old_name].items():
					header_text += "#define %s_FUNCTION_%s_ARG_%s = \"%s\"\n" % (var_base_name.upper(),old_name.upper(),old_arg.upper(),new_arg)
				header_text += "\n"
		if not args.header_function_args:
			header_text += "\n"
		header_text += "#endif"
		data = header_text

	if args.output_file == "":
		print(data)
	else:
		fd = open(args.output_file,"wb")
		if not fd:
			print("Could not open output file",file=sys.stderr)
			sys.exit(-1)
		fd.write(bytes(data,"utf-8"))
		fd.close()

if __name__ == "__main__":
	main()
