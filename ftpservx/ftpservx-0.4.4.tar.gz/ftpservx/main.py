#!/usr/bin/python
# -*- coding: utf-8 -*-
'''ftpserv - ftp server gui, based on pyftpdlib writed on Python. Licensed by GPL3.'''

import sys
import os
import getpass
import re
import socket
import imp

from multiprocessing import Process

from pyftpdlib.authorizers import DummyAuthorizer
from pyftpdlib.handlers import FTPHandler
from pyftpdlib.servers import FTPServer


try:
#raise ImportError
    imp.find_module('PySide')
    foundPySide = True
except ImportError:
    print (u"""Try to use PyQt4
(license - http://www.riverbankcomputing.co.uk/software/pyqt/license )
instead of PySide
(license - LGPL - http://www.gnu.org/copyleft/lesser.html )""")
    foundPySide = False

if foundPySide:
    from PySide import QtCore
    from PySide.QtGui import QWidget, QVBoxLayout, QHBoxLayout, QPushButton,\
        QLineEdit, QTextBrowser, QFileDialog, QDialog, QLabel, QCheckBox,\
        QPixmap, QIcon, QMainWindow, QApplication, QGroupBox, QDialogButtonBox, QKeySequence
    LIB_USE = "PySide"
else:
    from PyQt4 import QtCore
    from PyQt4.QtGui import QWidget, QVBoxLayout, QHBoxLayout, QPushButton,\
        QLineEdit, QTextBrowser, QFileDialog, QDialog, QLabel, QCheckBox,\
        QPixmap, QIcon, QMainWindow, QApplication, QGroupBox, QDialogButtonBox, QKeySequence
    LIB_USE = "PyQt"


__version__ = '''0.4.4'''


