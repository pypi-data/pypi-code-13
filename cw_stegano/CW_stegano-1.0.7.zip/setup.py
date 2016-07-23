from setuptools import setup
import pip, sys
files = ["steganography"]
setup(
  name = 'CW_stegano',
  packages = files,
  version = '1.0.7',
  description = 'A fun little python script that encodes and decodes strings and images\nPatch #2:\nthere were some errors with the v1.0.5, this patch should fix those errors.',
  author = 'Calder White',
  author_email = 'calderwhite1@gmail.com',
  url = 'https://github.com/CalderWhite/steganography',
  keywords = [],
  classifiers = []
)
# test dependancies now
depend = {
    "PIL" : "Pillow"
    }
for i in depend:
    try:
        __import__(i)
    except:
        print("Missing module [%s]. Attempting to install %s" % (i,depend[i]))
        try:
            pip.main(["install",depend[i]])
            print("Successfully installed %s" % (depend[i]))
        except:
            print("an error occured:")
            print(sys.exc_info())
