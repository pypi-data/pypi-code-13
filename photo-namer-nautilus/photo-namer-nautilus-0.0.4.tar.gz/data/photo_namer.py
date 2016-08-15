#!/usr/bin/env python3

HELP = """
    Nautilus scripts NAMER for photo app. Names choosen files and his
    counterpart (RAW file for example). File pairs (chosen and counterpart)
    will be searched two levels avove and underneath. All found pairs will
    Named.

    - A new name will appended on the old one and spcaces will replaced by
    under scores.

    - Value of three stars: *** trigger naming the other side with the name
    of the selected

    - Dependences:
    Zenety must be insalled


    Copyright (c) 2012 Andreas Fritz

    Permission is hereby granted, free of charge, to any person obtaining a copy of
    this software and associated documentation files (the "Software"), to deal in the
    Software without restriction, including without limitation the rights to use, copy,
    modify, merge, publish, distribute, sublicense, and/or sell copies of the Software,
    and to permit persons to whom the Software is furnished to do so, subject to the
    following conditions:

    The above copyright notice and this permission notice shall be included in all
    copies or substantial portions of the Software.

    THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED,
    INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A
    PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT
    HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION
    OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE
    SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
"""

# set desired logging mode: DEBUG for development or INFO for production run
LOGGING_MODE = 'INFO'

import logging
import unittest
import os
import sys
import urllib.parse
import shutil
import re
import subprocess

# info
try:
    sys.argv[1]
except IndexError:
    print('No arguments, use: photo-namer-nautilus --help')
    sys.exit()

if sys.argv[1] == '--help':
        print(os.system('cat %s/.local/share/photo-namer-nautilus/README.rst'
                        % os.environ['HOME']))
        sys.exit()

# Setup logging

# choose desired level
if LOGGING_MODE == 'DEBUG':
    lev = logging.DEBUG  # for development
elif LOGGING_MODE == 'INFO':
    lev = logging.INFO  # for production run
else:
    raise NameError('%s is not allowed. allowed is: DEBUG or INFO')

logpath = '%s/.%s.log' % (os.environ['HOME'], 'photo-namer')
logging.basicConfig(
filename=logpath,
format='%(levelname)s: %(module)s: %(funcName)s: \
%(lineno)d: %(message)s',
filemode='w',
level=lev,
)

logging.debug('Debug logging is enabled!')
logging.error('Error logging is enabled!')
logging.info('Info logging is enabled')


# test of python 3
if not sys.version_info[0] > 2:
    message = 'script must run under python 3! current python version \
    running the script: %s' % sys.version_info
    logging.debug(message)
    raise SystemError(message)


# For processing as nautilus script
def file_uri_to_path(uri):
    """ Converts a file uri to a path.
        Eg.: if uri is "file:///home/rafaelb" then "/home/rafaelb" is returned.
    """
    if not uri.startswith("file://"):
        return uri

    return urllib.parse.unquote(uri.replace('file://', ''))

nautilus_current_path = file_uri_to_path(os.environ.get('NAUTILUS_SCRIPT_CURRENT_URI', ''))
"""Current absolute path."""

nautilus_files = sys.argv[1:]
"""Selected file names."""

nautilus_paths = [os.path.join(nautilus_current_path, f) for f in nautilus_files]
"""Sequence containing the absolute paths for the selected files."""

"""
Nautilus Script Usage

if nautilus paths:
    for I in nautilus_paths:
        os.system('nautilus %s' % I)
else:
    os.system('nautilus %s' % nautilus_current_path)
"""

logging.debug('Variable: "nautilus_current_path" is: %s' % nautilus_current_path)
logging.debug('Variable: "nautilus_files" is: %s' % nautilus_files)
logging.debug('Variable: "nautilus_paths" is: %s' % nautilus_paths)


# Test if delete in the systems bin is possible
test_trash_cli = os.path.isfile('/usr/local/bin/trash-put')


class TestInut(unittest.TestCase):
    def setUp(self):
        LOGGING_MODE = 'DEBUG'

    def test_file_uri_to_path(self):
        test_uri = 'file:///home/user/über photo/X1%20Photographs'
        formated = '/home/user/über photo/X1 Photographs'

        self.assertNotEqual(file_uri_to_path(test_uri), test_uri)
        self.assertEqual(file_uri_to_path(test_uri), formated)
        self.assertEqual(file_uri_to_path(formated), formated)


