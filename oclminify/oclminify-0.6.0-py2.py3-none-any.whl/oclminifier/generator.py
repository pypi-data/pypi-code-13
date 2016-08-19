from __future__ import absolute_import
from pycparser import c_ast
from pycparserext.ext_c_generator import OpenCLCGenerator


class Generator(OpenCLCGenerator):
	def visit(self,n):
		result = super(OpenCLCGenerator,self).visit(n)
		# Find common patterns with extra spacing that can be shortened. This
		# might not work correctly if there is a character array that matches
		# one of these. Fortunately, character arrays are pretty much never
		# used in OpenCL in practice.
		replaces = [
			(", ",","),
			(" = ","="),
			("  "," "),
			(" { ","{"),
			("{ ","{"),
			(" } ","}"),
			("} ","}"),
			("; ",";"),
			(") ",")"),
			("& ","&"),
			("* ","*"),
			(" *","*"),
			("-- ","--"),
			("++ ","++"),
			(" __attribute__(())",""),
			(" \n","\n"),
			("\n ","\n"),
		]
		for replace in replaces:
			result = result.replace(*replace)
		# Simple method to remove extra newlines except where required
		# (#pragma). This has the same consequences as the above method but is
		# much simpler then reimplementing everything.
		lines = result.split("\n")
		result = ""
		for line in lines:
			if "#pragma" in line:
				# Put pragma on its own line.
				if len(result) != 0:
					result += "\n"
				result += line + "\n"
			else:
				result += line
		return result
	def visit_BinaryOp(self,n):
		# Only include brackets when order cannot be implied through through
		# operator priority. Based off of C because I could not find the
		# operator precedence in the specification.
		# http://en.cppreference.com/w/c/language/operator_precedence
		operator_precedence = {
			"*": 3,
			"/": 3,
			"%": 3,
			"+": 4,
			"-": 4,
			"<<": 5,
			">>": 5,
			"<": 6,
			"<=": 6,
			">": 6,
			">=": 6,
			"==": 7,
			"!=": 7,
			"&": 8,
			"^": 9,
			"|": 10,
			"&&": 11,
			"||": 12,
		}
		left = self.visit(n.left)
		right = self.visit(n.right)
		if isinstance(n.left,c_ast.BinaryOp):
			if operator_precedence[n.left.op] > operator_precedence[n.op]:
				left = "(" + left + ")"
		if isinstance(n.right,c_ast.BinaryOp):
			if operator_precedence[n.right.op] > operator_precedence[n.op]:
				right = "(" + right + ")"
		result = "%s%s%s" % (left,n.op,right)
		return result.replace(" ","")
	def visit_Assignment(self,n):
		result = super(OpenCLCGenerator,self).visit_Assignment(n)
		return result.replace(" ","")
	def visit_DeclList(self,n):
		result = super(OpenCLCGenerator,self).visit_DeclList(n)
		return result.replace(", ",",")
	def visit_Cast(self,n):
		# Work around an issue (bug?) in noticed in green's compiler that causes
		# vector literals in double brackets to be treated as a scaler using the
		# last value in the expression list.
		# ushort4 test = (ushort4)((0,1,2,3)); //test = (3,3,3,3)
		# ushort4 test = (ushort4)(0,1,2,3); //test = (0,1,2,3)
		result = "(" + self._generate_type(n.to_type) + ")"
		if self._is_simple_node(n.expr):
			result += " " + self.visit(n.expr)
		else:
			result += "(" + self.visit(n.expr) + ")"
		return result.replace(") ",")")
	def visit_TernaryOp(self,n):
		result = super(OpenCLCGenerator,self).visit_TernaryOp(n)
		return result.replace(" ? ","?").replace(" : ",":")
	def visit_If(self,n):
		result = super(OpenCLCGenerator,self).visit_If(n)
		return result.replace("if (","if(")
	def visit_For(self,n):
		result = super(OpenCLCGenerator,self).visit_For(n)
		return result.replace("for (","for(")
	def visit_While(self,n):
		result = super(OpenCLCGenerator,self).visit_While(n)
		return result.replace("while (","while(")
	def visit_DoWhile(self,n):
		result = super(OpenCLCGenerator,self).visit_DoWhile(n)
		return result.replace("while (","while(")
	def visit_Struct(self,n):
		result = super(OpenCLCGenerator,self).visit_Struct(n)
		return result.replace("struct {","struct{")
	def visit_Switch(self,n):
		result = super(OpenCLCGenerator,self).visit_Switch(n)
		return result.replace("switch (","switch(")
	def visit_FileAST(self,n):
		# Prevent parent implementation from inserting an unnecessary newline
		# for non-function definitions at the top level.
		result = ""
		for ext in n.ext:
			if isinstance(ext,c_ast.FuncDef) or isinstance(ext,c_ast.Pragma):
				result += self.visit(ext)
			else:
				result += self.visit(ext) + ";"
		return result

