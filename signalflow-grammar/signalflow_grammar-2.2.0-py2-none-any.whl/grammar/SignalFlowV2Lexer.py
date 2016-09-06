# Generated from grammar/SignalFlowV2Lexer.g4 by ANTLR 4.5.2
# encoding: utf-8
from __future__ import print_function
from antlr4 import *
from io import StringIO


import re
from SignalFlowV2Parser import SignalFlowV2Parser
from antlr4.Token import CommonToken


def serializedATN():
    with StringIO() as buf:
        buf.write(u"\3\u0430\ud6d1\u8206\uad2d\u4417\uaef1\u8d80\uaadd\2")
        buf.write(u"*\u0132\b\1\4\2\t\2\4\3\t\3\4\4\t\4\4\5\t\5\4\6\t\6\4")
        buf.write(u"\7\t\7\4\b\t\b\4\t\t\t\4\n\t\n\4\13\t\13\4\f\t\f\4\r")
        buf.write(u"\t\r\4\16\t\16\4\17\t\17\4\20\t\20\4\21\t\21\4\22\t\22")
        buf.write(u"\4\23\t\23\4\24\t\24\4\25\t\25\4\26\t\26\4\27\t\27\4")
        buf.write(u"\30\t\30\4\31\t\31\4\32\t\32\4\33\t\33\4\34\t\34\4\35")
        buf.write(u"\t\35\4\36\t\36\4\37\t\37\4 \t \4!\t!\4\"\t\"\4#\t#\4")
        buf.write(u"$\t$\4%\t%\4&\t&\4\'\t\'\4(\t(\4)\t)\4*\t*\4+\t+\4,\t")
        buf.write(u",\3\2\3\2\3\2\3\2\3\3\3\3\3\3\3\3\3\3\3\3\3\3\3\4\3\4")
        buf.write(u"\3\4\3\4\3\4\3\4\3\4\3\5\3\5\3\5\3\5\3\5\3\6\3\6\3\6")
        buf.write(u"\3\6\3\6\3\7\3\7\3\7\3\7\3\7\3\7\3\b\3\b\3\b\3\t\3\t")
        buf.write(u"\3\t\3\t\3\t\3\n\6\n\u0085\n\n\r\n\16\n\u0086\3\13\7")
        buf.write(u"\13\u008a\n\13\f\13\16\13\u008d\13\13\3\13\5\13\u0090")
        buf.write(u"\n\13\3\13\6\13\u0093\n\13\r\13\16\13\u0094\3\13\3\13")
        buf.write(u"\5\13\u0099\n\13\3\13\6\13\u009c\n\13\r\13\16\13\u009d")
        buf.write(u"\5\13\u00a0\n\13\3\f\3\f\3\f\7\f\u00a5\n\f\f\f\16\f\u00a8")
        buf.write(u"\13\f\3\f\3\f\3\f\3\f\7\f\u00ae\n\f\f\f\16\f\u00b1\13")
        buf.write(u"\f\3\f\5\f\u00b4\n\f\3\r\3\r\3\r\3\r\3\r\3\r\3\r\3\r")
        buf.write(u"\5\r\u00be\n\r\3\16\3\16\3\16\3\17\3\17\3\17\3\20\3\20")
        buf.write(u"\3\20\3\21\3\21\3\21\3\22\3\22\3\23\3\23\3\24\3\24\3")
        buf.write(u"\24\3\25\3\25\3\25\3\25\3\26\3\26\3\26\3\26\3\27\3\27")
        buf.write(u"\7\27\u00dd\n\27\f\27\16\27\u00e0\13\27\3\30\3\30\3\30")
        buf.write(u"\3\31\3\31\3\31\3\32\3\32\3\33\3\33\3\34\3\34\3\35\3")
        buf.write(u"\35\3\36\3\36\3\37\3\37\3 \3 \3!\3!\3\"\3\"\3#\3#\3$")
        buf.write(u"\3$\3%\3%\3%\3&\3&\3\'\3\'\3(\3(\3(\5(\u0108\n(\3(\3")
        buf.write(u"(\5(\u010c\n(\3(\5(\u010f\n(\5(\u0111\n(\3(\3(\3)\6)")
        buf.write(u"\u0116\n)\r)\16)\u0117\3*\3*\3*\5*\u011d\n*\3*\3*\3+")
        buf.write(u"\3+\7+\u0123\n+\f+\16+\u0126\13+\3,\3,\5,\u012a\n,\3")
        buf.write(u",\5,\u012d\n,\3,\3,\5,\u0131\n,\2\2-\3\3\5\4\7\5\t\6")
        buf.write(u"\13\7\r\b\17\t\21\n\23\13\25\f\27\r\31\2\33\16\35\17")
        buf.write(u"\37\20!\21#\22%\23\'\24)\25+\26-\27/\30\61\31\63\32\65")
        buf.write(u"\33\67\349\35;\36=\37? A!C\"E#G$I%K&M\'O(Q\2S)U*W\2\3")
        buf.write(u"\2\16\3\2\62;\4\2GGgg\4\2--//\6\2\f\f\17\17))^^\6\2\f")
        buf.write(u"\f\17\17$$^^\n\2$$))^^ddhhppttvv\3\2\62\65\3\2\629\5")
        buf.write(u"\2C\\aac|\6\2\62;C\\aac|\4\2\13\13\"\"\4\2\f\f\17\17")
        buf.write(u"\u0149\2\3\3\2\2\2\2\5\3\2\2\2\2\7\3\2\2\2\2\t\3\2\2")
        buf.write(u"\2\2\13\3\2\2\2\2\r\3\2\2\2\2\17\3\2\2\2\2\21\3\2\2\2")
        buf.write(u"\2\23\3\2\2\2\2\25\3\2\2\2\2\27\3\2\2\2\2\33\3\2\2\2")
        buf.write(u"\2\35\3\2\2\2\2\37\3\2\2\2\2!\3\2\2\2\2#\3\2\2\2\2%\3")
        buf.write(u"\2\2\2\2\'\3\2\2\2\2)\3\2\2\2\2+\3\2\2\2\2-\3\2\2\2\2")
        buf.write(u"/\3\2\2\2\2\61\3\2\2\2\2\63\3\2\2\2\2\65\3\2\2\2\2\67")
        buf.write(u"\3\2\2\2\29\3\2\2\2\2;\3\2\2\2\2=\3\2\2\2\2?\3\2\2\2")
        buf.write(u"\2A\3\2\2\2\2C\3\2\2\2\2E\3\2\2\2\2G\3\2\2\2\2I\3\2\2")
        buf.write(u"\2\2K\3\2\2\2\2M\3\2\2\2\2O\3\2\2\2\2S\3\2\2\2\2U\3\2")
        buf.write(u"\2\2\3Y\3\2\2\2\5]\3\2\2\2\7d\3\2\2\2\tk\3\2\2\2\13p")
        buf.write(u"\3\2\2\2\ru\3\2\2\2\17{\3\2\2\2\21~\3\2\2\2\23\u0084")
        buf.write(u"\3\2\2\2\25\u008b\3\2\2\2\27\u00b3\3\2\2\2\31\u00b5\3")
        buf.write(u"\2\2\2\33\u00bf\3\2\2\2\35\u00c2\3\2\2\2\37\u00c5\3\2")
        buf.write(u"\2\2!\u00c8\3\2\2\2#\u00cb\3\2\2\2%\u00cd\3\2\2\2\'\u00cf")
        buf.write(u"\3\2\2\2)\u00d2\3\2\2\2+\u00d6\3\2\2\2-\u00da\3\2\2\2")
        buf.write(u"/\u00e1\3\2\2\2\61\u00e4\3\2\2\2\63\u00e7\3\2\2\2\65")
        buf.write(u"\u00e9\3\2\2\2\67\u00eb\3\2\2\29\u00ed\3\2\2\2;\u00ef")
        buf.write(u"\3\2\2\2=\u00f1\3\2\2\2?\u00f3\3\2\2\2A\u00f5\3\2\2\2")
        buf.write(u"C\u00f7\3\2\2\2E\u00f9\3\2\2\2G\u00fb\3\2\2\2I\u00fd")
        buf.write(u"\3\2\2\2K\u0100\3\2\2\2M\u0102\3\2\2\2O\u0110\3\2\2\2")
        buf.write(u"Q\u0115\3\2\2\2S\u011c\3\2\2\2U\u0120\3\2\2\2W\u0127")
        buf.write(u"\3\2\2\2YZ\7f\2\2Z[\7g\2\2[\\\7h\2\2\\\4\3\2\2\2]^\7")
        buf.write(u"t\2\2^_\7g\2\2_`\7v\2\2`a\7w\2\2ab\7t\2\2bc\7p\2\2c\6")
        buf.write(u"\3\2\2\2de\7n\2\2ef\7c\2\2fg\7o\2\2gh\7d\2\2hi\7f\2\2")
        buf.write(u"ij\7c\2\2j\b\3\2\2\2kl\7P\2\2lm\7q\2\2mn\7p\2\2no\7g")
        buf.write(u"\2\2o\n\3\2\2\2pq\7V\2\2qr\7t\2\2rs\7w\2\2st\7g\2\2t")
        buf.write(u"\f\3\2\2\2uv\7H\2\2vw\7c\2\2wx\7n\2\2xy\7u\2\2yz\7g\2")
        buf.write(u"\2z\16\3\2\2\2{|\7k\2\2|}\7h\2\2}\20\3\2\2\2~\177\7g")
        buf.write(u"\2\2\177\u0080\7n\2\2\u0080\u0081\7u\2\2\u0081\u0082")
        buf.write(u"\7g\2\2\u0082\22\3\2\2\2\u0083\u0085\t\2\2\2\u0084\u0083")
        buf.write(u"\3\2\2\2\u0085\u0086\3\2\2\2\u0086\u0084\3\2\2\2\u0086")
        buf.write(u"\u0087\3\2\2\2\u0087\24\3\2\2\2\u0088\u008a\t\2\2\2\u0089")
        buf.write(u"\u0088\3\2\2\2\u008a\u008d\3\2\2\2\u008b\u0089\3\2\2")
        buf.write(u"\2\u008b\u008c\3\2\2\2\u008c\u008f\3\2\2\2\u008d\u008b")
        buf.write(u"\3\2\2\2\u008e\u0090\7\60\2\2\u008f\u008e\3\2\2\2\u008f")
        buf.write(u"\u0090\3\2\2\2\u0090\u0092\3\2\2\2\u0091\u0093\t\2\2")
        buf.write(u"\2\u0092\u0091\3\2\2\2\u0093\u0094\3\2\2\2\u0094\u0092")
        buf.write(u"\3\2\2\2\u0094\u0095\3\2\2\2\u0095\u009f\3\2\2\2\u0096")
        buf.write(u"\u0098\t\3\2\2\u0097\u0099\t\4\2\2\u0098\u0097\3\2\2")
        buf.write(u"\2\u0098\u0099\3\2\2\2\u0099\u009b\3\2\2\2\u009a\u009c")
        buf.write(u"\t\2\2\2\u009b\u009a\3\2\2\2\u009c\u009d\3\2\2\2\u009d")
        buf.write(u"\u009b\3\2\2\2\u009d\u009e\3\2\2\2\u009e\u00a0\3\2\2")
        buf.write(u"\2\u009f\u0096\3\2\2\2\u009f\u00a0\3\2\2\2\u00a0\26\3")
        buf.write(u"\2\2\2\u00a1\u00a6\7)\2\2\u00a2\u00a5\5\31\r\2\u00a3")
        buf.write(u"\u00a5\n\5\2\2\u00a4\u00a2\3\2\2\2\u00a4\u00a3\3\2\2")
        buf.write(u"\2\u00a5\u00a8\3\2\2\2\u00a6\u00a4\3\2\2\2\u00a6\u00a7")
        buf.write(u"\3\2\2\2\u00a7\u00a9\3\2\2\2\u00a8\u00a6\3\2\2\2\u00a9")
        buf.write(u"\u00b4\7)\2\2\u00aa\u00af\7$\2\2\u00ab\u00ae\5\31\r\2")
        buf.write(u"\u00ac\u00ae\n\6\2\2\u00ad\u00ab\3\2\2\2\u00ad\u00ac")
        buf.write(u"\3\2\2\2\u00ae\u00b1\3\2\2\2\u00af\u00ad\3\2\2\2\u00af")
        buf.write(u"\u00b0\3\2\2\2\u00b0\u00b2\3\2\2\2\u00b1\u00af\3\2\2")
        buf.write(u"\2\u00b2\u00b4\7$\2\2\u00b3\u00a1\3\2\2\2\u00b3\u00aa")
        buf.write(u"\3\2\2\2\u00b4\30\3\2\2\2\u00b5\u00bd\7^\2\2\u00b6\u00be")
        buf.write(u"\t\7\2\2\u00b7\u00b8\t\b\2\2\u00b8\u00b9\t\t\2\2\u00b9")
        buf.write(u"\u00be\t\t\2\2\u00ba\u00bb\t\t\2\2\u00bb\u00be\t\t\2")
        buf.write(u"\2\u00bc\u00be\t\t\2\2\u00bd\u00b6\3\2\2\2\u00bd\u00b7")
        buf.write(u"\3\2\2\2\u00bd\u00ba\3\2\2\2\u00bd\u00bc\3\2\2\2\u00be")
        buf.write(u"\32\3\2\2\2\u00bf\u00c0\7>\2\2\u00c0\u00c1\7?\2\2\u00c1")
        buf.write(u"\34\3\2\2\2\u00c2\u00c3\7@\2\2\u00c3\u00c4\7?\2\2\u00c4")
        buf.write(u"\36\3\2\2\2\u00c5\u00c6\7?\2\2\u00c6\u00c7\7?\2\2\u00c7")
        buf.write(u" \3\2\2\2\u00c8\u00c9\7#\2\2\u00c9\u00ca\7?\2\2\u00ca")
        buf.write(u"\"\3\2\2\2\u00cb\u00cc\7>\2\2\u00cc$\3\2\2\2\u00cd\u00ce")
        buf.write(u"\7@\2\2\u00ce&\3\2\2\2\u00cf\u00d0\7q\2\2\u00d0\u00d1")
        buf.write(u"\7t\2\2\u00d1(\3\2\2\2\u00d2\u00d3\7c\2\2\u00d3\u00d4")
        buf.write(u"\7p\2\2\u00d4\u00d5\7f\2\2\u00d5*\3\2\2\2\u00d6\u00d7")
        buf.write(u"\7p\2\2\u00d7\u00d8\7q\2\2\u00d8\u00d9\7v\2\2\u00d9,")
        buf.write(u"\3\2\2\2\u00da\u00de\t\n\2\2\u00db\u00dd\t\13\2\2\u00dc")
        buf.write(u"\u00db\3\2\2\2\u00dd\u00e0\3\2\2\2\u00de\u00dc\3\2\2")
        buf.write(u"\2\u00de\u00df\3\2\2\2\u00df.\3\2\2\2\u00e0\u00de\3\2")
        buf.write(u"\2\2\u00e1\u00e2\7*\2\2\u00e2\u00e3\b\30\2\2\u00e3\60")
        buf.write(u"\3\2\2\2\u00e4\u00e5\7+\2\2\u00e5\u00e6\b\31\3\2\u00e6")
        buf.write(u"\62\3\2\2\2\u00e7\u00e8\7]\2\2\u00e8\64\3\2\2\2\u00e9")
        buf.write(u"\u00ea\7_\2\2\u00ea\66\3\2\2\2\u00eb\u00ec\7}\2\2\u00ec")
        buf.write(u"8\3\2\2\2\u00ed\u00ee\7\177\2\2\u00ee:\3\2\2\2\u00ef")
        buf.write(u"\u00f0\7.\2\2\u00f0<\3\2\2\2\u00f1\u00f2\7=\2\2\u00f2")
        buf.write(u">\3\2\2\2\u00f3\u00f4\7<\2\2\u00f4@\3\2\2\2\u00f5\u00f6")
        buf.write(u"\7-\2\2\u00f6B\3\2\2\2\u00f7\u00f8\7/\2\2\u00f8D\3\2")
        buf.write(u"\2\2\u00f9\u00fa\7,\2\2\u00faF\3\2\2\2\u00fb\u00fc\7")
        buf.write(u"\61\2\2\u00fcH\3\2\2\2\u00fd\u00fe\7,\2\2\u00fe\u00ff")
        buf.write(u"\7,\2\2\u00ffJ\3\2\2\2\u0100\u0101\7?\2\2\u0101L\3\2")
        buf.write(u"\2\2\u0102\u0103\7\60\2\2\u0103N\3\2\2\2\u0104\u0105")
        buf.write(u"\6(\2\2\u0105\u0111\5Q)\2\u0106\u0108\7\17\2\2\u0107")
        buf.write(u"\u0106\3\2\2\2\u0107\u0108\3\2\2\2\u0108\u0109\3\2\2")
        buf.write(u"\2\u0109\u010c\7\f\2\2\u010a\u010c\7\17\2\2\u010b\u0107")
        buf.write(u"\3\2\2\2\u010b\u010a\3\2\2\2\u010c\u010e\3\2\2\2\u010d")
        buf.write(u"\u010f\5Q)\2\u010e\u010d\3\2\2\2\u010e\u010f\3\2\2\2")
        buf.write(u"\u010f\u0111\3\2\2\2\u0110\u0104\3\2\2\2\u0110\u010b")
        buf.write(u"\3\2\2\2\u0111\u0112\3\2\2\2\u0112\u0113\b(\4\2\u0113")
        buf.write(u"P\3\2\2\2\u0114\u0116\t\f\2\2\u0115\u0114\3\2\2\2\u0116")
        buf.write(u"\u0117\3\2\2\2\u0117\u0115\3\2\2\2\u0117\u0118\3\2\2")
        buf.write(u"\2\u0118R\3\2\2\2\u0119\u011d\5Q)\2\u011a\u011d\5U+\2")
        buf.write(u"\u011b\u011d\5W,\2\u011c\u0119\3\2\2\2\u011c\u011a\3")
        buf.write(u"\2\2\2\u011c\u011b\3\2\2\2\u011d\u011e\3\2\2\2\u011e")
        buf.write(u"\u011f\b*\5\2\u011fT\3\2\2\2\u0120\u0124\7%\2\2\u0121")
        buf.write(u"\u0123\n\r\2\2\u0122\u0121\3\2\2\2\u0123\u0126\3\2\2")
        buf.write(u"\2\u0124\u0122\3\2\2\2\u0124\u0125\3\2\2\2\u0125V\3\2")
        buf.write(u"\2\2\u0126\u0124\3\2\2\2\u0127\u0129\7^\2\2\u0128\u012a")
        buf.write(u"\5Q)\2\u0129\u0128\3\2\2\2\u0129\u012a\3\2\2\2\u012a")
        buf.write(u"\u0130\3\2\2\2\u012b\u012d\7\17\2\2\u012c\u012b\3\2\2")
        buf.write(u"\2\u012c\u012d\3\2\2\2\u012d\u012e\3\2\2\2\u012e\u0131")
        buf.write(u"\7\f\2\2\u012f\u0131\7\17\2\2\u0130\u012c\3\2\2\2\u0130")
        buf.write(u"\u012f\3\2\2\2\u0131X\3\2\2\2\33\2\u0086\u008b\u008f")
        buf.write(u"\u0094\u0098\u009d\u009f\u00a4\u00a6\u00ad\u00af\u00b3")
        buf.write(u"\u00bd\u00de\u0107\u010b\u010e\u0110\u0117\u011c\u0124")
        buf.write(u"\u0129\u012c\u0130\6\3\30\2\3\31\3\3(\4\b\2\2")
        return buf.getvalue()