class File:
    """File object class"""
    serial_delimeter = "_No"
    # compiled regular expressions
    reg_no_digits = re.compile("[\^\d]")
    reg_only_digits = re.compile("[^\d]")
    reg_no_parenthesis = re.compile("(\(.*\))")
    reg_onedigit = re.compile("(\d){1}")
    reg_serial = re.compile(serial_delimeter + "(\d+)")

    def __init__(self, root, file):
        """ root and file are strings.

            Root means whole path with file name.
            File means only filename without path
        """
        self.root = root
        self.file = file
        self.__cmp_str = False  # cache for comparable string
        self.mtsd = 14  # minimum time stamp digits

    def is_related(self, file_obj):
        """
        Test the relation to the given file object
        (try to compare the timstamp out of the filename). Return values
        are True and False.
        """
        cmpstr = self._get_cmpstr()

        if cmpstr == None:
            # logging.debug('val = False | cmpstr == None')
            return False

        elif file_obj._get_cmpstr() == cmpstr:
            if not self == file_obj:
                if not self.get_file_name() == file_obj.get_file_name():
                    if not self.get_sufix() == file_obj.get_sufix():
                        logging.debug('val = True | own cmpstr: %s other cmpstr: %s' %
                                     (cmpstr, file_obj._get_cmpstr()))
                        return True
            return False

        else:
            # logging.debug('val = False | own cmpstr: %s other cmpstr: %s' %
            #                  (cmpstr, file_obj._get_cmpstr()))
            return False

    def _get_cmpstr(self):
        """
        provides an file comparison string with only one parsing process
        per instance.
        """
        if self.__cmp_str:  # return from value from cache
            return self.__cmp_str

        elif self.__cmp_str == None:  # return from cache None
            return None

        elif self.__cmp_str == False:  # return from methode
            try:
                self.__cmp_str = self._calc_cmpstr()  # set cache value
                return self.__cmp_str

            except ValueError as e:
                logging.debug('ValueError: %s' % e)  # set cache to None
                self.__cmp_str = None
                return None

    def _calc_cmpstr(self):
        """returns a comparable string. The first digits defined in numbers by
            self.mtsd are used plus a serail number if available.
        """
        # liefert maximal die ersten 14 Zahlen
        digit_str = re.sub("[^\d]", "", self.file, 35)[:self.mtsd]
        if len(digit_str) < self.mtsd:  # Test for sufficent length
            raise ValueError(
                'from file: "%s" the comparison string is: %s which length is lower than %s' %
                             (self.file, digit_str, self.mtsd))

        # Entfernung der runden Klammern und deren inhalt
        file_no_parenthesis = re.sub(File.reg_no_parenthesis, "", self.file, 30)

        # Advanced parse
        if File.serial_delimeter in file_no_parenthesis:  # Test of serial processing
            # Complete and return string
            serial = self._get_serial(file_no_parenthesis)
            if serial:
                digit_str = digit_str + serial
        return digit_str

    def _get_serial(self, file_no_parenth):
        """ returns the appended serialnumber of an image if it
            exists, else none
        """
        # Berechnet den Index der letzen Zahl im Datum des Dateinamens
        end_index = 0
        for i in range(self.mtsd):
            s = File.reg_onedigit.search(file_no_parenth, end_index)
            if s:
                end_index = s.span()[1]

        # sucht nach der Seriennummer im Anschluss des Datums im Dateinamen
        serial = File.reg_serial.match(file_no_parenth, end_index)

        if not serial:
            return None
        return serial.group()[3:]

    def get_sufix(self):
        """ returns only the sufix without a point.
        """
        return self.file.split('.')[-1]

    def get_file_path(self):
        """ returns complete path with filename
        """
        return self.root

    def get_file_name(self):
        """ retuns the filename without path but with sufix
        """
        return self.file

    def remove(self):
        if test_trash_cli:
            os.system('trash-put "%s"' % self.get_file_path())
        else:
            message = 'Trash cli not found. Please use pip install trash-cli'
            logging.debug(message)
            raise SystemError(message)

    def get_root_path(self):
        """ returns path without file name
        """
        # return self.file
        return self.root.split(self.file)[0]

    def get_filename_no_sufix(self):
        """ retuns filename without sufix
        """
        return self.file.split('.%s' % self.get_sufix())[0]

    def get_custom_naming_string(self):
        """ returns the custom file naming string with emty spaces between
            words.
        """
        no_serial = re.sub(File.reg_serial, "", self.get_filename_no_sufix(), 30)
        logging.debug('filename without sufix is: %s' % self.get_filename_no_sufix())
        logging.debug('without serial: %s' % no_serial)

        nb = no_serial.split(')')
        if len(nb) > 1:
            no_brackets = ''
            for I in nb:
                nnb = '%s%s' % (I, ')')  # add lost bracket
                nnb = re.sub(File.reg_no_parenthesis, "", nnb, 30)
                no_brackets += nnb
            logging.debug('without brackets: %s' % no_brackets)
        else:
            no_brackets = no_serial
        no_brackets = no_brackets.strip(')')

        no_numbers = re.sub(File.reg_no_digits, "", no_brackets, 30)
        logging.debug('without numbers: %s' % no_numbers)

        text = no_numbers
        logging.debug('text after re: %s' % text)

        file_name = self.get_filename_no_sufix()
        logging.debug('filename without sufix: %s' % file_name)

        # replace seperators wit emty space
        for I in [':', '.', ',', ';', '-', '-', '#', '+', '_', '   ', '  ']:
            text = text.replace(I, ' ')
        file_name = file_name.replace('_', ' ')
        logging.debug('text: %s' % text)

        if text == ' ':
            return ''

        # strip expressions that are not related to filename
        text = text.strip(' ')
        excluded = ['LR-', '-LR', 'LR']
        for I in excluded:
            if I == text[:3]:
                text = text[3:]
            elif I == text[:2]:
                text = text[2:]
        text = text.strip(' ')  # text is for the first trigger expr.
        logging.debug('text: %s' % text)

        trigger = text.split(' ')[0]
        logging.debug('text is: %s and then the trigger is: %s' % (text, trigger))

        try:
            compare_text = file_name.strip(' ').split(trigger)
        except ValueError as e:
            logging.error('error with filename: %s: %s:' % (file_name, e))
            return ''

        logging.debug('compare text: %s' % compare_text)

        # build string from teh beginning of the trigger word
        ln = len(compare_text)
        name_str = ''
        if ln == 1:
            name_str = '%s %s' % (trigger, compare_text[0])
            logging.debug('namestring 1: %s' % name_str)

        elif ln > 1:
            compare_text.pop(0)
            for I in compare_text:
                name_str += trigger + I
                logging.debug('namestring 2: %s' % name_str)

        return name_str.replace('  ', ' ')

    def __repr__(self):
        return 'File object %s: %s' % (__name__, self.get_file_name())


