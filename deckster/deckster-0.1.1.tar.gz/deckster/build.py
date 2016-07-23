#!/usr/local/bin/python
# encoding: utf-8
"""
*Build the Reveal.js presentation into the specifed build directory*

:Author:
    David Young

:Date Created:
    May 28, 2016
"""
################# GLOBAL IMPORTS ####################
import sys
import os
import shutil
import re
import markdown as md
import codecs
os.environ['TERM'] = 'vt100'
from fundamentals import tools


class build():
    """
    *The worker class for the build module*

    **Key Arguments:**
        - ``log`` -- logger
        - ``sourceDir`` -- path the the source directory containing everything we need to build the presentation. Default *./source*
        - ``buildDir`` -- path to the folder to build our presentation into. Default *./build*
        - ``settings`` -- the settings dictionary
        - ``copyAssets`` -- copp assets found in the includes.txt file at the root of the source directory into the build directory. Default *True*

    **Usage:**
        .. todo::

            - add usage info
            - create a sublime snippet for usage

        .. code-block:: python 

            usage code   

    .. todo::

        - @review: when complete, clean build class
        - @review: when complete add logging
        - @review: when complete, decide whether to abstract class to another module
    """
    # Initialisation
    # 1. @flagged: what are the unique attrributes for each object? Add them
    # to __init__

    def __init__(
            self,
            log,
            sourceDir="./source",
            buildDir="./build",
            settings=False,
            copyAssets=True
    ):
        self.log = log
        log.debug("instansiating a new 'build' object")
        self.settings = settings
        self.sourceDir = sourceDir
        self.buildDir = buildDir
        self.copyAssets = copyAssets

        # xt-self-arg-tmpx

        # Variable Data Atrributes
        # TRANSITION TYPES
        self.transitions = ["none", "fade",
                            "slide", "convex", "concave", "zoom"]

        # 3. @flagged: what variable attrributes need overriden in any baseclass(es) used
        # Override Variable Data Atrributes

        # Initial Actions
        # CREATE THE BUILD DIRECTORY IF IT DOESN'T EXIST
        # Recursively create missing directories
        shutil.rmtree(buildDir)
        if not os.path.exists(buildDir):
            os.makedirs(buildDir)

        if self.copyAssets:
            self.copy_assets()

        return None

    # 4. @flagged: what actions does each object have to be able to perform? Add them here
    # Method Attributes
    def build(self):
        """
        *get the build object*

        **Return:**
            - ``build``

        .. todo::

            - @review: when complete, clean get method
            - @review: when complete add logging
        """
        self.log.info('starting the ``build`` method')

        content = self.get_deck_content()

        index = self.buildDir + "/index.html"
        print index
        writeFile = codecs.open(index, encoding='utf-8', mode='w')
        writeFile.write(content)
        writeFile.close()

        self.log.info('completed the ``build`` method')
        return build

    def copy_assets(
            self):
        """*Copy the assets from the source directory into the build directory*

        The includes.txt file is read from the root of the source directory and anything added here is copied across to the build

        **Key Arguments:**
            # -

        **Return:**
            - None

        **Usage:**
            ..  todo::

                add usage info
                create a sublime snippet for usage

            .. code-block:: python 

                usage code 

        .. todo::

            - @review: when complete, clean methodName method
            - @review: when complete add logging
        """
        self.log.info('starting the ``copy_assets`` method')

        pathToReadFile = self.sourceDir + "/includes.txt"
        try:
            self.log.debug("attempting to open the file %s" %
                           (pathToReadFile,))
            readFile = codecs.open(pathToReadFile, encoding='utf-8', mode='r')
            thisData = readFile.read()
            readFile.close()
        except IOError, e:
            message = 'could not open the file %s' % (pathToReadFile,)
            self.log.critical(message)
            raise IOError(message)

        assets = thisData.strip().split("\n")
        # SORT ASSETS SO THERE ARE NO ISSUES WITH OVERWRITING
        assets.sort()

        for a in assets:
            basename = os.path.basename(a)
            dirOfFile = (self.buildDir + "/" + a).replace(basename, "")
            if basename == "*":
                fullDir = (self.sourceDir + "/" + a).replace(basename, "")
                try:
                    fullDir = (self.sourceDir + "/" + a).replace(basename, "")
                except Exception, e:
                    self.log.warning(
                        'the requested include folder %(a)s does not exist. %(e)s' % locals())
                shutil.copytree(fullDir, dirOfFile)
                continue
            # Recursively create missing directories
            print dirOfFile
            if not os.path.exists(dirOfFile):
                os.makedirs(dirOfFile)
            try:
                shutil.copyfile(self.sourceDir + "/" + a,
                                self.buildDir + "/" + a)
            except Exception, e:
                self.log.warning(
                    'the requested include file %(a)s does not exist' % locals())

        readFile.close()

        self.log.info('completed the ``copy_assets`` method')
        return None

    # use the tab-trigger below for new method
    def parse_markdown(
        self,
        slideFile="slide-deck.md"
    ):
        """*Read the multimardkown file and return the metadata in the yaml header alongside the parsed markdown content as HTML*

        **Key Arguments:**
            - ``slideFile`` -- the path to the slide deck markdown file. Default *slide-deck.md*.

        **Return:**
            - ``htmlContent`` -- parsed marddown to HTML content 
            - ``metadata`` -- metadata dictionary found in the header of the markdown file

        **Usage:**
            ..  todo::

                add usage info
                create a sublime snippet for usage

            .. code-block:: python 

                usage code 

        .. todo::

            - @review: when complete, clean methodName method
            - @review: when complete add logging
        """
        self.log.info('starting the ``parse_markdown`` method')

        # IMPORT CONTENTS OF THE MARKDOWN FILE
        slideFile = self.sourceDir + "/" + slideFile
        pathToReadFile = slideFile
        try:
            self.log.debug("attempting to open the file %s" %
                           (pathToReadFile,))
            readFile = codecs.open(pathToReadFile, encoding='utf-8', mode='r')
            thisData = readFile.read()
            readFile.close()
        except IOError, e:
            message = 'could not open the file %s' % (pathToReadFile,)
            self.log.critical(message)
            raise IOError(message)
        readFile.close()

        # FIX MMD SYNTAX FOR IMAGE SO PYTHON MARKDOWN PARSES CORRECTLY
        regex = re.compile(
            r'(?P<image>\[.*?\]\:.*?)(?P<dim>width|height)=(?P<size>.*?(px|%))', re.S)
        thisData = regex.sub("""\g<image> "" style="\g<dim>:\g<size>" """,
                             thisData)

        # CONVERT TO HTML
        parser = md.Markdown(
            extensions=['toc', 'meta', 'extra',  'footnotes'])
        htmlContent = parser.convert(thisData)

        # CORRECT ANY PARSING ISSUES
        regex = re.compile(
            r'(&quot;\s+?style=&quot;)', re.S)
        htmlContent = regex.sub("""\" style=\"""",
                                htmlContent)

        # GET META
        metadata = parser.Meta

        # REMOVE COMMENTS FROM METADATA VALUES
        for k, v in metadata.iteritems():
            metadata[k] = v[0].split(" //")[0].strip()

        self.log.info('completed the ``parse_markdown`` method')
        return htmlContent, metadata

    # use the tab-trigger below for new method
    def _get_html_head(
            self,
            metadata):
        """* get html head*

        **Key Arguments:**
            - ``metadata`` -- metadata dictionary parsed form markdown file yaml header.
            -

        **Return:**
            - None

        **Usage:**
            ..  todo::

                add usage info
                create a sublime snippet for usage

            .. code-block:: python 

                usage code 

        .. todo::

            - @review: when complete, clean methodName method
            - @review: when complete add logging
        """
        self.log.info('starting the ``_get_html_head`` method')

        # DEFAULTS
        title = "no title"
        description = "no description"
        author = "no author"
        theme = "white"
        highlighter = "zenburn"

        # UNPACK DICTIONARY VALUES TO LOCAL()
        for arg, val in metadata.iteritems():
            varname = arg
            if isinstance(val, str) or isinstance(val, unicode):
                exec(varname + ' = """%s""" ' % (val,))
            else:
                exec(varname + " = %s" % (val,))
            self.log.debug('%s = %s' % (varname, val,))

        head = u"""<head>
    <meta charset="utf-8">

    <title>%(title)s</title>

    <meta name="description" content="%(description)s">
    <meta name="author" content="%(author)s">

    <meta name="apple-mobile-web-app-capable" content="yes" />
    <meta name="apple-mobile-web-app-status-bar-style" content="black-translucent" />

    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no, minimal-ui">

    <link rel="stylesheet" href="css/reveal.css">
    <link rel="stylesheet" href="css/theme/%(theme)s.css" id="theme">
    

    <!-- Code syntax highlighting -->
    <link rel="stylesheet" href="css/highlight/%(highlighter)s.css" id="highlight-theme">

    <!-- Printing and PDF exports -->
    <script>
      var link = document.createElement( 'link' );
      link.rel = 'stylesheet';
      link.type = 'text/css';
      link.href = window.location.search.match( /print-pdf/gi ) ? 'css/print/pdf.css' : 'css/print/paper.css';
      document.getElementsByTagName( 'head' )[0].appendChild( link );
    </script>

    <!--[if lt IE 9]>
        <script src="lib/js/html5shiv.js"></script>
    <![endif]-->

    <link rel="stylesheet" href="css/custom.css">

  </head>
  """ % locals()

        self.log.info('completed the ``_get_html_head`` method')
        return head

    # use the tab-trigger below for new method
    def _get_slides(
            self,
            htmlContent):
        """* get slides*

        **Key Arguments:**
            - ``htmlContent`` -- the HTML content returned from parsing the markdown file.

        **Return:**
            - None

        **Usage:**
            ..  todo::

                add usage info
                create a sublime snippet for usage

            .. code-block:: python 

                usage code 

        .. todo::

            - @review: when complete, clean methodName method
            - @review: when complete add logging
        """
        self.log.info('starting the ``_get_slides`` method')

        # CONVERT NOTES TO REVEAL.JS NOTES
        htmlContent = self._convert_notes(htmlContent)

        # CREATE SLIDE ARRAY
        slidesArray = htmlContent.split("<hr />")

        slides = []
        slides[:] = [self._add_slide_attributes(s) for s in slidesArray]

        slides = ("\n\n").join(slides)

        # # ADD ELEMENT ATTRIBUTES
        # regex = re.compile(
        #     r'<((?P=ele)).*?)>(?P<con>(?:((?P=ele)>).)*?)f:(?P<attributes>.*?)</(?P<ele>\w+)>', re.S | re.I)
        # thisIter = regex.finditer(slides)
        # for item in thisIter:
        #     print item.group()

        self.log.info('completed the ``_get_slides`` method')
        return slides

    # use the tab-trigger below for new method
    def _get_reveal_config(
            self,
            metadata):
        """* get reveal config*

        **Key Arguments:**
            - ``metadata`` -- metadata dictionary parsed form markdown file yaml header.

        **Return:**
            - None

        **Usage:**
            ..  todo::

                add usage info
                create a sublime snippet for usage

            .. code-block:: python 

                usage code 

        .. todo::

            - @review: when complete, clean methodName method
            - @review: when complete add logging
        """
        self.log.info('starting the ``_get_reveal_config`` method')

        # DEFAULTS
        controls = "true"
        progress = "true"
        slidenumber = "false"
        history = "false"
        keyboard = "true"
        overview = "true"
        center = "true"
        touch = "true"
        loop = "true"
        rtl = "false"
        fragments = "true"
        embedded = "false"
        hhelp = "true"
        shownotes = "false"
        autoslide = 0
        autoslidestoppable = "true"
        mousewheel = "false"
        hideaddressbar = "true"
        previewlinks = "false"
        transition = 'slide'
        transitionspeed = '500'
        backgroundtransition = 'zoom'
        viewdistance = 3
        parallaxbackgroundimage = ''
        parallaxbackgroundsize = ''
        parallaxbackgroundhorizontal = ""
        parallaxbackgroundvertical = ""
        width = 960
        height = 700
        margin = 0.1
        minscale = 0.2
        maxscale = 1.5

        # UNPACK DICTIONARY VALUES TO LOCAL()
        for arg, val in metadata.iteritems():
            varname = arg
            if isinstance(val, str) or isinstance(val, unicode):
                if varname == "help":
                    varname = "hhelp"
                exec(varname + ' = """%s""" ' % (val,))
            else:
                exec(varname + " = %s" % (val,))
            self.log.debug('%s = %s' % (varname, val,))

        if "true" in slidenumber:
            slidenumber = "'c/t'"

        config = u"""// Full list of configuration options available at:
            // https://github.com/hakimel/reveal.js#configuration
            Reveal.initialize({
                controls: %(controls)s,
                progress: %(progress)s,
                slideNumber: %(slidenumber)s,
                history: %(history)s,
                keyboard: %(keyboard)s,
                overview: %(overview)s,
                center: %(center)s,
                touch: %(touch)s,
                loop: %(loop)s,
                rtl: %(rtl)s,
                fragments: %(fragments)s,
                embedded: %(embedded)s,
                help: %(hhelp)s,
                showNotes: %(shownotes)s,
                autoSlide: %(autoslide)s,
                autoSlideStoppable: %(autoslidestoppable)s,
                mouseWheel: %(mousewheel)s,
                hideAddressBar: %(hideaddressbar)s,
                previewLinks: %(previewlinks)s,
                transition: '%(transition)s',
                transitionSpeed: '%(transitionspeed)s',
                backgroundTransition: '%(backgroundtransition)s',
                viewDistance: %(viewdistance)s,
                parallaxBackgroundImage: '%(parallaxbackgroundimage)s',
                parallaxBackgroundSize: '%(parallaxbackgroundsize)s',
                parallaxBackgroundHorizontal: %(parallaxbackgroundhorizontal)s,
                parallaxBackgroundVertical: %(parallaxbackgroundvertical)s,
                width: %(width)s,
                height: %(height)s,
                margin: %(margin)s,
                minScale: %(minscale)s,
                maxScale: %(maxscale)s,

                // transition: 'slide', // none/fade/slide/convex/concave/zoom

                // Optional reveal.js plugins
                dependencies: [
                    { src: 'lib/js/classList.js', condition: function() { return !document.body.classList; } },
                    { src: 'plugin/markdown/marked.js', condition: function() { return !!document.querySelector( '[data-markdown]' ); } },
                    { src: 'plugin/markdown/markdown.js', condition: function() { return !!document.querySelector( '[data-markdown]' ); } },
                    { src: 'plugin/highlight/highlight.js', async: true, callback: function() { hljs.initHighlightingOnLoad(); } },
                    { src: 'plugin/zoom-js/zoom.js', async: true },
                    { src: 'plugin/notes/notes.js', async: true }
                ]
            });
    """ % locals()

        self.log.info('completed the ``_get_reveal_config`` method')
        return config

    # use the tab-trigger below for new method
    def get_deck_content(
            self):
        """*get deck content*

        **Key Arguments:**
            # -

        **Return:**
            - ``deck`` -- content of the HTML presentation deck

        **Usage:**
            ..  todo::

                add usage info
                create a sublime snippet for usage

            .. code-block:: python 

                usage code 

        .. todo::

            - @review: when complete, clean methodName method
            - @review: when complete add logging
        """
        self.log.info('starting the ``get_deck_content`` method')

        # PARSE MARKDOWN AND GENERATE CONTENT COMPONENTS
        htmlContent, metadata = self.parse_markdown()
        head = self._get_html_head(metadata=metadata)
        slides = self._get_slides(htmlContent=htmlContent)
        config = self._get_reveal_config(metadata=metadata)

        deck = u"""<!doctype html>
<html lang="en">

  %(head)s

  <body>

    <div class="reveal">
      <div class="slides">

        %(slides)s


      </div>
    </div>

    <script src="lib/js/head.min.js"></script>
    <script src="js/reveal.js"></script>
    

    <script>
    %(config)s
    </script>

    <script src="js/dynamic-theme.js"></script><script src="js/custom.js"></script>

  </body>
</html>""" % locals()

        self.log.info('completed the ``get_deck_content`` method')
        return deck

    # use the tab-trigger below for new method
    def _convert_notes(
            self,
            slides):
        """*Convert the notes from `Notes:` notation to the syntax expected by reveal.js*

        **Key Arguments:**
            - ``slides`` -- the HTML slides contents.

        **Return:**
            - ``slides`` -- newly formated slides with corrented notes

        **Usage:**
            ..  todo::

                add usage info
                create a sublime snippet for usage

            .. code-block:: python 

                usage code 

        .. todo::

            - @review: when complete, clean methodName method
            - @review: when complete add logging
        """
        self.log.info('starting the ``_convert_notes`` method')

        # ADD NOTES
        regex = re.compile(
            r'(<p>note(s)?\:\s*?</p>)(?P<note>.*?)<hr />', re.S | re.I)
        slides = regex.sub(
            """<aside class="notes">\g<note></aside><hr />""", slides)

        self.log.info('completed the ``_convert_notes`` method')
        return slides

    # use the tab-trigger below for new method
    def _add_slide_attributes(
            self,
            slide):
        """* add slide attributes*

        **Key Arguments:**
            - ``slide`` -- a single slide HTML content.

        **Return:**
            - ``slide`` -- slide as a <section> with HTML attributes added

        **Usage:**
            ..  todo::

                add usage info
                create a sublime snippet for usage

            .. code-block:: python 

                usage code 

        .. todo::

            - @review: when complete, clean methodName method
            - @review: when complete add logging
        """
        self.log.info('starting the ``_add_slide_attributes`` method')

        # FIND ALL SLIDE ATTRIBUTES AND OPTIONS FOR THE SLIDE
        sectionAtrributes = {}
        if "@slide" in slide:
            regex = re.compile(
                r'@slide-(?P<attr>[\w\-]+?)\((?P<keyvalue>.*?)(,\s*?(?P<options>.*?))?\)', re.I)
            thisIter = regex.finditer(slide)
            for item in thisIter:
                attr = item.group("attr")
                keyvalue = item.group("keyvalue")
                options = item.group("options")
                if attr not in sectionAtrributes.keys():
                    sectionAtrributes[attr] = {
                        "keyvalue": keyvalue,
                        "options": {}
                    }
                if options:
                    options = options.split(",")
                    for o in options:
                        oneOpt = o.strip().split("=")
                        sectionAtrributes[attr]["options"][
                            oneOpt[0]] = oneOpt[1]

            # REMOVE @SLIDE-... COMMANDS
            slide = regex.sub("", slide)
            print sectionAtrributes

        # CREATE THE SLIDE SECTION HEADER
        section = "<section"
        for k, v in sectionAtrributes.iteritems():
            attr = v["keyvalue"]
            section = """%(section)s data-%(k)s="%(attr)s" """ % locals()
            for opt, optVal in v["options"].iteritems():
                section = """%(section)s data-%(k)s-%(opt)s="%(optVal)s" """ % locals()
            print section

        slide = """%(section)s>%(slide)s</section>""" % locals()

        # # ADD BACKGROUND ATTRIBUTES
        # regex = re.compile(
        #     r'<section(?P<attr>(?:(?!>).)*?)>(?P<con1>(?:(?!</section>).)*?)<p>@slide-background\((?P<background>.*?)\)(\n|</p>)(?P<con2>.*?)</section>', re.S | re.I)
        # thisIter = regex.finditer(slide)
        # for item in thisIter:

        #     background = item.group("background").strip().split(" ")
        #     print background
        #     attr = item.group("attr")
        #     con1 = item.group("con1")
        #     con2 = item.group("con2")
        #     # print attr
        #     theseAttr = ""
        #     for b in background:
        #         if "/" in b:
        #             if ".mov" not in b and ".mp4" not in b:
        #                 theseAttr += """ data-background="%(b)s" """ % locals()
        #         if "#" in b:
        #             theseAttr += """ data-background="%(b)s" """ % locals()
        #         if b in self.transitions:
        #             theseAttr += """ data-background-transition """ % locals(
        #             )
        #     replace = """<section %(attr)s %(theseAttr)s>%(con1)s%(con2)s</section>""" % locals()
        #     slide = slide.replace(item.group(), replace)

        # slide = """<section>%(slide)s</section>""" % locals()

        self.log.info('completed the ``_add_slide_attributes`` method')
        return slide

    # use the tab-trigger below for new method
    # xt-class-method

    # 5. @flagged: what actions of the base class(es) need ammending? ammend them here
    # Override Method Attributes
    # method-override-tmpx