TANGO_ICONS = {
'list-add': """/* XPM */ static char * list_add_xpm[] = { "16 16 19 1","  c None",".  c #3465A4","+   c #B7CEE6","@   c #C0D3E8","#   c #BBD1E7","$   c #BCD1E7","%   c #B6CDE6","&   c #B5CCE6","*   c #B6CCE6","=   c #B4CCE5","-   c #95B7DB",";   c #94B6DB",">   c #92B4DA",",   c #90B3DA","'   c #86ADD9",")   c #83AAD8","!   c #7FA8D7","~   c #7DA6D7","{   c #9FBEE0","                ","                ","      ....      ","      .++.      ","      .++.      ","      .++.      ","  .....++.....  ","  .@#$++++%&*.  ","  .=-;>,')!~{.  ","  .....''.....  ","      .+'.      ","      .+'.      ","      .++.      ","      ....      ","                ","                "};""",
'document-open': """/* XPM */ static char * document_open_xpm[] = { "16 16 137 2","     c None",".  c #565854","+   c #575955","@   c #595B57","#   c #5A5C58","$   c #5F615D","%   c #7A7A7A","&   c #797979","*   c #F7F7F7","=   c #F9F9F9","-   c #FAFAFA",";   c #FBFBFB",">   c #FCFCFC",",   c #A2A3A2","'   c #5B5C58",")   c #787878","!   c #C9C9C9","~   c #C7C7C7","{   c #C4C4C4","]   c #555753","^   c #DADADA","/   c #D3D3D3","(   c #D2D2D2","_   c #CFCFCF",":   c #CDCDCD","<   c #FEFEFE","[   c #939392","}   c #5B5E5A","|   c #737373","1   c #C5C5C5","2   c #B0B0B0","3   c #ACACAC","4   c #DCDCDC","5   c #9C9D9C","6   c #D5D5D4","7   c #FDFDFD","8   c #969796","9   c #5B5D59","0   c #6E6E6E","a   c #C1C1C0","b   c #AAAAAA","c   c #E2E2E2","d   c #DFDFDF","e   c #DEDEDE","f   c #DDDDDD","g   c #E0E0E0","h   c #E9E9E9","i   c #E5E5E5","j   c #D0D0D0","k   c #5D5F5B","l   c #6A6A6A","m   c #BDBDBD","n   c #A9A9A9","o   c #A5A5A5","p   c #E6E6E6","q   c #9FA09E","r   c #9C9D9B","s   c #E3E3E3","t   c #D0D1D0","u   c #656565","v   c #B7B7B7","w   c #A6A6A6","x   c #A1A1A1","y   c #EBEBEB","z   c #EAEAEA","A   c #E8E8E8","B   c #E7E7E7","C   c #D9D9D9","D   c #5B5C59","E   c #5F5F5F","F   c #B3B3B3","G   c #406CA5","H   c #3868A5","I   c #3768A5","J   c #3666A5","K   c #3566A5","L   c #3566A4","M   c #3465A4","N   c #3767A6","O   c #5B5B5B","P   c #AEAEAE","Q   c #C0D5EA","R   c #C1D5EA","S   c #C1D6EA","T   c #BBD2E8","U   c #3465A5","V   c #565656","W   c #C3D6EA","X   c #92B5DB","Y   c #95B8DC","Z   c #B9D0E7","`   c #3466A4"," .  c #515151","..  c #A5A5A4","+.  c #3666A4","@.  c #C5D7EB","#.  c #98B9DD","$.  c #95B7DC","%.  c #B8CEE7","&.  c #4C4C4C","*.  c #3767A5","=.  c #BFD2E9","-.  c #9BBADD",";.  c #9ABADD",">.  c #96B7DC",",.  c #8FB2DA","'.  c #8BB0D8",").  c #B1C9E4","!.  c #484848","~.  c #9B9B9B","{.  c #A5C1E1","].  c #8EB2D9","^.  c #8AAFD8","/.  c #85ACD7","(.  c #83AAD6","_.  c #81A9D5",":.  c #7EA7D4","<.  c #79A3D3","[.  c #77A2D2","}.  c #7BA5D3","|.  c #95B6DB","1.  c #3567A6","2.  c #494949","3.  c #999999","4.  c #3968A5","5.  c #94B5DB","6.  c #82AAD5","7.  c #7DA6D4","8.  c #7FA8D4","9.  c #85ABD5","0.  c #7E8896","a.  c #5588BF","b.  c #5689C0","c.  c #4B7EB7","d.  c #3667A6","e.  c #454A51","f.  c #3565A4","        . + . + + @ # $         ","% & & & . * = - ; ; > , '       ",") ! ~ { ] ^ / / ( _ : < [ }     ","| 1 2 3 ] 4 5 5 5 5 6 < 7 8 9   ","0 a 3 b . c d e e f g h i j k   ","l m n o . p q r r r f s s t 9   ","u v w x + y z z h h A A B C D   ","E F G H H I J J K L L L M M M N ","O P K Q Q Q Q Q Q R S S S S T U ","V n L W X X X X X X X X X Y Z ` "," ...+.@.#.#.#.#.#.#.#.#.#.$.%.K ","&.x *.=.-.;.;.;.;.;.;.>.,.'.).K ","!.~.H {.].^./.(._.:.<.[.[.}.|.1.","2.3.4.5.6.7.7.7.7.7.7.7.7.8.9.J ","!.0.4.a.b.b.b.b.b.b.b.b.b.b.c.d.","e.M M M M M M M M M M M M M f.  "};""",
'folder-remote': """/* XPM */ static char * folder_remote_xpm[] = { "32 32 227 2", "     c None", ".     c #7A7A7A", "+  c #777777", "@  c #787878", "#  c #808080", "$  c #CDCDCD", "%  c #C4C4C4", "&  c #C3C3C3", "*  c #C1C1C1", "=  c #C0C0C0", "-  c #BFBFBF", ";  c #818181", ">  c #B3B3B3", ",  c #9F9F9F", "'  c #9E9E9E", ")  c #9D9D9D", "!  c #9C9C9C", "~  c #9B9B9B", "{  c #9A9A9A", "]  c #999999", "^  c #919191", "/  c #C5C5C4", "(  c #B0B0B0", "_  c #AEAEAE", ":  c #ADADAD", "<  c #ACACAC", "[  c #ABABAB", "}  c #A9A9A9", "|  c #A8A8A8", "1  c #A3A3A3", "2  c #737373", "3  c #6F6F6F", "4  c #6E6E6E", "5  c #6D6D6D", "6  c #B1B1B1", "7  c #979797", "8  c #969696", "9  c #959595", "0  c #949494", "a  c #939393", "b  c #6C6C6C", "c  c #C2C2C1", "d  c #AAAAAA", "e  c #A7A7A7", "f  c #A6A6A6", "g  c #A5A5A5", "h  c #A4A4A4", "i  c #A2A2A2", "j  c #696969", "k  c #B0B0AF", "l  c #989898", "m  c #909090", "n  c #8F8F8F", "o  c #8E8E8E", "p  c #929292", "q  c #8A8A8A", "r  c #666666", "s  c #BDBDBD", "t  c #738AA6", "u  c #3767A5", "v  c #3666A4", "w  c #3565A3", "x  c #3566A5", "y  c #3869A6", "z  c #656565", "A  c #5476A1", "B  c #9AB8D8", "C  c #BED3E9", "D  c #BDD2E9", "E  c #BCD2E9", "F  c #BCD1E8", "G  c #BBD1E8", "H  c #A0BDDC", "I  c #3869A7", "J  c #626262", "K  c #B6B6B5", "L  c #4E75A7", "M  c #A7C1DE", "N  c #9BBDDD", "O  c #8DB3D9", "P  c #8EB3D9", "Q  c #8FB4D9", "R  c #8FB4DA", "S  c #8FB5DA", "T  c #90B5DA", "U  c #9CBDDE", "V  c #96B6D7", "W  c #396AA7", "X  c #5F5F5F", "Y  c #446EA5", "Z  c #B2CAE3", "`  c #99BADD", " . c #8FB3D9", ".. c #93B6DB", "+. c #8EAFD3", "@. c #3969A8", "#. c #5E5E5E", "$. c #ADADAC", "%. c #3D6BA6", "&. c #97B9DD", "*. c #92B5DB", "=. c #86ADD7", "-. c #86A7CF", ";. c #3767A7", ">. c #5A5A5A", ",. c #8E8E8F", "'. c #3868A5", "). c #C5D8EC", "!. c #96B8DC", "~. c #95B7DC", "{. c #95B6DC", "]. c #88AED7", "^. c #81A9D5", "/. c #A0BEDF", "(. c #7C9FCA", "_. c #575757", ":. c #A5A5A4", "<. c #979BA0", "[. c #4672AB", "}. c #C4D8EC", "|. c #98B9DD", "1. c #95B8DC", "2. c #88AFD7", "3. c #84ACD6", "4. c #A7C4E2", "5. c #7196C3", "6. c #555555", "7. c #808892", "8. c #557DB2", "9. c #BFD4EA", "0. c #9BBBDE", "a. c #94B6DC", "b. c #8AAFD9", "c. c #88AED8", "d. c #ADC7E4", "e. c #648BBD", "f. c #525252", "g. c #838F9F", "h. c #6288B8", "i. c #B8CEE8", "j. c #9ABADE", "k. c #96B8DD", "l. c #8FB3DA", "m. c #89AFD8", "n. c #ACC6E4", "o. c #547EB5", "p. c #505050", "q. c #6F7F94", "r. c #6A8FBE", "s. c #AAC5E3", "t. c #93B6DC", "u. c #8AB0D9", "v. c #85ACD7", "w. c #81A9D6", "x. c #80A8D5", "y. c #7FA8D5", "z. c #A3C0E1", "A. c #4572AC", "B. c #4E4E4E", "C. c #7186A0", "D. c #6F94C2", "E. c #9DBCDE", "F. c #7EA7D4", "G. c #78A2D2", "H. c #77A2D2", "I. c #99B9DD", "J. c #3A69A7", "K. c #4B4B4B", "L. c #878786", "M. c #5F7899", "N. c #6790C2", "O. c #6F9DCF", "P. c #709DCF", "Q. c #8AAFD7", "R. c #3466A4", "S. c #494949", "T. c #878787", "U. c #5D7CA3", "V. c #608CC0", "W. c #6998CD", "X. c #6B9ACE", "Y. c #75A0CE", "Z. c #3667A6", "`. c #474747", " + c #7E7E7E", ".+ c #4F73A0", "++ c #6995C7", "@+ c #79A4D2", "#+ c #77A3D1", "$+ c #719CCC", "%+ c #444444", "&+ c #4A73A5", "*+ c #789ECA", "=+ c #84A9D1", "-+ c #83A8D1", ";+ c #6893C3", ">+ c #3967A5", ",+ c #3E3E3E", "'+ c #707478", ")+ c #3A68A4", "!+ c #5B89BB", "~+ c #5D8BBC", "{+ c #4674AD", "]+ c #305E96", "^+ c #3C5679", "/+ c #3465A4", "(+ c #3566A4", "_+ c #33619C", ":+ c #3F4143", "<+ c #575A5C", "[+ c #636466", "}+ c #404143", "|+ c #424242", "1+ c #7C7C7C", "2+ c #797979", "3+ c #515151", "4+ c #454545", "5+ c #414141", "6+ c #DADADA", "7+ c #E2E2E2", "8+ c #E0E0E0", "9+ c #A0A0A0", "0+ c #FCFCFC", "a+ c #DFDFDF", "b+ c #676767", "c+ c #636363", "d+ c #484848", "                                                                ", "    . + + + + + + + + + @                                       ", "    # $ % & & * * = = = - .                                     ", "    ; > , ' ) ! ~ { ] ] { ^                                     ", "    . / ( _ : < [ } } | } 1 2 3 3 4 4 4 4 4 4 5                 ", "    2 6 ! { ] 7 8 8 9 0 0 0 a , < : _ _ ( 6 6 1 b               ", "    3 c < d } e f g h 1 i i i i i i 1 h g f e ] j               ", "    j k l 8 8 0 a ^ m n n o o o o n n m ^ p 0 q r               ", "    r s | t u u u u v v v v v v v v v v u u u v w x x x x y     ", "    z d 9 A B C C C D D E E E E E E E F F F F F G G G G H I     ", "    J K g L M N O O P P P P P Q Q Q Q Q Q R R R S S T U V W     ", "    X g p Y Z `  . . . . . . . . . . . . . . . . . .P ..+.@.    ", "    #.$.i %.F &.*.*.*.*.*.*.*.*.*.*.*.*.*.*.*.*.*.*.=.` -.;.    ", "    >., ,.'.).!.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.{.].^./.(.      ", "    _.:.<.[.}.|.|.|.|.|.|.|.|.|.|.|.|.|.|.|.|.1.2.3.3.4.5.      ", "    6.l 7.8.9.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.a.b.c.c.c.d.e.      ", "    f.! g.h.i.0.0.0.0.0.0.0.0.j.|.k.~.*.l.m.c.c.c.c.c.n.o.      ", "    p.m q.r.s.a.a.t.l.u.v.w.x.y.y.y.y.y.y.y.y.y.y.y.y.z.A.      ", "    B.^ C.D.E.=.F.G.H.H.H.H.H.H.H.H.H.H.H.H.H.H.H.H.H.I.J.      ", "    K.L.M.N.F.O.O.O.O.O.O.O.O.O.O.O.O.O.O.O.O.O.O.O.P.Q.R.      ", "    S.T.U.V.P.W.W.W.W.W.W.W.W.W.W.W.W.W.W.W.W.W.W.W.X.Y.Z.      ", "    `. +.+++@+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+@+$+I       ", "    %+ +&+*+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+-+;+>+      ", "    ,+'+)+!+~+~+~+~+~+~+~+~+~+~+~+~+~+~+~+~+~+~+~+~+~+{+]+      ", "      ^+/+v v v v v v v v v v v v v v v v v v v v (+(+_+        ", "                            :+<+[+}+                            ", "                      |+|+|+S.1+2+3+4+5+                        ", "        `.`.`.`.`.`.4+`.% d 6+7+7+7+8+9+`.`.`.`.`.`.`.`.        ", "        0+0+0+0+0+0+a+`.b+j j j j j j c+K.0+0+0+0+0+0+0+0+      ", "        `.`.`.`.`.`.d+`.4+4+4+4+4+4+4+4+`.`.`.`.`.`.`.`.d+      ", "                                                                ", "                                                                "}; """,
'network-workgroup': """/* XPM */ static char * network_workgroup_xpm[] = { "32 32 106 2", "     c None", ".     c #5E5E5E", "+  c #AAAAA9", "@  c #EDEDED", "#  c #DCDCDC", "$  c #7B7B7B", "%  c #B3B3B3", "&  c #E5E5E5", "*  c #F3F3F3", "=  c #F5F5F6", "-  c #C0C0C5", ";  c #F3F3F4", ">  c #F0F0F0", ",  c #606060", "'  c #B7B4C3", ")  c #B7B5C4", "!  c #F5F5F5", "~  c #748DB1", "{  c #E4E4E4", "]  c #FDFDFD", "^  c #FAFAFA", "/  c #F7F7F7", "(  c #C6C6C6", "_  c #EEEEEE", ":  c #B6B4C3", "<  c #B7B5C3", "[  c #B3B1C1", "}  c #B5B3C1", "|  c #EAEAEB", "1  c #D6DAE1", "2  c #5382B9", "3  c #EFEFEF", "4  c #F9F9F9", "5  c #FCFCFC", "6  c #F6F6F6", "7  c #C4CBD8", "8  c #BDBDBD", "9  c #DADADA", "0  c #D9D9D9", "a  c #D6D6D6", "b  c #D5D5D5", "c  c #D2D2D2", "d  c #F4F4F4", "e  c #D8D8D8", "f  c #757575", "g  c #656565", "h  c #B1B1B1", "i  c #B6B6B6", "j  c #B5B5B5", "k  c #B4B4B4", "l  c #F2F2F2", "m  c #B8B8B8", "n  c #858585", "o  c #F8F8F8", "p  c #666666", "q  c #737372", "r  c #838383", "s  c #F1F1F1", "t  c #E3E3E3", "u  c #DEDEDE", "v  c #DBDBDB", "w  c #E8E8E8", "x  c #E2E2E2", "y  c #DFDFDF", "z  c #5B5B5B", "A  c #FEFEFE", "B  c #A5A5A5", "C  c #8A8A8A", "D  c #ABABAB", "E  c #BABABA", "F  c #B9B9B9", "G  c #7D7D7C", "H  c #B4B4B3", "I  c #6F6F6E", "J  c #888888", "K  c #B2B2B2", "L  c #7E7E7E", "M  c #C3C3C3", "N  c #7F7F7E", "O  c #C8C8C7", "P  c #AAAAAA", "Q  c #7C7C7C", "R  c #BCBCBC", "S  c #C9C9C9", "T  c #D3D3D3", "U  c #D4D4D4", "V  c #CBCBCB", "W  c #818180", "X  c #696968", "Y  c #5D5D5C", "Z  c #D7D7D7", "`  c #A4A4A3", " . c #ECECEC", ".. c #C1C1C1", "+. c #CDCDCC", "@. c #EAEAEA", "#. c #80807F", "$. c #EBEBEB", "%. c #CDCDCD", "&. c #ADADAC", "*. c #9D9D9C", "=. c #636362", "-. c #595959", ";. c #AFAFAF", ">. c #FBFBFB", ",. c #555753", "                                                                ", "                                                                ", "                                                                ", "                              . . . . . . . . . . .             ", "                            . + @ @ @ @ @ @ @ @ @ + .           ", "                            . @ # $ $ $ $ $ $ $ % & .           ", "                            . * $ = - - = - - ; $ > .           ", "      , , , , , , ,         . > $ ' ) ) ) = ! ~ $ > .           ", "    , { ] ] ^ ^ / ( ,       . _ $ : < [ } | 1 2 $ 3 .           ", "  , 4 ] ] 5 ^ ^ / 6 _ ,     . _ $ 2 2 2 2 7 7 2 $ _ .           ", "  , ^ 8 8 8 8 8 8 8 ] ,     . @ $ 2 2 2 2 2 2 2 $ @ .           ", "  , ^ % 9 0 a b c % d ,     . * e $ $ f g . . . . . . . . . .   ", "  , ^ h i i j j k h l ,     . m @ @ @ n + @ @ @ @ @ @ @ @ @ + . ", "  , o 8 8 8 8 8 8 8 d ,     . . p q r . @ # $ $ $ $ $ $ $ % & . ", "  , o % 9 0 a b c % s ,     . * > t @ . * $ = - - = - - ; $ > . ", "  , ^ h i i j j k h * ,     . u 0 0 v . > $ ' ) ) ) = ! ~ $ > . ", "  , ^ w & & x t 0 y * ,     z . . . . . _ $ : < [ } | 1 2 $ 3 . ", "  , A B C D 8 E F m 5 ,     G H I     . _ $ 2 2 2 2 7 7 2 $ _ . ", "  , A J K L M # v j 5 ,     N O N     . @ $ 2 2 2 2 2 2 2 $ @ . ", "  , ] P Q D 8 8 R 8 5 ,     N O N     . * e $ $ $ $ $ $ $ S @ . ", "  , ] T U T U T U T 5 ,     N T N     . m @ @ @ @ @ @ @ @ @ M . ", "  , ] V b V b V b V 5 ,     N W N     . . p q r r r r q X Y . . ", "  , ] M b M b M b M 5 , N N Z b ` N N . * > t @  . .H ..+.# @.. ", "  , ] 8 Z 8 Z 8 Z 8 5 , % #.b $.i W % . u 0 0 v y y v 0 t t %.. ", "  , ] i e i e i e i 5 , N N &.i *.N N =.. . . . . . . . . . . -.", "  , ] ;.0 ;.0 ;.0 ;.5 ,     N N N                               ", "  , A 5 >.5 >.5 >.5 A ,                                         ", "  ,., , , , , , , , , ,.                                        ", "                                                                ", "                                                                ", "                                                                ", "                                                                "}; """,
'system-log-out': """/* XPM */ static char * system_log_out_xpm[] = { "32 32 333 2", "      c None", ".     c #5A5C58", "+  c #555753", "@  c #565854", "#  c #585A56", "$  c #5F615D", "%  c #686A67", "&  c #70726F", "*  c #767774", "=  c #787976", "-  c #777975", ";  c #747673", ">  c #6E706D", ",  c #757774", "'  c #B4B4B4", ")  c #8D8D8D", "!  c #848484", "~  c #7F7F7F", "{  c #787878", "]  c #727272", "^  c #6D6D6D", "/  c #686868", "(  c #636363", "_  c #5F5F5F", ":  c #5C5C5C", "<  c #606060", "[  c #6B6B6A", "}  c #DADAD9", "|  c #F4F4F2", "1  c #F5F5F3", "2  c #F5F5F4", "3  c #F4F4F3", "4  c #EAEAE9", "5  c #757773", "6  c #B8B8B8", "7  c #909090", "8  c #888888", "9  c #818181", "0  c #7B7B7B", "a  c #767676", "b  c #707070", "c  c #6B6B6B", "d  c #676767", "e  c #616161", "f  c #E3E3E1", "g  c #F7F7F6", "h  c #F8F8F7", "i  c #F9F9F8", "j  c #F6F6F5", "k  c #868885", "l  c #BEBEBE", "m  c #949494", "n  c #858585", "o  c #808080", "p  c #7A7A7A", "q  c #757575", "r  c #6F6F6F", "s  c #666666", "t  c #838383", "u  c #E7E7E6", "v  c #FBFBFA", "w  c #FBFBFB", "x  c #FAFAF9", "y  c #929491", "z  c #C5C5C5", "A  c #9A9A9A", "B  c #919191", "C  c #8A8A8A", "D  c #7E7E7E", "E  c #797979", "F  c #747474", "G  c #6C6C6C", "H  c #898989", "I  c #E9E9E8", "J  c #FCFCFB", "K  c #FCFCFC", "L  c #F8F8F8", "M  c #989996", "N  c #CBCBCB", "O  c #A0A0A0", "P  c #979797", "Q  c #717171", "R  c #777777", "S  c #8E8E8E", "T  c #EBEBEA", "U  c #FDFDFC", "V  c #989A97", "W  c #CCCCCC", "X  c #A3A3A3", "Y  c #9D9D9D", "Z  c #8F8F8F", "`  c #ECECEB", " . c #999A98", ".. c #CDCDCD", "+. c #A4A4A4", "@. c #9F9F9F", "#. c #969696", "$. c #EDEDED", "%. c #9A9B98", "&. c #A70101", "*. c #A50000", "=. c #CECECE", "-. c #A6A6A6", ";. c #9B9B9B", ">. c #929292", ",. c #7D7D7D", "'. c #EEEEED", "). c #A70303", "!. c #CB5555", "~. c #AE1919", "{. c #CFCFCF", "]. c #A7A7A7", "^. c #A1A1A1", "/. c #989898", "(. c #868686", "_. c #999999", ":. c #FAFAFA", "<. c #9B918E", "[. c #A90A0A", "}. c #CD5858", "|. c #EEB2B2", "1. c #AE1A1A", "2. c #A8A8A8", "3. c #A2A2A2", "4. c #9E9E9E", "5. c #959595", "6. c #8C8C8C", "7. c #AAAAAA", "8. c #F3E7E6", "9. c #A41818", "0. c #CE5757", "a. c #EB9D9D", "b. c #ECA5A5", "c. c #AE1818", "d. c #A60000", "e. c #A9A9A9", "f. c #8B8B8B", "g. c #AFAFAF", "h. c #B2B2B2", "i. c #EEEEEE", "j. c #F4E7E7", "k. c #B22424", "l. c #CD5555", "m. c #E89090", "n. c #E16565", "o. c #EB9898", "p. c #EBA1A1", "q. c #EBA3A3", "r. c #EBA2A2", "s. c #EA9D9D", "t. c #A5A5A5", "u. c #9C9C9C", "v. c #939393", "w. c #BBBBBB", "x. c #B9B9B9", "y. c #F5E7E6", "z. c #B12222", "A. c #CD5151", "B. c #E68181", "C. c #DE5656", "D. c #DD5353", "E. c #DD5858", "F. c #DE5B5B", "G. c #DD5959", "H. c #DD5555", "I. c #EA9898", "J. c #ABABAB", "K. c #C3C3C3", "L. c #F4E4E3", "M. c #B12020", "N. c #CC4949", "O. c #E27272", "P. c #DA4747", "Q. c #DA4444", "R. c #DA4848", "S. c #DB4B4B", "T. c #DB4D4D", "U. c #E88E8E", "V. c #EFEFEE", "W. c #F4E5E5", "X. c #B01D1D", "Y. c #CB4040", "Z. c #DF6161", "`. c #D73737", " + c #D73535", ".+ c #D83A3A", "++ c #D83D3D", "@+ c #D94040", "#+ c #D83B3B", "$+ c #D73939", "%+ c #E68484", "&+ c #EBCDCD", "*+ c #AA0B0B", "=+ c #D23C3C", "-+ c #D22020", ";+ c #D32424", ">+ c #D21D1D", ",+ c #D01313", "'+ c #CD0707", ")+ c #CC0000", "!+ c #CD0404", "~+ c #CF0E0E", "{+ c #E16969", "]+ c #BABABA", "^+ c #BFBFBF", "/+ c #E1ADAC", "(+ c #AB0C0C", "_+ c #CF2E2E", ":+ c #D52D2D", "<+ c #CC0202", "[+ c #828282", "}+ c #DCACAC", "|+ c #A90B0B", "1+ c #CD2828", "2+ c #D52F2F", "3+ c #CD0303", "4+ c #DC5050", "5+ c #F0F0EF", "6+ c #EBEBEB", "7+ c #D0A2A2", "8+ c #A80909", "9+ c #CB2121", "0+ c #D63030", "a+ c #CD0505", "b+ c #D94242", "c+ c #DA4646", "d+ c #A40000", "e+ c #F7F8F7", "f+ c #F0F0F0", "g+ c #DCDDDC", "h+ c #C49A99", "i+ c #A40606", "j+ c #C81B1B", "k+ c #D53737", "l+ c #A70606", "m+ c #E5E5E5", "n+ c #F7F7F7", "o+ c #F1F1F0", "p+ c #E7E7E7", "q+ c #DDDDDC", "r+ c #D1D1D0", "s+ c #875F5E", "t+ c #A50202", "u+ c #C71616", "v+ c #D33535", "w+ c #A50505", "x+ c #BBBCBB", "y+ c #D8D8D7", "z+ c #F3F3F2", "A+ c #EBECEB", "B+ c #E2E2E1", "C+ c #D7D7D7", "D+ c #80827F", "E+ c #A40101", "F+ c #C11111", "G+ c #A50404", "H+ c #A8A8A7", "I+ c #C6C6C5", "J+ c #E4E4E3", "K+ c #F2F2F1", "L+ c #F2F3F2", "M+ c #DFE0DF", "N+ c #838582", "O+ c #959594", "P+ c #939593", "Q+ c #B3B4B3", "R+ c #D3D4D2", "S+ c #E5E6E4", "T+ c #ECEDEB", "U+ c #EEEFED", "V+ c #E8E9E7", "W+ c #858683", "X+ c #999A99", "Y+ c #91918F", "Z+ c #B1B1AF", "`+ c #CFCFCD", " @ c #DCDDDA", ".@ c #E6E6E4", "+@ c #E7E8E5", "@@ c #E7E8E6", "#@ c #E2E2E0", "$@ c #7D7F7B", "%@ c #CFCFCE", "&@ c #ADADAD", "*@ c #A4A4A3", "=@ c #91928F", "-@ c #B1B2AE", ";@ c #CBCDC8", ">@ c #D5D7D2", ",@ c #DADCD8", "'@ c #DDDFDB", ")@ c #DEDFDC", "!@ c #DFE0DC", "~@ c #AEAEAE", "{@ c #BDBDBD", "]@ c #B1B1B0", "^@ c #989997", "/@ c #B3B5AF", "(@ c #C6C8C2", "_@ c #CECFCA", ":@ c #D2D4CF", "<@ c #D4D5D1", "[@ c #D5D7D3", "}@ c #D6D7D3", "|@ c #D6D8D3", "1@ c #D5D6D2", "2@ c #6C6D6A", "3@ c #BFBFBE", "4@ c #A6A8A4", "5@ c #B3B5B0", "6@ c #BFC1BC", "7@ c #C5C8C2", "8@ c #C8CBC6", "9@ c #CACCC7", "0@ c #CACDC8", "a@ c #CBCEC9", "b@ c #CCCEC9", "c@ c #C9CBC6", "d@ c #636561", "e@ c #B9BAB7", "f@ c #B7B9B3", "g@ c #BABCB6", "h@ c #BEC0BA", "i@ c #C0C2BC", "j@ c #C1C3BD", "k@ c #C2C4BE", "l@ c #C3C5BF", "m@ c #C2C4BF", "n@ c #C0C2BD", "o@ c #5C5E5A", "p@ c #575955", "q@ c #595B57", "r@ c #5B5D59", "                                                                ", "  . + + + + + + + + + + @ # $ % & * = - ; > ,                   ", "  + ' ) ! ~ { ] ^ / ( _ : < [ } | 1 2 2 3 4 5                   ", "  + 6 7 8 9 0 a b c d ( e d { f g h i i h j k                   ", "  + l m ) n o p q r c d s ^ t u i v w w x h y                   ", "  + z A B C n D E F b G c ] H I x J K K w L M                   ", "  + N O P 7 C ! ~ E a Q b R S T x J U K w i V                   ", "  + W X Y P Z H ! o p a F 0 B ` x K U K w i  .                  ", "  + ..+.@.A #.7 C n ~ 0 E ~ m $.x K U K w i %.    &.*.          ", "  + =.-.O ;.P >.S H ! ~ ,.t P '.x K U K w i %.  ).!.~.          ", "  + {.].^.Y /.m Z C (.9 o n _.'.:.K U K w i <.[.}.|.1.          ", "  + {.2.3.4._.5.7 6.) 7.@.S A '.:.K U K w 8.9.0.a.b.c.d.d.d.d.d.", "  + {.e.+.@.;.#.B ) f.g.' h.-.i.:.K U U j.k.l.m.n.o.p.q.r.p.s.*.", "  + {.7.t.O u.P v.S C a ! w.x.i.:.K U y.z.A.B.C.D.E.F.F.G.H.I.*.", "  + {.J.-.3.Y /.m Z f.(.A K.+.i.:.K L.M.N.O.P.Q.R.S.T.T.S.R.U.*.", "  + {.J.].X 4.A 5.B 6.m N e.v.V.:.W.X.Y.Z.`. +.+++@+#+$+@+++%+*.", "  + {.J.e.+.@.;.#.>.B K.6 ~ A V.:.&+*+=+++-+;+>+,+'+)+)+!+~+{+*.", "  + {.J.7.t.^.u./.v.]+^+D n ^.V.:.K /+(+_+:+<+)+)+)+)+)+)+)+H.*.", "  + {.J.7.-.3.Y _.@.w.f.[+) X V.v K J }+|+1+2+3+)+<+<+<+<+<+4+*.", "  + {.J.7.2.X @.A 5.B C f.B t.5+v K 3 6+7+8+9+0+a+.+@+b+Q.c+R.d+", "  + {.J.7.e.+.O ;.P >.S 6.>.-.I e+L f+u g+h+i+j+0+k+l+d+d+d+d+d+", "  + {.J.7.7.-.^.u./.v.7 Z #.e.z m+n+o+p+q+r+s+t+u+v+w+          ", "  + {.J.7.7.].3.4._.#.m m u.].x+y+z+2 A+B+C+D+  E+F+G+          ", "  + {.J.7.7.2.+.O u.;.;.A #.H+I+J+K+3 L+6+M+N+    *.*.          ", "  + {.J.7.7.e.-.X +.t.O+P+Q+R+S+T+U+U+U+T+V+W+                  ", "  + {.J.7.J.J.J.g.X+Y+Z+`+ @f .@+@+@@@+@S+#@$@                  ", "  + %@J.J.&@]+*@=@-@;@>@,@'@)@!@!@!@!@!@'@,@;                   ", "  + =.~@{@]@^@/@(@_@:@<@>@[@}@}@|@}@}@}@1@:@2@                  ", "  + =.3@4@5@6@7@8@9@0@;@a@a@b@b@b@a@a@a@;@c@d@                  ", "  + e@f@g@h@i@j@k@k@l@l@l@l@l@l@l@l@l@l@m@n@o@                  ", "  . + @ p@# q@. . r@r@r@r@r@r@r@o@r@r@r@r@. $                   ", "                                                                "}; """,
'system-lock-screen': """/* XPM */ static char * system_lock_screen_xpm[] = { "32 32 502 2", "      c None", ".     c #949594", "+  c #909090", "@  c #8F8F8F", "#  c #8D8D8D", "$  c #8B8B8B", "%  c #898989", "&  c #878787", "*  c #868686", "=  c #848484", "-  c #828282", ";  c #808080", ">  c #7E7E7E", ",  c #7D7D7D", "'  c #7B7B7B", ")  c #797979", "!  c #777777", "~  c #7C7C7C", "{  c #959595", "]  c #F1F2EF", "^  c #F5F6F3", "/  c #F4F5F3", "(  c #F4F5F2", "_  c #F4F4F2", ":  c #F3F4F2", "<  c #F3F4F1", "[  c #F2F4F1", "}  c #F2F3F1", "|  c #EDEEEB", "1  c #A2A2A2", "2  c #F2F3F0", "3  c #B9BBC8", "4  c #3E3F8E", "5  c #545592", "6  c #535491", "7  c #525290", "8  c #515190", "9  c #52528F", "0  c #51518F", "a  c #50508F", "b  c #51518E", "c  c #53548D", "d  c #52538D", "e  c #52528B", "f  c #51518B", "g  c #53538D", "h  c #55568E", "i  c #54548E", "j  c #55558E", "k  c #54548D", "l  c #535494", "m  c #D4D7D0", "n  c #EEF0ED", "o  c #858685", "p  c #AAAAA9", "q  c #F0F2EE", "r  c #A7AAC0", "s  c #6A6A91", "t  c #7E7E96", "u  c #7D7D95", "v  c #7C7C94", "w  c #7A7A93", "x  c #797992", "y  c #777790", "z  c #888897", "A  c #999B9E", "B  c #9D9FA2", "C  c #919396", "D  c #7F8187", "E  c #717188", "F  c #6F6F8A", "G  c #6D6D88", "H  c #6B6B86", "I  c #6A6A85", "J  c #696985", "K  c #494A8B", "L  c #ADAFAC", "M  c #C2C3C2", "N  c #8D8E8D", "O  c #AFB0AF", "P  c #EFF0ED", "Q  c #9697B8", "R  c #67678C", "S  c #767690", "T  c #75758F", "U  c #74748D", "V  c #73738D", "W  c #72728C", "X  c #A7A9AC", "Y  c #D3D5D2", "Z  c #D0D3CE", "`  c #B9BBB7", " . c #BBBEBA", ".. c #DBDDD9", "+. c #A7A9A8", "@. c #757683", "#. c #666683", "$. c #656582", "%. c #646482", "&. c #636380", "*. c #626280", "=. c #454688", "-. c #D3D6CF", ";. c #EAECE8", ">. c #959695", ",. c #B8B8B7", "'. c #EEEFEB", "). c #8284AD", "!. c #646488", "~. c #6E6E89", "{. c #878794", "]. c #E6E7E5", "^. c #B0B1B1", "/. c #7A7B87", "(. c #68687E", "_. c #69697D", ":. c #7B7B82", "<. c #BDC1BB", "[. c #8B8E8C", "}. c #62627E", "|. c #61617F", "1. c #5F5F7F", "2. c #5F5F7E", "3. c #535375", "4. c #3F4084", "5. c #B2B4B0", "6. c #B7B8B7", "7. c #9B9C9B", "8. c #BFBFBE", "9. c #ECEDE9", "0. c #7173A4", "a. c #646486", "b. c #696986", "c. c #676785", "d. c #676784", "e. c #666684", "f. c #989A9F", "g. c #F0F2EF", "h. c #808186", "i. c #626281", "j. c #616181", "k. c #606080", "l. c #60607F", "m. c #848684", "n. c #A0A49E", "o. c #606179", "p. c #49496E", "q. c #36365F", "r. c #292954", "s. c #242450", "t. c #373880", "u. c #D2D5CE", "v. c #E5E7E3", "w. c #A4A5A3", "x. c #C5C5C3", "y. c #EAECE7", "z. c #61639D", "A. c #646483", "B. c #919296", "C. c #ECEDEA", "D. c #75767F", "E. c #5D5D7F", "F. c #5C5C7E", "G. c #5B5B7D", "H. c #858787", "I. c #AFB3AC", "J. c #3F3F5D", "K. c #272754", "L. c #282855", "M. c #34357E", "N. c #B8BBB6", "O. c #ACADAB", "P. c #CACBC9", "Q. c #E8EAE5", "R. c #575998", "S. c #606081", "T. c #5F5F80", "U. c #5E5E80", "V. c #736A61", "W. c #B99916", "X. c #BE9702", "Y. c #B99300", "Z. c #B38E00", "`. c #AD8900", " + c #A68400", ".+ c #A07F00", "++ c #9A7B00", "@+ c #947701", "#+ c #89700B", "$+ c #413B44", "%+ c #2B2B5A", "&+ c #2C2C5A", "*+ c #2C2C5B", "=+ c #30317C", "-+ c #D0D4CD", ";+ c #E0E2DD", ">+ c #B0B1AF", ",+ c #8C8C8C", "'+ c #CFD0CD", ")+ c #E7E9E4", "!+ c #535595", "~+ c #5C5C7F", "{+ c #5B5B7F", "]+ c #59597E", "^+ c #B89513", "/+ c #F2E494", "(+ c #FFF8BB", "_+ c #FFF6A9", ":+ c #FCF39E", "<+ c #FAEF90", "[+ c #F7EC82", "}+ c #F4E773", "|+ c #F0E364", "1+ c #ECDD52", "2+ c #CBB620", "3+ c #7E6709", "4+ c #2F2F5F", "5+ c #30305F", "6+ c #303060", "7+ c #2D2D7B", "8+ c #BFC1BC", "9+ c #A4A4A3", "0+ c #B6B7B5", "a+ c #5D5D5D", "b+ c #8E8E8E", "c+ c #E5E7E2", "d+ c #525393", "e+ c #58587F", "f+ c #58587E", "g+ c #57577D", "h+ c #56567D", "i+ c #BE9700", "j+ c #FDF8CB", "k+ c #FFF27D", "l+ c #FEEB3E", "m+ c #F9E635", "n+ c #F5E12B", "o+ c #F0DD22", "p+ c #ECD818", "q+ c #E8D30E", "r+ c #E5D115", "s+ c #DFCF41", "t+ c #7F6500", "u+ c #333364", "v+ c #343465", "w+ c #2E2E7A", "x+ c #C5C9C7", "y+ c #DBDDD8", "z+ c #BBBCB9", "A+ c #5E5E5E", "B+ c #8E8E8D", "C+ c #D8D8D6", "D+ c #E3E6E0", "E+ c #505192", "F+ c #54547D", "G+ c #54547C", "H+ c #52527B", "I+ c #FDF8CC", "J+ c #FFF279", "K+ c #E4D012", "L+ c #DFCF42", "M+ c #7C6300", "N+ c #383869", "O+ c #38386A", "P+ c #303078", "Q+ c #B8BCC3", "R+ c #D8DBD5", "S+ c #C0C1BE", "T+ c #606060", "U+ c #DCDDDA", "V+ c #E1E4DE", "W+ c #4C4D90", "X+ c #51517C", "Y+ c #50507C", "Z+ c #50507B", "`+ c #4E4E7B", " @ c #BB9400", ".@ c #FDF7CC", "+@ c #FFF179", "@@ c #DECF42", "#@ c #3C3C6F", "$@ c #3C3C70", "%@ c #313179", "&@ c #ADB0BD", "*@ c #D5D9D3", "=@ c #C4C6C2", "-@ c #8A8A89", ";@ c #DFE0DE", ">@ c #DFE1DC", ",@ c #48498E", "'@ c #4B4B7A", ")@ c #444474", "!@ c #B69100", "~@ c #FDF7C9", "{@ c #FFF27A", "]@ c #E5D114", "^@ c #DECF41", "/@ c #404074", "(@ c #404075", "_@ c #323277", ":@ c #A0A3B9", "<@ c #D4D6D0", "[@ c #C8CAC7", "}@ c #5E5E5C", "|@ c #E3E3E1", "1@ c #DCE0D9", "2@ c #41418B", "3@ c #404072", "4@ c #3D3D71", "5@ c #3E3E72", "6@ c #AB8C13", "7@ c #EEE193", "8@ c #FFF7B4", "9@ c #FEF498", "0@ c #FCF18B", "a@ c #F9EC7C", "b@ c #F5E86D", "c@ c #F2E35C", "d@ c #EFE055", "e@ c #EBDC4C", "f@ c #C7B421", "g@ c #7A630B", "h@ c #444479", "i@ c #44447A", "j@ c #45457A", "k@ c #36367B", "l@ c #9193B1", "m@ c #D1D5CF", "n@ c #CCCECB", "o@ c #585958", "p@ c #848584", "q@ c #E5E6E3", "r@ c #DBDED6", "s@ c #3C3C88", "t@ c #414176", "u@ c #424276", "v@ c #424277", "w@ c #5D545B", "x@ c #A18416", "y@ c #A28001", "z@ c #9B7C00", "A@ c #957700", "B@ c #8F7200", "C@ c #896D00", "D@ c #836800", "E@ c #7D6401", "F@ c #7B650F", "G@ c #544E60", "H@ c #48487E", "I@ c #48487F", "J@ c #49497F", "K@ c #3D3D7E", "L@ c #8183AA", "M@ c #CFD2CC", "N@ c #D1D2CF", "O@ c #575756", "P@ c #808180", "Q@ c #E7E9E6", "R@ c #D9DCD5", "S@ c #383987", "T@ c #45457B", "U@ c #46467C", "V@ c #46467D", "W@ c #47477D", "X@ c #47477E", "Y@ c #494980", "Z@ c #4A4A81", "`@ c #4B4B82", " # c #4B4B83", ".# c #4C4C84", "+# c #4D4D85", "@# c #454583", "## c #7073A3", "$# c #CDD1CB", "%# c #D3D6D1", "&# c #525252", "*# c #EAEBE8", "=# c #D7DAD2", "-# c #202184", ";# c #3B3C87", "># c #3B3C88", ",# c #3B3B88", "'# c #3B3C89", ")# c #3C3C89", "!# c #3C3C8A", "~# c #3C3D8A", "{# c #3D3D8A", "]# c #373889", "^# c #66689F", "/# c #CBCFC8", "(# c #D7D9D5", "_# c #4D4D4D", ":# c #787878", "<# c #EAECE9", "[# c #D1D4CE", "}# c #CED2CA", "|# c #CED1CA", "1# c #CDD1C9", "2# c #CDD0C9", "3# c #CCD0C8", "4# c #CCCFC8", "5# c #CBCFC7", "6# c #CBCEC7", "7# c #CACEC6", "8# c #AEB0AB", "9# c #B3B6AF", "0# c #C9CCC5", "a# c #C8CCC4", "b# c #C8CBC4", "c# c #C7CBC4", "d# c #C7CAC3", "e# c #C6CAC3", "f# c #C6C9C3", "g# c #C5C9C3", "h# c #C5C8C2", "i# c #C4C8C2", "j# c #C5C9C2", "k# c #D9DBD7", "l# c #4A4A4A", "m# c #D4D6D2", "n# c #EBECE9", "o# c #E9EBE7", "p# c #E8EAE6", "q# c #E7E9E5", "r# c #E6E8E5", "s# c #E6E8E4", "t# c #E4E6E2", "u# c #E3E6E1", "v# c #E2E5E1", "w# c #E2E4E0", "x# c #E1E3DF", "y# c #E0E2DE", "z# c #DFE2DD", "A# c #DEE1DC", "B# c #DEE0DC", "C# c #DDDFDB", "D# c #DCDEDA", "E# c #C0C2BE", "F# c #4D4D4C", "G# c #747474", "H# c #6E6E6E", "I# c #6C6C6C", "J# c #6A6A6A", "K# c #686868", "L# c #676767", "M# c #656565", "N# c #636363", "O# c #616161", "P# c #5F5F5F", "Q# c #5C5C5C", "R# c #5A5A5A", "S# c #585858", "T# c #565656", "U# c #555555", "V# c #535353", "W# c #515151", "X# c #4F4F4F", "Y# c #4C4C4C", "Z# c #484848", "`# c #4D504C", " $ c #565855", ".$ c #777A76", "+$ c #81837F", "@$ c #767874", "#$ c #545753", "$$ c #4C4E4B", "%$ c #4F504E", "&$ c #838581", "*$ c #ACAFA9", "=$ c #ADB0AA", "-$ c #8B8E89", ";$ c #81837E", ">$ c #4E504D", ",$ c #525451", "'$ c #9B9E9A", ")$ c #AFB2AC", "!$ c #B1B3AE", "~$ c #AEB1AB", "{$ c #A9ABA6", "]$ c #959993", "^$ c #4F524E", "/$ c #3C3E3C", "($ c #595A57", "_$ c #878A85", ":$ c #A6A8A4", "<$ c #BFC0BD", "[$ c #C9CBC8", "}$ c #CED0CD", "|$ c #CFD1CD", "1$ c #BEC1BE", "2$ c #A8ABA6", "3$ c #8C8E8A", "4$ c #373837", "5$ c #494A46", "6$ c #50524F", "7$ c #5A5C58", "8$ c #646763", "9$ c #6B6E6A", "0$ c #646662", "a$ c #595B57", "b$ c #50524E", "c$ c #454644", "                                                                ", "                                                                ", "      . + @ @ @ @ @ @ @ @ @ @ # $ % & * = - ; > , ' ) ! ~       ", "      { ] ^ ^ ^ ^ ^ ^ / / / / ( ( _ _ : : : < < < [ } | )       ", "      1 2 3 4 5 5 6 7 8 9 0 a b c d e f g h i j k l m n o       ", "      p q r s t u v w x y z A B C D E F G G H I J K L M N       ", "      O P Q R S T U V W X Y Z `  ...+.@.#.$.%.&.*.=.-.;.>.      ", "      ,.'.).!.~.G G H {.].^./.(._.:.<.[.}.|.1.2.3.4.5.6.7.      ", "      8.9.0.a.b.c.d.e.f.g.h.i.j.k.l.m.n.o.p.q.r.s.t.u.v.w.      ", "      x.y.z.a.A.A.i.j.B.C.D.E.E.F.G.H.I.J.K.K.L.L.M.N.O.O.      ", "      P.Q.R.j.S.T.U.V.W.X.Y.Z.`. +.+++@+#+$+%+&+*+=+-+;+>+      ", "    ,+'+)+!+~+{+{+]+^+/+(+_+:+<+[+}+|+1+2+3+4+5+6+7+8+9+0+a+    ", "    b+Y c+d+e+f+g+h+i+j+k+l+m+n+o+p+q+r+s+t+u+v+v+w+x+y+z+A+    ", "    B+C+D+E+F+G+G+H+i+I+J+l+m+n+o+p+q+K+L+M+N+O+O+P+Q+R+S+T+    ", "    # U+V+W+X+Y+Z+`+ @.@+@l+m+n+o+p+q+K+@@M+#@#@$@%@&@*@=@A+    ", "    -@;@>@,@`+'@)@#@!@~@{@l+m+n+o+p+q+]@^@M+/@/@(@_@:@<@[@}@    ", "    & |@1@2@3@4@5@5@6@7@8@9@0@a@b@c@d@e@f@g@h@i@j@k@l@m@n@o@    ", "    p@q@r@s@t@u@v@v@w@x@y@z@A@B@C@D@M+E@F@G@H@I@J@K@L@M@N@O@    ", "    P@Q@R@S@T@U@U@V@W@X@H@I@J@Y@Y@Z@Z@`@`@ #.#.#+#@###$#%#&#    ", "    ~ *#=#-#;#>#,#,#>#'#)#)#)#'#'#)#!#~#~#~#{#~#~#]#^#/#(#_#    ", "    :#<#[#}#|#1#2#2#3#4#5#6#7#8#9#0#a#b#c#d#e#f#g#h#i#j#k#l#    ", "    :#m#n#n#;.*#o#p#p#q#r#s#v.c+t#u#v#w#x#x#y#z#A#B#C#D#E#F#    ", "      G#H#I#J#K#L#M#N#O#P#A+Q#R#S#T#U#V#W#X#_#Y#l#Z#Z#Z#_#      ", "                    `# $.$+$+$+$+$+$+$@$#$$$                    ", "                  %$&$*$=$-$-$-$-$-$-$=$=$;$>$                  ", "                  ,$'$)$!$)$~$=$=$~$~$=${$]$^$                  ", "                  /$($_$:$<$[$}$|$[@1$2$3$ $4$                  ", "                      5$6$7$8$9$9$0$a$b$c$                      ", "                                                                ", "                                                                ", "                                                                ", "                                                                "}; """,
'process-stop': """/* XPM */ static char * process_stop_xpm[] = { "32 32 369 2", "  \tc None", ". \tc #AF3333", "+ \tc #C34848", "@ \tc #C34747", "# \tc #C34646", "$ \tc #C34444", "% \tc #C34343", "& \tc #B63636", "* \tc #900202", "= \tc #C24747", "- \tc #EC7474", "; \tc #E15757", "> \tc #E15656", ", \tc #E15454", "\' \tc #E15353", ") \tc #E05151", "! \tc #E05050", "~ \tc #E76262", "{ \tc #CE4F4F", "] \tc #910404", "^ \tc #C64E4E", "/ \tc #EB7171", "( \tc #D94242", "_ \tc #D94343", ": \tc #D94141", "< \tc #D94040", "[ \tc #D93F3F", "} \tc #D83E3E", "| \tc #D83D3D", "1 \tc #D83C3C", "2 \tc #D83B3B", "3 \tc #E45B5B", "4 \tc #D25252", "5 \tc #8F0404", "6 \tc #C74F4F", "7 \tc #EA7171", "8 \tc #DA4444", "9 \tc #E55A5A", "0 \tc #CE4E4E", "a \tc #C84F4F", "b \tc #EA7272", "c \tc #DA4545", "d \tc #DA4646", "e \tc #D83A3A", "f \tc #E45959", "g \tc #CD4848", "h \tc #CB5353", "i \tc #DA4747", "j \tc #D73A3A", "k \tc #D63939", "l \tc #C84545", "m \tc #CC5656", "n \tc #DA4848", "o \tc #DC4646", "p \tc #E03F3F", "q \tc #D93C3C", "r \tc #DE3434", "s \tc #D73C3C", "t \tc #D63A3A", "u \tc #D53939", "v \tc #D43838", "w \tc #E35858", "x \tc #C84343", "y \tc #CE5656", "z \tc #EA6E6E", "A \tc #DB4545", "B \tc #F42727", "C \tc #F52F2F", "D \tc #E23A3A", "E \tc #DA3E3E", "F \tc #F22424", "G \tc #E03030", "H \tc #D53A3A", "I \tc #D43939", "J \tc #D33838", "K \tc #D23737", "L \tc #E15555", "M \tc #C63E3E", "N \tc #CC5757", "O \tc #E96B6B", "P \tc #DC4242", "Q \tc #E2B2B2", "R \tc #DED8D8", "S \tc #F33C3C", "T \tc #E33838", "U \tc #DB3D3D", "V \tc #F42424", "W \tc #E4AFAF", "X \tc #DDD8D8", "Y \tc #F24141", "Z \tc #E03131", "` \tc #D03535", " .\tc #E05353", "..\tc #C13B3B", "+.\tc #960D0D", "@.\tc #EF7D7D", "#.\tc #F42626", "$.\tc #E4ACAC", "%.\tc #DEDEDE", "&.\tc #DFDFDF", "*.\tc #E1D7D7", "=.\tc #F53939", "-.\tc #E23838", ";.\tc #DA3F3F", ">.\tc #F32C2C", ",.\tc #E7ABAB", "\'.\tc #E0E0E0", ").\tc #DED6D6", "!.\tc #F44242", "~.\tc #DB3434", "{.\tc #D23838", "].\tc #D03636", "^.\tc #CF3535", "/.\tc #CE3434", "(.\tc #E65D5D", "_.\tc #940A0A", ":.\tc #ED7777", "<.\tc #EC2E2E", "[.\tc #EC7575", "}.\tc #E2E2E2", "|.\tc #E4DBDB", "1.\tc #F54545", "2.\tc #E13A3A", "3.\tc #DA4040", "4.\tc #F43535", "5.\tc #E9B1B1", "6.\tc #E3E3E3", "7.\tc #E1E1E1", "8.\tc #E4C2C2", "9.\tc #F43838", "0.\tc #D63737", "a.\tc #D13737", "b.\tc #E45757", "c.\tc #ED7676", "d.\tc #EC3434", "e.\tc #EF7C7C", "f.\tc #E4E4E4", "g.\tc #E5E5E5", "h.\tc #E6E6E6", "i.\tc #E7DFDF", "j.\tc #F64F4F", "k.\tc #F63939", "l.\tc #EBB7B7", "m.\tc #E7C5C5", "n.\tc #F44040", "o.\tc #D63838", "p.\tc #D13838", "q.\tc #D03737", "r.\tc #CD3333", "s.\tc #E35656", "t.\tc #930A0A", "u.\tc #ED7575", "v.\tc #EC3C3C", "w.\tc #F08383", "x.\tc #E7E7E7", "y.\tc #E8E8E8", "z.\tc #E9E9E9", "A.\tc #EAE2E2", "B.\tc #EDCBCB", "C.\tc #EBCACA", "D.\tc #F44949", "E.\tc #CF3636", "F.\tc #CE3535", "G.\tc #CC3434", "H.\tc #CB3232", "I.\tc #E25555", "J.\tc #EB4343", "K.\tc #F38484", "L.\tc #EBEBEB", "M.\tc #ECECEC", "N.\tc #EECACA", "O.\tc #F45151", "P.\tc #CD3535", "Q.\tc #CB3333", "R.\tc #CA3232", "S.\tc #E25353", "T.\tc #ED4A4A", "U.\tc #F39D9D", "V.\tc #EEEEEE", "W.\tc #EFDBDB", "X.\tc #F65A5A", "Y.\tc #CF3434", "Z.\tc #CB2828", "`.\tc #C81F1F", " +\tc #C51818", ".+\tc #C31515", "++\tc #C21212", "@+\tc #C01010", "#+\tc #DC3636", "$+\tc #900404", "%+\tc #950B0B", "&+\tc #EC7373", "*+\tc #D73939", "=+\tc #F45757", "-+\tc #F2C4C4", ";+\tc #F0F0F0", ">+\tc #F1F1F1", ",+\tc #F1EAEA", "\'+\tc #F77272", ")+\tc #D72C2C", "!+\tc #C50B0B", "~+\tc #C10101", "{+\tc #C00000", "]+\tc #BF0000", "^+\tc #BE0000", "/+\tc #BD0000", "(+\tc #BC0000", "_+\tc #BB0000", ":+\tc #D92828", "<+\tc #8E0000", "[+\tc #EC7171", "}+\tc #D73838", "|+\tc #DA3C3C", "1+\tc #F55D5D", "2+\tc #F2CECE", "3+\tc #F2F2F2", "4+\tc #F3F3F3", "5+\tc #F4F4F4", "6+\tc #F1EDED", "7+\tc #F47878", "8+\tc #D21D1D", "9+\tc #BA0000", "0+\tc #D92727", "a+\tc #EC7070", "b+\tc #D73636", "c+\tc #D73737", "d+\tc #F46262", "e+\tc #F3CACA", "f+\tc #F5F5F5", "g+\tc #F7E0E0", "h+\tc #F7B5B5", "i+\tc #F6F6F6", "j+\tc #F2ECEC", "k+\tc #F57C7C", "l+\tc #CE1B1B", "m+\tc #B90000", "n+\tc #D82626", "o+\tc #EC6D6D", "p+\tc #D73535", "q+\tc #D83939", "r+\tc #F46A6A", "s+\tc #F8E1E1", "t+\tc #F46B6B", "u+\tc #E64949", "v+\tc #F7AAAA", "w+\tc #F1ECEC", "x+\tc #F48787", "y+\tc #CC1F1F", "z+\tc #B80000", "A+\tc #D82424", "B+\tc #EC6B6B", "C+\tc #D63434", "D+\tc #F46F6F", "E+\tc #F0CDCD", "F+\tc #F8E3E3", "G+\tc #F47575", "H+\tc #C90A0A", "I+\tc #C30000", "J+\tc #E34E4E", "K+\tc #F8B3B3", "L+\tc #EFEBEB", "M+\tc #F48E8E", "N+\tc #C71919", "O+\tc #B70000", "P+\tc #D72323", "Q+\tc #8C0000", "R+\tc #940606", "S+\tc #E66969", "T+\tc #DD4444", "U+\tc #D63333", "V+\tc #EC6666", "W+\tc #F4B3B3", "X+\tc #F6E3E3", "Y+\tc #F47A7A", "Z+\tc #C90B0B", "`+\tc #C20000", " @\tc #C10000", ".@\tc #F6B4B4", "+@\tc #F1E2E2", "@@\tc #F28888", "#@\tc #BF0C0C", "$@\tc #B70101", "%@\tc #DA2727", "&@\tc #950C0C", "*@\tc #E36363", "=@\tc #DF4646", "-@\tc #D63131", ";@\tc #D63232", ">@\tc #D52F2F", ",@\tc #D12121", "\'@\tc #E65A5A", ")@\tc #F5B3B3", "!@\tc #F5DFDF", "~@\tc #F38080", "{@\tc #C70909", "]@\tc #DE5454", "^@\tc #F5B8B8", "/@\tc #F3E3E3", "(@\tc #F28C8C", "_@\tc #BE0A0A", ":@\tc #D62323", "<@\tc #AB0F0F", "[@\tc #960A0A", "}@\tc #DD4B4B", "|@\tc #D92424", "1@\tc #CC0606", "2@\tc #C90000", "3@\tc #C80000", "4@\tc #C70000", "5@\tc #E76363", "6@\tc #F58B8B", "7@\tc #C80C0C", "8@\tc #E05C5C", "9@\tc #F59090", "0@\tc #C00E0E", "a@\tc #B80202", "b@\tc #D52323", "c@\tc #A60D0D", "d@\tc #920303", "e@\tc #D41818", "f@\tc #C60000", "g@\tc #C50000", "h@\tc #C50202", "i@\tc #BB0202", "j@\tc #B70303", "k@\tc #D62424", "l@\tc #910303", "m@\tc #D21717", "n@\tc #C40000", "o@\tc #B60000", "p@\tc #D52424", "q@\tc #A00B0B", "r@\tc #D11616", "s@\tc #B80303", "t@\tc #9F0A0A", "u@\tc #860101", "v@\tc #D53434", "w@\tc #CF1818", "x@\tc #B90404", "y@\tc #9A0909", "z@\tc #830303", "A@\tc #D33333", "B@\tc #CD1515", "C@\tc #C20505", "D@\tc #C10505", "E@\tc #C00505", "F@\tc #BF0404", "G@\tc #BE0404", "H@\tc #BC0404", "I@\tc #BB0404", "J@\tc #BA0404", "K@\tc #BB0606", "L@\tc #D42525", "M@\tc #950909", "N@\tc #810101", "O@\tc #C52828", "P@\tc #CE2C2C", "Q@\tc #CC2B2B", "R@\tc #CB2929", "S@\tc #CA2626", "T@\tc #CA2525", "U@\tc #CA2323", "V@\tc #C82222", "W@\tc #C92222", "X@\tc #C72121", "Y@\tc #920808", "Z@\tc #470000", "`@\tc #460000", " #\tc #480000", "                    . + + + @ @ @ # $ $ % & *                   ", "                  = - ; ; > > > > , \' ) ! ~ { ]                 ", "                ^ / ( _ ( ( : : < [ } | 1 2 3 4 5               ", "              6 7 8 8 8 8 _ _ ( : < [ } | 1 2 9 0               ", "            a b c c d d c c 8 _ ( : < [ } 1 2 e f g             ", "          h b c d i i i i d c 8 _ ( < [ } | 1 j k f l           ", "        m 7 8 c i n o p n i d 8 _ ( : [ q r s t u v w x         ", "      y z _ 8 c i A B C D i d c _ ( : E F C G H I J K L M       ", "    N O : _ 8 c P B Q R S T c 8 _ ( U V W X Y Z I J K `  ...    ", "  +.@.< : ( _ 8 #.$.%.&.*.=.-._ ( ;.>.,.\'.&.).!.~.{.].^./.(._.  ", "  +.:.[ < : ( _ <.[.\'.}.}.|.1.2.3.4.5.6.}.7.8.9.0.a.].^./.b._.  ", "  +.c.} [ < : : ( d.e.f.g.h.i.j.k.l.h.g.f.m.n.o.p.q.^./.r.s.t.  ", "  +.u.| } [ [ < : : v.w.x.y.z.A.B.z.z.y.C.D.k p.q.E.F.G.H.I.t.  ", "  +.u.1 | | } [ [ [ [ J.K.L.L.M.M.M.L.N.O.H p.q.E.P.G.Q.R.S.t.  ", "  +.- 2 2 1 | | | } } } T.U.V.V.V.V.W.X.H p.Y.Z.`. +.+++@+#+$+  ", "  %+&+*+e 2 2 2 1 1 1 q =+-+;+>+>+>+,+\'+)+!+~+{+]+^+/+(+_+:+<+  ", "  %+[+}+}+*+e e e e |+1+2+3+4+5+5+4+3+6+7+8+{+]+^+/+(+_+9+0+<+  ", "  %+a+b+c+}+}+}+*+e d+e+3+5+f+g+h+i+5+4+j+k+l+^+/+(+_+9+m+n+<+  ", "  %+o+p+b+b+b+c+q+r+2+>+5+i+s+t+u+v+i+5+3+w+x+y+(+_+9+m+z+A+<+  ", "  _.B+C+C+C+p+p+D+E+;+3+f+F+G+H+I+J+K+i+4+>+L+M+N+9+m+z+O+P+Q+  ", "  R+S+T+U+U+U+C+V+W+;+4+X+Y+Z+I+`+ @S..@5+>++@@@#@m+z+O+$@%@Q+  ", "    &@*@=@-@;@>@,@\'@)@!@~@{@I+`+ @{+]+]@^@/@(@_@m+z+O+$@:@<@    ", "      [@}@|@1@2@3@4@5@6@7@I+`+ @{+]+^+/+8@9@0@m+z+O+a@b@c@      ", "        d@E e@3@4@f@g@h@I+`+ @{+]+^+/+(+_+i@m+z+O+j@k@c@        ", "          l@2 m@f@g@n@I+`+ @{+]+^+/+(+_+9+m+z+o@j@p@q@          ", "            l@}+r@n@I+`+ @{+]+^+/+(+_+9+m+O+o@s@p@t@            ", "              u@v@w@`+ @{+]+^+/+(+_+9+z+O+o@x@p@y@              ", "                z@A@B@C@C@D@E@F@G@H@I@J@x@K@L@M@                ", "                  N@O@P@Q@R@Z.S@S@T@U@V@W@X@Y@                  ", "                            Z@Z@`@Z@ #                          ", "                                                                ", "                                                                "}; """,
}