class SignalFlowV2Lexer(Lexer):

    atn = ATNDeserializer().deserialize(serializedATN())

    decisionsToDFA = [ DFA(ds, i) for i, ds in enumerate(atn.decisionToState) ]


    DEF = 1
    RETURN = 2
    LAMBDA = 3
    NONE = 4
    TRUE = 5
    FALSE = 6
    IF = 7
    ELSE = 8
    INT = 9
    FLOAT = 10
    STRING = 11
    LE = 12
    GE = 13
    EQ = 14
    NE = 15
    LT = 16
    GT = 17
    OR = 18
    AND = 19
    NOT = 20
    ID = 21
    OPEN_PAREN = 22
    CLOSE_PAREN = 23
    LSQUARE = 24
    RSQUARE = 25
    LBRACE = 26
    RBRACE = 27
    COMMA = 28
    SEMICOLON = 29
    COLON = 30
    PLUS = 31
    MINUS = 32
    MUL = 33
    DIV = 34
    POW = 35
    BINDING = 36
    DOT = 37
    NEWLINE = 38
    SKIP_ = 39
    COMMENT = 40

    modeNames = [ u"DEFAULT_MODE" ]

    literalNames = [ u"<INVALID>",
            u"'def'", u"'return'", u"'lambda'", u"'None'", u"'True'", u"'False'", 
            u"'if'", u"'else'", u"'<='", u"'>='", u"'=='", u"'!='", u"'<'", 
            u"'>'", u"'or'", u"'and'", u"'not'", u"'('", u"')'", u"'['", 
            u"']'", u"'{'", u"'}'", u"','", u"';'", u"':'", u"'+'", u"'-'", 
            u"'*'", u"'/'", u"'**'", u"'='", u"'.'" ]

    symbolicNames = [ u"<INVALID>",
            u"DEF", u"RETURN", u"LAMBDA", u"NONE", u"TRUE", u"FALSE", u"IF", 
            u"ELSE", u"INT", u"FLOAT", u"STRING", u"LE", u"GE", u"EQ", u"NE", 
            u"LT", u"GT", u"OR", u"AND", u"NOT", u"ID", u"OPEN_PAREN", u"CLOSE_PAREN", 
            u"LSQUARE", u"RSQUARE", u"LBRACE", u"RBRACE", u"COMMA", u"SEMICOLON", 
            u"COLON", u"PLUS", u"MINUS", u"MUL", u"DIV", u"POW", u"BINDING", 
            u"DOT", u"NEWLINE", u"SKIP_", u"COMMENT" ]

    ruleNames = [ u"DEF", u"RETURN", u"LAMBDA", u"NONE", u"TRUE", u"FALSE", 
                  u"IF", u"ELSE", u"INT", u"FLOAT", u"STRING", u"ESCAPE_SEQ", 
                  u"LE", u"GE", u"EQ", u"NE", u"LT", u"GT", u"OR", u"AND", 
                  u"NOT", u"ID", u"OPEN_PAREN", u"CLOSE_PAREN", u"LSQUARE", 
                  u"RSQUARE", u"LBRACE", u"RBRACE", u"COMMA", u"SEMICOLON", 
                  u"COLON", u"PLUS", u"MINUS", u"MUL", u"DIV", u"POW", u"BINDING", 
                  u"DOT", u"NEWLINE", u"SPACES", u"SKIP_", u"COMMENT", u"LINE_JOINING" ]

    grammarFileName = u"SignalFlowV2Lexer.g4"

    def __init__(self, input=None):
        super(SignalFlowV2Lexer, self).__init__(input)
        self.checkVersion("4.5.2")
        self._interp = LexerATNSimulator(self, self.atn, self.decisionsToDFA, PredictionContextCache())
        self._actions = None
        self._predicates = None


        # A queue where extra tokens are pushed on (see the NEWLINE lexer rule).
        self.tokens = []

        # The stack that keeps track of the indentation level.
        self.indents = []

        # The amount of opened braces, brackets and parenthesis.
        self.opened = 0

        # The most recently produced token.
        self.lastToken = None

    def emitToken(self, t):
        self._token = t
        self.tokens.append(t)
           
    def nextToken(self):
        # Check if the end-of-file is ahead and there are still some DEDENTS expected.
        if self._input.LA(1) == SignalFlowV2Parser.EOF and self.indents:

            # Remove any trailing EOF tokens from our buffer.
            for i in range(len(self.tokens) -1, -1, -1):
                if (self.tokens[i].type == SignalFlowV2Parser.EOF):
                    del self.tokens[i]

            # First emit an extra line break that serves as the end of the statement.
            self.emitToken(self.commonToken(SignalFlowV2Parser.NEWLINE, "\n"))

            # Now emit as many DEDENT tokens as needed.
            while self.indents:
                self.emitToken(self.createDedent());
                self.indents.pop()

            # Put the EOF back on the token stream.
            self.emitToken(self.commonToken(SignalFlowV2Parser.EOF, "<EOF>"))

        next = Lexer.nextToken(self)

        if next.channel == Token.DEFAULT_CHANNEL:
            # Keep track of the last token on the default channel.
            self.lastToken = next

        return next if not self.tokens else self.tokens.pop(0)

    def createDedent(self):
        dedent = self.commonToken(SignalFlowV2Parser.DEDENT, "")
        dedent.line = self.lastToken.line
        return dedent
      
    def commonToken(self, type, text):
        stop = self.getCharIndex() - 1
        start = stop if not text else stop - len(text) + 1
        return CommonToken(self._tokenFactorySourcePair, type, self.DEFAULT_TOKEN_CHANNEL, start, stop)

    ## Calculates the indentation of the provided whiteSpace, taking the
    ## following rules into account:
    ##
    ## "Tabs are replaced (from left to right) by one to eight spaces
    ##  such that the total number of characters up to and including
    ##  the replacement is a multiple of eight [...]"
    ##
    ##  -- https://docs.python.org/3.1/reference/lexical_analysis.html#indentation
    @staticmethod
    def getIndentationCount(whiteSpace):
        count = 0;
        for ch in whiteSpace:
            if '\t' == ch:
                count += 8 - (count % 8)
            else:
                count += 1
        return count

    def atStartOfInput(self):
        return self.column == 0 and self.line == 1


    def action(self, localctx, ruleIndex, actionIndex):
    	if self._actions is None:
    		actions = dict()
    		actions[22] = self.OPEN_PAREN_action 
    		actions[23] = self.CLOSE_PAREN_action 
    		actions[38] = self.NEWLINE_action 
    		self._actions = actions
    	action = self._actions.get(ruleIndex, None)
    	if action is not None:
    		action(localctx, actionIndex)
    	else:
    		raise Exception("No registered action for:" + str(ruleIndex))

    def OPEN_PAREN_action(self, localctx , actionIndex):
        if actionIndex == 0:
            self.opened += 1
     

    def CLOSE_PAREN_action(self, localctx , actionIndex):
        if actionIndex == 1:
            self.opened -= 1
     

    def NEWLINE_action(self, localctx , actionIndex):
        if actionIndex == 2:

            newLine = re.sub("[^\r\n]+", "", self.text)
            whiteSpaces = re.sub("[\r\n]+", "", self.text)
            next = self._input.LA(1)
            if self.opened > 0 or next == '\r' or next == '\n' or next == '#':
                # If we are inside a list or on a blank line, ignore all indents,
                # dedents and line breaks.
                self.skip()
            else:
                self.emitToken(self.commonToken(SignalFlowV2Lexer.NEWLINE, newLine));
                indent = SignalFlowV2Lexer.getIndentationCount(whiteSpaces);
                previous = 0 if not self.indents else self.indents[-1]
                if indent == previous:
                    # skip indents of the same size as the present indent-size
                    self.skip()

                elif indent > previous:
                    self.indents.append(indent)
                    self.emitToken(self.commonToken(SignalFlowV2Parser.INDENT, whiteSpaces))
                else:
                    # Possibly emit more than 1 DEDENT token.
                    while self.indents and self.indents[-1] > indent:
                        self.emitToken(self.createDedent())
                        self.indents.pop()
                
     

    def sempred(self, localctx, ruleIndex, predIndex):
        if self._predicates is None:
            preds = dict()
            preds[38] = self.NEWLINE_sempred
            self._predicates = preds
        pred = self._predicates.get(ruleIndex, None)
        if pred is not None:
            return pred(localctx, predIndex)
        else:
            raise Exception("No registered predicate for:" + str(ruleIndex))

    def NEWLINE_sempred(self, localctx, predIndex):
            if predIndex == 0:
                return self.atStartOfInput()
         