class TestFile(unittest.TestCase):

    def setUp(self):
        LOGGING_MODE = 'DEBUG'

        self.f1 = File('/some/path/2006:06:06 15:14:33-some_text.jpg',
                       '2006:06:06 15:14:33-some_text.jpg')
        self.f2 = File('/some/path/2006:06:06 15:14:33-some_other_text.jpg',
                       '2006:06:06 15:14:33-some_other_text.jpg')
        self.f3 = File('/some/path/2006:06:06 15:14:33_No2_text_No1.jpg',
                       '2006:06:06 15:14:33_No2_text_No1.jpg')

        self.f4 = File('/some/path/2006:06:06 15:14:33-some_text.raw',
                       '2006:06:06 15:14:33-some_text.raw')
        self.f5 = File('/some/path/2006:06:06 15:14:33-some_other_new_text.dng',
                       '2006:06:06 15:14:33-some_other_text.dng')
        self.f6 = File('/some/path/2006:06:06 15:14:33_No2_text.dng',
                       '2006:06:06 15:14:33_No2_text.dng')
        self.f7 = File('/some/path/only_a_name.dng', 'only_a_name.dng')
        self.f8 = File('/some/path/only_a_name_No22.dng', 'only_a_name_No22.dng')

        self.f11 = File('/some/path/2006:06:06 15:14:33_66_street_some_text.jpg',
                       '2006:06:06 15:14:33_66_street_some_text.jpg')

        self.f12 = File('/some/path/2006:06:06 15:14:33(X1-12)_street_(expl.)_text.jpg',
                       '2006:06:06 15:14:33(X1-12)_street_(expl.)_text.jpg')

        self.f20 = File('/a/path/2015-02-18--17.52.42(M9K)-LR-2_China_Hongkong.jpg',
                  '2015-02-18--17.52.42(M9K)-LR-2_China_Hongkong.jpg')

    def test_is_related(self):
        self.assertTrue(self.f1.is_related(self.f5))
        self.assertFalse(self.f1.is_related(self.f3))
        self.assertFalse(self.f2.is_related(self.f6))
        self.assertTrue(self.f2.is_related(self.f5))
        self.assertTrue(self.f3.is_related(self.f6))
        self.assertFalse(self.f7.is_related(self.f1))

        self.assertFalse(self.f7.is_related(self.f7))
        self.assertFalse(self.f1.is_related(self.f1))

        f7 = File('/a/path/2015-02-18--17.52.42(M9K)-LR-2_China_Hongkong.jpg',
          '2015-02-18--17.52.42(M9K)-LR-2_China_Hongkong.jpg')

        f72 = File('/raw/2015-02-18--17.52.42(M9-K).dng',
                   '2015-02-18--17.52.42(M9-K).dng')

        f8 = File('/a/path/2015-02-18--17.22.24(M9K)-LR_China_Hongkong.jpg',
          '2015-02-18--17.22.24(M9K)-LR_China_Hongkong.jpg')

        f82 = File('/raw/2015-02-18--17.22.24(M9K).dng',
                   '2015-02-18--17.22.24(M9K).dng')

        f9 = File('/a/path/2015-05-01--15.08.02(M9-)_Australien_SA_Redhill-LR.jpg',
          '2015-05-01--15.08.02(M9-)_Australien_SA_Redhill-LR.jpg')

        f92 = File('/raw/2015-05-01--15.08.02(M9-).dng',
                   '2015-05-01--15.08.02(M9-).dng')

        self.assertTrue(f7.is_related(f72))
        self.assertTrue(f8.is_related(f82))
        self.assertTrue(f9.is_related(f92))

        self.assertTrue(f72.is_related(f7))
        self.assertTrue(f82.is_related(f8))
        self.assertTrue(f92.is_related(f9))

    def test__get_compstr(self):
        f7 = File('/some/path/7_689.-65.9-9#45.jpg',
                       '7_689.-65.9-9#45.jpg')
        self.assertEqual(f7._get_cmpstr(), None)  # value from methode
        self.assertEqual(f7._get_cmpstr(), None)  # 2nd run: value from cache

        f8 = File('/some/path/7_689..89.-65.9-9#4785.jpg',
                       '7_689..89.-65.9-9#4785.jpg')
        self.assertEqual(f8._get_cmpstr(), '76898965994785')

        f9 = File('/some/path/7_689..89.-65.9-9#4785_No55.jpg',
                       '7_689..89.-65.9-9#4785_No55.jpg')
        self.assertEqual(f9._get_cmpstr(), '7689896599478555')

        self.assertEqual(self.f7._get_cmpstr(), None)

    def test__calc_compstr(self):
        f7 = File('/some/path/7_689.-65.9-9#45.jpg',
                       '7_689.-65.9-9#45.jpg')

        with self.assertRaises(ValueError):
            f7._calc_cmpstr()
            self.f7._calc_cmpstr()
            self.f8._calc_cmpstr()

        f8 = File('/some/path/7_689..89.-65.9-9#4785.jpg',
                       '7_689..89.-65.9-9#4785.jpg')
        self.assertEqual(f8._calc_cmpstr(), '76898965994785')

        f9 = File('/some/path/7_689..89.-65.9-9#4785_No55.jpg',
                       '7_689..89.-65.9-9#4785_No55.jpg')
        self.assertEqual(f9._calc_cmpstr(), '7689896599478555')

    def test__get_serial(self):
        self.assertEqual('2', self.f6._get_serial(self.f6.get_file_name()))

        f9 = File('/some/path/7_689..89.-65.9-9#4785_No55.jpg',
                       '7_689..89.-65.9-9#4785_No55.jpg')
        self.assertEqual('55', f9._get_serial(f9.get_file_name()))

        self.assertEqual(None, self.f1._get_serial(self.f1.get_file_name()))
        self.assertEqual(None, self.f8._get_serial(self.f8.get_file_name()))

    def test_get_sufix(self):
        self.assertEqual(self.f1.get_sufix(), 'jpg')
        self.assertEqual(self.f3.get_sufix(), 'jpg')
        self.assertEqual(self.f4.get_sufix(), 'raw')
        self.assertEqual(self.f6.get_sufix(), 'dng')
        self.assertEqual(self.f8.get_sufix(), 'dng')
        self.assertEqual(self.f20.get_sufix(), 'jpg')

    def test_get_file_path(self):
        self.assertEqual(self.f1.get_file_path(),
                         '/some/path/2006:06:06 15:14:33-some_text.jpg')
        self.assertEqual(self.f3.get_file_path(),
                         '/some/path/2006:06:06 15:14:33_No2_text_No1.jpg')
        self.assertEqual(self.f8.get_file_path(),
                         '/some/path/only_a_name_No22.dng')

    def test_get_file_name(self):
        self.assertEqual(self.f1.get_file_name(),
                         '2006:06:06 15:14:33-some_text.jpg')
        self.assertEqual(self.f2.get_file_name(),
                         '2006:06:06 15:14:33-some_other_text.jpg')
        self.assertEqual(self.f3.get_file_name(),
                         '2006:06:06 15:14:33_No2_text_No1.jpg')
        self.assertEqual(self.f8.get_file_name(),
                         'only_a_name_No22.dng')

    def test__remove(self):
        file_dir = '%s/files/' % os.path.dirname(__file__)
        test_file = '%s/files/test/pictures/2016:07:22--14.20.10.dng' \
                                                % os.path.dirname(__file__)
        new_file_path = '%s/new_file.dng' % file_dir
        shutil.copy(test_file, new_file_path)
        new_file_objekt = File(new_file_path, 'new_file.dng')

        # TODO | bug in python or eclipse - check next time again
        # new_file_objekt.remove()
        # self.assertFalse(os.path.isfile(new_file_path))

    def test_get_root_path(self):
        self.assertEqual(self.f1.get_root_path(), '/some/path/')
        self.assertEqual(self.f11.get_root_path(), '/some/path/')
        self.assertEqual(self.f12.get_root_path(), '/some/path/')

    def test_get_filename_no_sufix(self):
        self.assertEqual(self.f2.get_filename_no_sufix(),
                         '2006:06:06 15:14:33-some_other_text')
        self.assertEqual(self.f11.get_filename_no_sufix(),
                         '2006:06:06 15:14:33_66_street_some_text')
        self.assertEqual(self.f12.get_filename_no_sufix(),
                         '2006:06:06 15:14:33(X1-12)_street_(expl.)_text')
        self.assertEqual(self.f20.get_filename_no_sufix(),
                         '2015-02-18--17.52.42(M9K)-LR-2_China_Hongkong')

    def test_get_custom_naming_string(self):

        self.assertEqual(self.f2.get_custom_naming_string(),
                        'some other text')

        self.assertEqual(self.f3.get_custom_naming_string(),
                       'text No1')

        self.assertNotEqual(self.f11.get_custom_naming_string(),
                        '66 street some text')

        self.assertEqual(self.f11.get_custom_naming_string(),
                        'street some text')

        self.assertEqual(self.f12.get_custom_naming_string(),
                        'street (expl.) text')

        f5 = File('/a/path/2016-05-07--18.19.40(X1)_Schwarzwald.jpg',
                  '2016-05-07--18.19.40(X1)_Schwarzwald.jpg')

        f6 = File('/a/path/raw/2016-05-07--18.19.40(X1).dng',
                  '2016-05-07--18.19.40(X1).dng')

        self.assertEqual(f5.get_custom_naming_string(),
                         'Schwarzwald')

        self.assertEqual(f6.get_custom_naming_string(),
                         '')

        f0 = File(
            '/some/path/2006:06:06 15:14:33(X1-12)_No3_a_street_33_(expl.)_a_text_(good one)_a_place.jpg',
            '2006:06:06 15:14:33(X1-12)_No3_a_street_33_(expl.)_a_text_(good one)_a_place.jpg')
        self.assertEqual(f0.get_custom_naming_string(),
                        'a street 33 (expl.) a text (good one) a place')

        f7 = File('/a/path/2015-02-18--17.52.42(M9K)-LR-2_China_Hongkong_Blumenmarkt.jpg',
          '2015-02-18--17.52.42(M9K)-LR-2_China_Hongkong_Blumenmarkt.jpg')
        self.assertEqual(f7.get_custom_naming_string(),
                         'China Hongkong Blumenmarkt')

        f8 = File('/a/path/2015-02-18--17.22.24(M9K)-LR_China_Hongkong_Blumenmarkt.jpg',
          '2015-02-18--17.22.24(M9K)-LR_China_Hongkong_Blumenmarkt.jpg')
        self.assertEqual(f8.get_custom_naming_string(),
                         'China Hongkong Blumenmarkt')

        f9 = File('/a/path/2015-05-01--15.08.02(M9-)_Australien_SA_Redhill-LR.jpg',
          '2015-05-01--15.08.02(M9-)_Australien_SA_Redhill-LR.jpg')
        self.assertEqual(f9.get_custom_naming_string(),
                         'Australien SA Redhill-LR')