def runFtpD( userdir=r"/", username=u"user", userpass=u"12345",
            serverpermitions=u"elradfmw", anonymousdir=None, 
            serverip=u"127.0.0.1", serverport=21010):
    """runFtpD( userdir=r"/", username=u"user", userpass=u"12345",
            serverpermitions=u"elradfmw", anonymousdir=None, 
            serverip=u"127.0.0.1", serverport=21010) - run ftpd server"""

    authorizer = DummyAuthorizer()
    authorizer.add_user(username, userpass, userdir,
                        perm=serverpermitions)
    if anonymousdir:
        authorizer.add_anonymous(anonymousdir)

    handler = FTPHandler
    handler.authorizer = authorizer
    server = FTPServer((serverip, serverport), handler)
    return server.serve_forever()

if os.name != "nt":
    import fcntl
    import struct

    def get_interface_ip(ifname):
        '''get_interface_ip(ifname) - get ip from interface string'''
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        return socket.inet_ntoa(fcntl.ioctl(s.fileno(), 0x8915,
                                struct.pack('256s', ifname[:15]))[20:24])


def get_lan_ip():
    '''get_lan_ip() - get current pc ip'''
    ip = socket.gethostbyname(socket.gethostname())
    if ip.startswith("127.") and os.name != "nt":
        interfaces = [
                      "eth0",
                      "eth1",
                      "eth2",
                      "wlan0",
                      "wlan1",
                      "wifi0",
                      "ath0",
                      "ath1",
                      "ppp0",
                      ]
        for ifname in interfaces:
            try:
                ip = get_interface_ip(ifname)
                break
            except IOError:
                pass
    return ip


