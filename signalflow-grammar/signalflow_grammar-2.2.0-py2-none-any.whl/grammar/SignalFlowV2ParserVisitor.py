# Generated from grammar/SignalFlowV2Parser.g4 by ANTLR 4.5.2
from antlr4 import *

# This class defines a complete generic visitor for a parse tree produced by SignalFlowV2Parser.

class SignalFlowV2ParserVisitor(ParseTreeVisitor):

    # Visit a parse tree produced by SignalFlowV2Parser#program.
    def visitProgram(self, ctx):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SignalFlowV2Parser#functionDefinition.
    def visitFunctionDefinition(self, ctx):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SignalFlowV2Parser#parameters.
    def visitParameters(self, ctx):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SignalFlowV2Parser#varArgsList.
    def visitVarArgsList(self, ctx):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SignalFlowV2Parser#varArgsListParamDef.
    def visitVarArgsListParamDef(self, ctx):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SignalFlowV2Parser#varArgsListParamName.
    def visitVarArgsListParamName(self, ctx):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SignalFlowV2Parser#statement.
    def visitStatement(self, ctx):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SignalFlowV2Parser#simpleStatement.
    def visitSimpleStatement(self, ctx):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SignalFlowV2Parser#smallStatement.
    def visitSmallStatement(self, ctx):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SignalFlowV2Parser#exprStatement.
    def visitExprStatement(self, ctx):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SignalFlowV2Parser#returnStatement.
    def visitReturnStatement(self, ctx):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SignalFlowV2Parser#flowStatment.
    def visitFlowStatment(self, ctx):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SignalFlowV2Parser#compoundStatement.
    def visitCompoundStatement(self, ctx):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SignalFlowV2Parser#suite.
    def visitSuite(self, ctx):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SignalFlowV2Parser#test.
    def visitTest(self, ctx):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SignalFlowV2Parser#lambdef.
    def visitLambdef(self, ctx):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SignalFlowV2Parser#or_test.
    def visitOr_test(self, ctx):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SignalFlowV2Parser#and_test.
    def visitAnd_test(self, ctx):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SignalFlowV2Parser#not_test.
    def visitNot_test(self, ctx):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SignalFlowV2Parser#comparison.
    def visitComparison(self, ctx):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SignalFlowV2Parser#expr.
    def visitExpr(self, ctx):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SignalFlowV2Parser#term.
    def visitTerm(self, ctx):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SignalFlowV2Parser#factor.
    def visitFactor(self, ctx):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SignalFlowV2Parser#power.
    def visitPower(self, ctx):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SignalFlowV2Parser#atom_expr.
    def visitAtom_expr(self, ctx):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SignalFlowV2Parser#atom.
    def visitAtom(self, ctx):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SignalFlowV2Parser#list_value.
    def visitList_value(self, ctx):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SignalFlowV2Parser#trailer.
    def visitTrailer(self, ctx):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SignalFlowV2Parser#actual_args.
    def visitActual_args(self, ctx):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SignalFlowV2Parser#argument.
    def visitArgument(self, ctx):
        return self.visitChildren(ctx)