class Process:
    """ Process Files for renaming
    """
    def __init__(self, current_path, files, paths):
        self.TEST_MODE = False
        self.main_path = os.path.normpath(current_path)
        self.selected_files = files
        self.selected_path = paths

        # get file objects
        self.selected_file_objects = []
        self.surrounded_file_objects = []
        self._generate_file_objects()

    def start_ui(self):
        proc = subprocess.run("zenity --entry --title='photo file namer' \
                --text='name selected!'", shell=True, stdout=subprocess.PIPE)
        val = proc.stdout
        txt = val.decode("utf-8")  # Decode the bytes into a useful string
        # format string
        logging.debug('got form zenety: %s' % txt)
        txt = txt.replace('   ', ' ').replace('\n', '').replace('  ', ' ')

        if txt == '***':
            logging.debug('perform name oposites')
            self._name_oposites(self._get_file_pairs())
        else:
            logging.debug('perform name files')
            self._name_files(self._get_file_pairs(), txt)

    def _name_oposites(self, file_pairs):
        """ name only oposite files which the same string as the
            selected files already named
        """
        test = {}
        pairs = file_pairs[0]

        for pair in pairs:
            go = False
            if pair[0] in self.selected_file_objects:
                master_file = pair[0]
                follower_file = pair[1]
                go = True
                logging.debug('1. master: %s follower: %s' %
                              (master_file, follower_file))
            elif pair[1] in self.selected_file_objects:
                master_file = pair[1]
                follower_file = pair[0]
                go = True
                logging.debug('2. master: %s follower: %s' %
                              (master_file, follower_file))

            if go:
                mpf = follower_file.get_filename_no_sufix()

                spliter = follower_file.get_custom_naming_string()
                spliter = spliter.replace(' ', '_').strip('_')
                logging.debug('splitter is: %s' % spliter)

                try:
                    manipulated_filename = mpf.split(spliter)[0]
                except ValueError:
                    manipulated_filename = mpf
                manipulated_filename = manipulated_filename.strip('_')

                if not master_file.get_custom_naming_string():
                    dash = ''
                else:
                    dash = '_'

                logging.debug('manipulated filename: %s' % manipulated_filename)

                old = follower_file.get_file_path()
                new = '%s%s%s.%s' % \
                (
                 manipulated_filename,
                 dash,
                 master_file.get_custom_naming_string(),
                 follower_file.get_sufix()
                 )
                new = new.replace(' ', '_')
                new = '%s%s' % (follower_file.get_root_path(), new)

                # rename file
                logging.debug('old file: %s | new file %s' % (old, new))
                if self.TEST_MODE:
                    test.update({old: new})
                else:
                    self._rename_files(old, new)

        if self.TEST_MODE:
            return test

    def _name_files(self, file_pairs, txt):
        """ it names all files which are selected and also its oponents
        """
        txt = txt.replace(' ', '_'
                                                                )
        test = {}
        logging.debug('formated text: %s' % txt)

        # make list form file_pairs and selected
        L = []
        for pair in file_pairs[0]:  # from file_pairs
            for I in pair:
                L.append(I)

        for sel in file_pairs[1]:  # from lonly selected
            L.append(sel)

        # name files
        if txt:
            txt = '_%s' % txt

            # rename files
            for I in L:
                old = I.get_file_path()
                new = '%s%s.%s' % (old.split('.%s' % I.get_sufix())[0],
                                   txt, I.get_sufix())
                # self._rename_files(old, new)

                if self.TEST_MODE:
                    test.update({old: new})
                else:
                    self._rename_files(old, new)

        if self.TEST_MODE:
            return test

    def _rename_files(self, old, new):
        """ rename files from old to new. Old and new must be strings.
        """
        if LOGGING_MODE == 'INFO' or self.TEST_MODE == True:
            try:
                shutil.copy(old, new)
                os.remove(old)
            except:
                logging.error("Unexpected error: %s", sys.exc_info()[0])
        else:
            logging.debug('shutil.copy(%s, %s)' % (old, new))
            logging.debug('os.remove(%s)' % old)


    def _get_file_pairs(self):
        """ retuns a tuple with a list of file pairs and a list of
            the lonly ones: ([[fX, fY],[fZ, fU]], [o1, o2, o3])
        """
        L = []  # list of related pairs in in twin groups
        X = []  # list of all related files form selected and surrounded (not as pairs)
        Y = []  # list of selected files with no relation to others

        # relateion from selected to the sourounded files
        for obj1 in self.selected_file_objects:
            for obj2 in self.surrounded_file_objects:
                if obj1.is_related(obj2) and obj2 not in self.selected_file_objects:
                    L.append([obj1, obj2])
                    X.append(obj1)
                    X.append(obj2)

        for I in self.selected_file_objects:
            if I not in Y and I not in X:
                logging.debug('selected file: %s must not be in: %s' % (I, X))
                Y.append(I)  # selected files without pairs


        logging.debug('Will return this file pattern: (%s, %s)' % (L, Y))
        return L, Y

    def _generate_file_objects(self):
        self.surrounded_file_objects = self._get_surrounded()
        sf = self.selected_files
        sp = self.selected_path

        for path in sp:
            for file in sf:
                if file in path:
                    self.selected_file_objects.append(File(path, file))

        logging.debug('list of objects of selected files: %s' %
                      self.selected_file_objects)
        logging.debug('list of objects of surrounded files: %s' %
                      self.surrounded_file_objects)

    def _get_surrounded(self):
        """ beginn to crawl 2 levels above for getting files which are not
            selected. Retuns a dictionary with {path: name, ... }
        """
        dirname = os.path.dirname(self.main_path)
        logging.debug('first dirname value: %s' % dirname)
        next = os.path.dirname(dirname)  # start two dirs up
        logging.debug('second dirname value: %s' % next)
        # Skip levels with amount of folders greater this number. All for good speed.
        folder_search_limit = 15

        if dirname == os.environ['HOME']:
            start = self.main_path
        else:
            start = dirname  # start one dir upwards
            trigger = ['pictures', 'Bilder', 'Fotos', 'Grafik', 'grapics', 'pic',
                       'pics', 'graphic', 'photographs']
            for I in trigger:
                if I.lower() in next.lower():
                    start = next

        logging.debug('start point of traverse search % s' % start)
        all_found_dirs = []


        # getting alls files under start_path
        collected_files = []

        for root, dirs, files in os.walk(start):
            for file in files:
                file = File('%s/%s' % (root, file), file)
                collected_files.append(file)

        logging.debug('All collected files: %s' % collected_files)
        return collected_files