def getIcon(iconname):
    """getIcon(iconname) - get icon data by icon name"""
    newPixmap = QPixmap()
    newPixmap.loadFromData(TANGO_ICONS[iconname])
    return QIcon(newPixmap)


class FtpdX(QMainWindow):
    """FtpdX - gui ftpd server"""
    def __init__(self):
        '''__init__(self) - init FtpdX instance'''
        super(FtpdX, self).__init__()
#init class constants
        self.homePath = os.path.expanduser('~')
        self.baseDir = u''+os.getcwd()
        self.procftp = None
        self.startPath = None
        self.initUI()

    def initUI(self):
        '''initUI(self) - init Ui ftpserx'''
        self.statusBar()
#self.setGeometry(100, 100, 400, 400)
        self.setWindowIcon(getIcon('folder-remote'))
        self.setMinimumSize(570, 460)
        self.setWindowTitle(u'ftpservX')

        window = QWidget()
        commonLayout = QVBoxLayout()
        buttonsLayout = QHBoxLayout()
        confLayout = QVBoxLayout()
        pathLayout = QHBoxLayout()
        addressLayout = QHBoxLayout()
        authorizationLayout = QHBoxLayout()
        premitionsLayout = QHBoxLayout()
        anonymousLayout = QHBoxLayout()
        logLayout = QVBoxLayout()

        self.pathLabel = QLabel("Path: ")
        self.pathInput = QLineEdit(self.homePath)
        self.pathInput.setToolTip('Set start folder for ftp access')
        self.buttonPath = QPushButton(getIcon('document-open'), "Select Path")
        self.buttonPath.setToolTip('Select start folder for ftp access')
        self.ipLabel = QLabel("IP: ")
        self.ipInput = QLineEdit("0.0.0.0")
        self.ipInput.setToolTip('''Enter "0.0.0.0"
for global FTP-server listening
or "127.0.0.1"
for local FTP-server listening''')
#self.ipInput.setReadOnly(True)
#self.ipInput.setInputMask('000.000.000.000;_')
        self.portLabel = QLabel("Port: ")
        self.portInput = QLineEdit("21010")
        self.portInput.setInputMask("00009;")
        self.portInput.setToolTip('Enter port number for FTP-server listening')
        self.userLabel = QLabel("User Name: ")
        self.userInput = QLineEdit(getpass.getuser())
        self.userInput.setToolTip('Enter FTP-user name')
        self.passwordLabel = QLabel("Password: ")
        self.passwordInput = QLineEdit("12345")
        self.passwordInput.setToolTip('Enter FTP-user password')
        self.permitionsLabel = QLabel("Permitions: ")
        self.permitionsInput = QLineEdit("elradfmw")
        self.permitionsInput.setReadOnly(True)
        premitiontip = r'''Read permissions:
    "e" = change directory
    "l" = list files
    "r" = retrieve file from the server

Write permissions:
    "a" = append data to an existing file
    "d" = delete file or directory
    "f" = rename file or directory
    "m" = create directory
    "w" = store a file to the server
    "M" = change mode/permission'''
        self.permitionsInput.setToolTip(premitiontip)
        self.buttonPermitions = QPushButton(getIcon('system-lock-screen'), "Set Permitions")
        self.buttonPermitions.setToolTip('Wizard to setup premitions')
        self.buttonRunCwd = QPushButton(getIcon('list-add'), self.baseDir)
        self.buttonRunCwd.setToolTip('Run ftpserverx whith start access to current folder')
        self.buttonRunSet = QPushButton(getIcon('network-workgroup'), "&Run FTP-server")
        self.buttonRunSet.setToolTip('Run/stop ftpserverx whith seted settings')
        self.buttonRunSet.setShortcut(QKeySequence(QKeySequence.fromString("Ctrl+R")))
        self.allowAnonymous = QCheckBox("Allow anonymous")
        self.allowAnonymous.setToolTip('Allow anonymous connect to FTP-server')
        self.buttonExit = QPushButton(getIcon('system-log-out'), "Exit")
        self.buttonExit.setToolTip('Exit ftpservx')
        self.logBox = QGroupBox("ftpservX Server log:")

        self.buttonPath.clicked.connect(self.openFolder)
        self.buttonPermitions.clicked.connect(self.setPremition)
        self.buttonRunCwd.clicked.connect(self.RunCwdClicked)
        self.buttonRunSet.clicked.connect(self.RunSetClicked)
        self.buttonExit.clicked.connect(self.exitClicked)

        pathLayout.addWidget(self.pathLabel)
        pathLayout.addWidget(self.pathInput)
        pathLayout.addWidget(self.buttonPath)
        addressLayout.addWidget(self.ipLabel)
        addressLayout.addWidget(self.ipInput)
        addressLayout.addWidget(self.portLabel)
        addressLayout.addWidget(self.portInput)
        authorizationLayout.addWidget(self.userLabel)
        authorizationLayout.addWidget(self.userInput)
        authorizationLayout.addWidget(self.passwordLabel)
        authorizationLayout.addWidget(self.passwordInput)
        premitionsLayout.addWidget(self.permitionsLabel)
        premitionsLayout.addWidget(self.permitionsInput)
        premitionsLayout.addWidget(self.buttonPermitions)
        anonymousLayout.addWidget(self.allowAnonymous)

        confLayout.addLayout(pathLayout)
        confLayout.addLayout(addressLayout)
        confLayout.addLayout(authorizationLayout)
        confLayout.addLayout(premitionsLayout)
        confLayout.addLayout(anonymousLayout)
        buttonsLayout.addWidget(self.buttonRunSet)
        self.logBox.setLayout(logLayout)
        self.textLog = QTextBrowser()
        self.textLog.setOpenLinks(False)
        logLayout.addWidget(self.textLog)

        commonLayout.addLayout(confLayout)
        commonLayout.addLayout(buttonsLayout)
        commonLayout.addWidget(self.logBox)
        commonLayout.addWidget(self.buttonExit)

        window.setLayout(commonLayout)
        self.setCentralWidget(window)
        self.show()

        self.statusBar().showMessage('ftpservx ver. ' + __version__)


    def setPremition(self):
        '''setPremition(self) - run premitions wizard'''
        dlg = PremitionsDialog(self)
        if dlg.exec_():
            values = dlg.getValues()
            if len(values) > 0:
                self.permitionsInput.setText(values)

    def RunSetClicked(self):
        '''RunSetClicked(self) - run ftp server whith setted options'''
        if self.procftp:
            self.procftp.terminate()
            self.procftp = None
            self.buttonRunSet.setIcon(getIcon('network-workgroup'))
            self.buttonRunSet.setText('&Run FTP-server')
            self.buttonRunSet.setShortcut(QKeySequence(QKeySequence.fromString("Ctrl+R")))
            self.statusBar().showMessage(str(self.procftp))
            self.textLog.append('Server is stopped')
        else:
            ip_get = re.search(r'\b(?:[0-9]{1,3}\.){3}[0-9]{1,3}\b', self.ipInput.text())
            if ip_get:
                server_ip = ip_get.group(0)
            else:
                self.statusBar().showMessage("Error in IP: " + self.ipInput.text())
                return
            try:
                port_n = int(self.portInput.text())
            except ValueError:
                self.statusBar().showMessage("Port number ValueError: " + self.portInput.text())
                return
            if port_n < 1 or port_n > 65535:
                self.statusBar().showMessage("Port number not in range (1, 65535): " + self.portInput.text())
                return
            if self.userInput.text() == '':
                self.statusBar().showMessage("self.userInput.text(): " + self.userInput.text())
                return
            if self.passwordInput.text() == '':
                self.statusBar().showMessage("self.passwordInput.text(): " + self.passwordInput.text())
                return
            if self.permitionsInput.text() == '':
                self.statusBar().showMessage("self.permitionsInput.text(): " + self.permitionsInput.text())
                return
            if self.allowAnonymous.isChecked():
                anonimpath = str(self.pathInput.text())
            else:
                anonimpath = None

            self.procftp = Process(target=runFtpD,
                                   args=(str(self.pathInput.text()),
                                         str(self.userInput.text()),
                                         str(self.passwordInput.text()),
                                         str(self.permitionsInput.text()),
                                         anonimpath,
                                         str(server_ip),
                                         port_n
                                         ))
            self.procftp.start()
            ftp_link = '<a href="ftp://' + get_lan_ip() + ':' + \
                        self.portInput.text() + '">ftp://' + get_lan_ip() + \
                        ':' + self.portInput.text()+'</a>'
            self.buttonRunSet.setText('&Stop FTP-server')
            self.buttonRunSet.setIcon(getIcon('process-stop'))
            self.buttonRunSet.setShortcut(QKeySequence(QKeySequence.fromString("Ctrl+S")))
            self.textLog.append('Server ' + ftp_link + ' is started at ' + self.pathInput.text())
            self.statusBar().showMessage(self.pathInput.text())

    def RunCwdClicked(self):
        '''RunCwdClicked(self) - run ftp server whith current path to sharing by ftp'''
        self.RunFtpPath(self.baseDir)

    def openFolder(self):
        '''openFolder(self) - select path to sharing by ftp'''
        if not self.startPath:
# for os windows
            self.startPath = './'

        self.path = QFileDialog.getExistingDirectory(self, 
                        caption='Select Directory', 
                        directory=self.startPath.__str__()
                            ).encode('utf-8')

        if self.path:
# for PySide
            if type(self.path) is tuple:
                self.path = self.path[0]
            if self.path:
                self.startPath = self.path
                self.pathInput.setText(self.path.__str__().decode('utf-8'))
                self.statusBar().showMessage("Open: "+self.path)
        else:
            self.statusBar().showMessage(u'Stop Open Path')

    def RunFtpPath(self, ftppath):
        '''RunFtpPath(self, ftppath) - run FTP-server at setted path'''
        if self.procftp:
            self.procftp.terminate()
            self.procftp = None
            self.textLog.append('Server is stopped')
            self.statusBar().showMessage(str(self.procftp))
        else:
            self.procftp = Process(target=runFtpD,
                                   args=(str(ftppath),
                                         str(self.userInput.text()),
                                         str(self.passwordInput.text()),
                                         str(self.permitionsInput.text()),
                                         None,
                                         str(self.ipInput.text()),
                                         int(self.portInput.text())
                                         ))
            self.procftp.start()
            ftp_link = '<a href="ftp://' + get_lan_ip() + ':' + self.portInput.text() + '">ftp://' + get_lan_ip() + ':' + self.portInput.text()+'</a>'
            self.textLog.append('Server ' + ftp_link + ' is started at ' + ftppath)

    def exitClicked(self):
        '''exitClicked(self) - exit clicked'''
        if self.procftp:
            self.procftp.terminate()
        sys.exit()

    def closeEvent(self, event):
        '''closeEvent(self) - close button clicked'''
        self.exitClicked()
        event.accept()


class PremitionsDialog(QDialog):
    """PremitionsDialog - set premition dialog"""
    def __init__(self, parent=None):
        '''__init__(self) - init PremitionsDialog instance'''
        QDialog.__init__(self, parent)
        self.rulesstr = parent.permitionsInput.text()
        self.setupUi()
        self.setWindowTitle(u'Set premitions')
        self.setWindowIcon(getIcon('system-lock-screen'))

    def setupUi(self):
        '''setupUi(self) - setup Ui wizard'''
        commonLayout = QVBoxLayout()
        readLayout = QVBoxLayout()
        self.readRulesBox = QGroupBox("Read premitions:")
        self.readChangeDirectory = QCheckBox('"e" = change directory', self.readRulesBox)
        self.readChangeDirectory.setToolTip('"e" = change directory (CWD, CDUP commands)')
        readLayout.addWidget(self.readChangeDirectory)
        self.readListDirectory = QCheckBox('"l" = list files', self.readRulesBox)
        self.readListDirectory.setToolTip('"l" = list files (LIST, NLST, STAT, MLSD, MLST, SIZE commands)')
        readLayout.addWidget(self.readListDirectory)
        self.readRetrieveFile = QCheckBox('"r" = retrieve file from the server', self.readRulesBox)
        self.readRetrieveFile.setToolTip('"r" = retrieve file from the server (RETR command)')
        readLayout.addWidget(self.readRetrieveFile)
        self.readRulesBox.setLayout(readLayout)
        commonLayout.addWidget(self.readRulesBox)

        writeLayout = QVBoxLayout()
        self.writeRulesBox = QGroupBox("Write premitions:")
        self.writeAppendData = QCheckBox('"a" = append data to an existing file', self.writeRulesBox)
        self.writeAppendData.setToolTip('"a" = append data to an existing file (APPE command)')
        writeLayout.addWidget(self.writeAppendData)
        self.writeDeleteFile = QCheckBox('"d" = delete file or directory', self.writeRulesBox)
        self.writeDeleteFile.setToolTip('"d" = delete file or directory (DELE, RMD commands)')
        writeLayout.addWidget(self.writeDeleteFile)
        self.writeRename = QCheckBox('"f" = rename file or directory', self.writeRulesBox)
        self.writeRename.setToolTip('"f" = rename file or directory (RNFR, RNTO commands)')
        writeLayout.addWidget(self.writeRename)
        self.writeCreateDirectory = QCheckBox('"m" = create directory', self.writeRulesBox)
        self.writeCreateDirectory.setToolTip('"m" = create directory (MKD command)')
        writeLayout.addWidget(self.writeCreateDirectory)
        self.writeStoreFile = QCheckBox('"w" = store a file to the server', self.writeRulesBox)
        self.writeStoreFile.setToolTip('"w" = store a file to the server (STOR, STOU commands)')
        writeLayout.addWidget(self.writeStoreFile)
        self.writeChangeMode = QCheckBox('"M" = change mode/permission', self.writeRulesBox)
        self.writeChangeMode.setToolTip('"M" = change mode/permission (SITE CHMOD command)')
        writeLayout.addWidget(self.writeChangeMode)
        self.writeRulesBox.setLayout(writeLayout)
        commonLayout.addWidget(self.writeRulesBox)

        self.buttonBox = QDialogButtonBox(self)
        commonLayout.addWidget(self.buttonBox)

        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QDialogButtonBox.Ok)
        QtCore.QObject.connect(self.buttonBox,
                               QtCore.SIGNAL("accepted()"),
                               self.accept)
        QtCore.QMetaObject.connectSlotsByName(self)

        self.setLayout(commonLayout)

        self.setValues()

    def setValues(self):
        '''setValues(self) - set premitions value from parent'''
        if 'e' in self.rulesstr:
            self.readChangeDirectory.setChecked(True)
        if 'l' in self.rulesstr:
            self.readListDirectory.setChecked(True)
        if 'r' in self.rulesstr:
            self.readRetrieveFile.setChecked(True)

        if 'a' in self.rulesstr:
            self.writeAppendData.setChecked(True)
        if 'd' in self.rulesstr:
            self.writeDeleteFile.setChecked(True)
        if 'f' in self.rulesstr:
            self.writeRename.setChecked(True)
        if 'm' in self.rulesstr:
            self.writeCreateDirectory.setChecked(True)
        if 'w' in self.rulesstr:
            self.writeStoreFile.setChecked(True)
        if 'M' in self.rulesstr:
            self.writeChangeMode.setChecked(True)

    def getValues(self):
        '''getValues(self) - get premitions string'''
        rulesstr = ''
        if self.readChangeDirectory.isChecked():
            rulesstr += 'e'
        if self.readListDirectory.isChecked():
            rulesstr += 'l'
        if self.readRetrieveFile.isChecked():
            rulesstr += 'r'

        if self.writeAppendData.isChecked():
            rulesstr += 'a'
        if self.writeDeleteFile.isChecked():
            rulesstr += 'd'
        if self.writeRename.isChecked():
            rulesstr += 'f'
        if self.writeCreateDirectory.isChecked():
            rulesstr += 'm'
        if self.writeStoreFile.isChecked():
            rulesstr += 'w'
        if self.writeChangeMode.isChecked():
            rulesstr += 'M'

        return rulesstr


def main():
    '''main() - main loop ftpservx'''
    app = QApplication(sys.argv)
    w = FtpdX()
    app.exec_()


if __name__ == "__main__":
    main()
    sys.exit()