class TestProcess(unittest.TestCase):
    def setUp(self):
        dirname = os.path.dirname
        p = dirname(__file__)

        self.current_path = '%s/files/test/pictures/2/current path/' % p
        logging.debug('current_path is %s' % self.current_path)

        files = [f for f in os.listdir(self.current_path) if
                 os.path.isfile(self.current_path + f)]
        self.f = files
        logging.debug('files are %s' % files)

        paths = [self.current_path + f for f in os.listdir(self.current_path)
                 if os.path.isfile(self.current_path + f)]
        logging.debug('files paths are %s' % paths)

        self.p = Process(self.current_path, files, paths)
        self.p.TEST_MODE = True

    def test_generate_file_objects(self):
        self.assertEqual(len(self.p.selected_file_objects), 7)
        self.assertEqual(len(self.p.surrounded_file_objects), 13)

    def test_get_surrounded(self):
        surr = self.p._get_surrounded()
        res = []
        for I in surr:
            res.append(I.get_file_name())


        self.assertEqual(type(res), list)
        self.assertEqual(len(res), 13)
        self.assertTrue('2016:07:24--11.47.01_London.nef' in res)
        self.assertTrue('2016:07:24--15.10.22_Paris.tiff' in res)
        self.assertTrue('2016:07:22--14.20.10.dng' in res)
        self.assertTrue('2016:07:22--14.20.11_Roma.raw' in res)

        self.assertTrue('2002:09:17--08.20.44_some_text.fff' in res)

    def test__get_file_pairs(self):
        pairs = self.p._get_file_pairs()
        l = []

        for pair in pairs[0]:
            p = []
            for I in pair:
                p.append(I.get_file_name())
            l.append(p)

        self.assertTrue(
            ['2016:07:22--14.20.11_Roma.jpg',
             '2016:07:22--14.20.11_Roma.raw'] in l)

        self.assertTrue(
            ['2016:07:22--14.20.10.jpg',
             '2016:07:22--14.20.10.dng'] in l)

        self.assertTrue(
            ['2016:07:24--11.47.01_London.jpg',
             '2016:07:24--11.47.01_London.nef'] in l)

        self.assertTrue(
            ['2016:07:24--15.10.22_Paris.jpg',
             '2016:07:24--15.10.22_Paris.tiff'] in l)

        self.assertTrue(
            ['2002:09:17--08.20.44_some other text.jpg',
             '2002:09:17--08.20.44_some_text.fff'] in l)

        self.assertFalse(
            ['2013-04-11--14:22:10_I_am_a_lonly_file.jpg',
             '2013-04-11--14:22:10_I_am_a_lonly_file.jpg'] in l)

        sel = []
        for I in pairs[1]:
            sel.append(I.get_file_name())
        # print(pairs[1])

        self.assertFalse('2013-04-11--14:22:10_I_am_a_lonly_file.jpg' in l)
        self.assertTrue('2013-04-11--14:22:10_I_am_a_lonly_file.jpg' in sel)
        self.assertEqual(len(sel), 1, 'selected is: %s' % sel)

    def test_name_oposites(self):
        f1 = File('/a first/path/2013-04-11--14:22:10_I_am_a_lonly_file.jpg',
                  '2013-04-11--14:22:10_I_am_a_lonly_file.jpg')

        f2 = File('/a first/path/dng/2013-04-11--14:22:10.dng',
                  '2013-04-11--14:22:10.dng')

        f3 = File('/a first/path/2013-05-11--14:22:10_an_other_file.jpg',
                  '2013-05-11--14:22:10_an_other_file.jpg')

        f4 = File('/an/other/path/2013-05-11--14:22:10_something_meaningful.raw',
                  '2013-05-11--14:22:10_something_meaningful.raw')

        f5 = File('/a/path/2016-05-07--18.19.40(X1)_Schwarzwald.jpg',
                  '2016-05-07--18.19.40(X1)_Schwarzwald.jpg')

        f6 = File('/a/path/raw/2016-05-07--18.19.40(X1).dng',
                  '2016-05-07--18.19.40(X1).dng')

        f7 = File('/a/path/2015-02-18--17.52.42(M9K)-LR-2_China_Hongkong.jpg',
          '2015-02-18--17.52.42(M9K)-LR-2_China_Hongkong.jpg')

        f72 = File('/raw/2015-02-18--17.52.42(M9-K).dng',
                   '2015-02-18--17.52.42(M9-K).dng')

        f8 = File('/a/path/2015-02-18--17.22.24(M9K)-LR_China_Hongkong.jpg',
          '2015-02-18--17.22.24(M9K)-LR_China_Hongkong.jpg')

        f82 = File('/raw/2015-02-18--17.22.24(M9K).dng',
                   '2015-02-18--17.22.24(M9K).dng')

        f9 = File('/a/path/2015-05-01--15.08.02(M9-)_Australien_SA_Redhill-LR.jpg',
          '2015-05-01--15.08.02(M9-)_Australien_SA_Redhill-LR.jpg')

        f92 = File('/raw/2015-05-01--15.08.02(M9-).dng',
                   '2015-05-01--15.08.02(M9-).dng')

        f100 = File('/a/path/2010-06-28--11.22.22(Summilux).jpg',
                    '2010-06-28--11.22.22(Summilux).jpg')

        f101 = File('/a/path/raw/2010-06-28--11.22.22(X).dng',
                    '2010-06-28--11.22.22(X).dng')

        files = ['2015-02-18--17.52.42(M9K)-LR-2_China_Hongkong.jpg',
                 '2015-02-18--17.22.24(M9K)-LR_China_Hongkong.jpg',
                 '2015-05-01--15.08.02(M9-)_Australien_SA_Redhill-LR.jpg',
                 '2013-04-11--14:22:10_I_am_a_lonly_file.jpg',
                 '2013-05-11--14:22:10_an_other_file.jpg',
                 '2016-05-07--18.19.40(X1)_Schwarzwald.jpg',
                 '2010-06-28--11.22.22(Summilux).jpg',
                 ]

        paths = ['/a/path/2015-02-18--17.52.42(M9K)-LR-2_China_Hongkong.jpg',
                 'a/path/2015-02-18--17.22.24(M9K)-LR_China_Hongkong_Blumenmarkt.jpg',
                 '/a/path/2015-05-01--15.08.02(M9-)_Australien_SA_Redhill-LR.jpg',
                 '/a first/path/2013-04-11--14:22:10_I_am_a_lonly_file.jpg',
                 '/a first/path/2013-05-11--14:22:10_an_other_file.jpg',
                 '/a/path/2016-05-07--18.19.40(X1)_Schwarzwald.jpg',
                 '/a/path/2010-06-28--11.22.22(Summilux).jpg',
                 ]

        self.p.selected_files = files
        self.p.selected_path = paths
        self.p.selected_file_objects = [f1, f3, f5, f7, f8, f9, f100]
        val = self.p._name_oposites(([[f1, f2], [f3, f4], [f5, f6], [f7, f72],
                                      [f8, f82], [f9, f92], [f100, f101]], []))

        newf = val['/a first/path/dng/2013-04-11--14:22:10.dng']
        self.assertEqual(newf,
                        '/a first/path/dng/2013-04-11--14:22:10_I_am_a_lonly_file.dng')

        newf = val['/an/other/path/2013-05-11--14:22:10_something_meaningful.raw']
        self.assertEqual(newf,
                        '/an/other/path/2013-05-11--14:22:10_an_other_file.raw')

        newf = val['/a/path/raw/2016-05-07--18.19.40(X1).dng']
        self.assertEqual(newf,
                        '/a/path/raw/2016-05-07--18.19.40(X1)_Schwarzwald.dng')

        newf = val['/raw/2015-02-18--17.52.42(M9-K).dng']
        self.assertEqual(newf,
                        '/raw/2015-02-18--17.52.42(M9-K)_China_Hongkong.dng')

        newf = val['/raw/2015-02-18--17.22.24(M9K).dng']
        self.assertEqual(newf,
                        '/raw/2015-02-18--17.22.24(M9K)_China_Hongkong.dng')

        newf = val['/raw/2015-05-01--15.08.02(M9-).dng']
        self.assertEqual(newf,
                        '/raw/2015-05-01--15.08.02(M9-)_Australien_SA_Redhill-LR.dng')

        newf = val['/a/path/raw/2010-06-28--11.22.22(X).dng']
        self.assertEqual(newf,
                        '/a/path/raw/2010-06-28--11.22.22(X).dng')

    def test_name_files(self):

        file1 = '/a first/path/2016:07:22--14.20.11_Roma.jpg'
        file4 = '/a second/path/2016:07:22--14.20.11_Roma.raw'
        file2 = '/a/third/path/2016:07:24--11.47.01_London.jpg'
        file3 = '/a/path/2016:07:24--11.47.01_London.nef'
        file5 = '/a/path/2011:03:23--11.47.01_some_meaning.dng'
        # file6 = '/a/path/2016:07:22--14.20.11_Roma.jpg'

        f1 = File(file1, '2016:07:22--14.20.11_Roma.jpg')
        f4 = File(file4, '2016:07:22--14.20.11_Roma.raw')
        f2 = File(file2, '2016:07:24--11.47.01_London.jpg')
        f3 = File(file3, '/a/path/2016:07:24--11.47.01_London.nef')
        f5 = File(file5, '2011:03:23--11.47.01_some_meaning.dng')

        pairs = ([[f1, f4], [f2, f3]], [f5])
        named = self.p._name_files(pairs, 'this is a (example: bla) text')

        # test case
        new = '/a first/path/2016:07:22--14.20.11_Roma_this_is_a_(example:_bla)_text.jpg'
        self.assertEqual(named[f1.get_file_path()], new)

        new = '/a second/path/2016:07:22--14.20.11_Roma_this_is_a_(example:_bla)_text.raw'
        self.assertEqual(named[f4.get_file_path()], new)

        new = '/a/third/path/2016:07:24--11.47.01_London_this_is_a_(example:_bla)_text.jpg'
        self.assertEqual(named[f2.get_file_path()], new)

        new = '/a/path/2016:07:24--11.47.01_London_this_is_a_(example:_bla)_text.nef'
        self.assertEqual(named[f3.get_file_path()], new)

        new = '/a/path/2011:03:23--11.47.01_some_meaning_this_is_a_(example:_bla)_text.dng'
        self.assertEqual(named[f5.get_file_path()], new)


if __name__ == '__main__':
    process = Process(nautilus_current_path, nautilus_files, nautilus_paths)
    process.start_ui()
