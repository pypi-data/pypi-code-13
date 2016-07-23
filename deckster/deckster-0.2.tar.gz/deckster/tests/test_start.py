import os
import nose
import shutil
import yaml
import codecs
from deckster import start, cl_utils
from deckster.utKit import utKit

from fundamentals import tools

su = tools(
    arguments={"settingsFile": None},
    docString=__doc__,
    logLevel="WARNING",
    options_first=False,
    projectName="deckster",
    tunnel=False
)
arguments, settings, log, dbConn = su.setup()


# SETUP AND TEARDOWN FIXTURE FUNCTIONS FOR THE ENTIRE MODULE
moduleDirectory = os.path.dirname(__file__)

# load settings
stream = file(moduleDirectory +
              "/example_settings.yaml", 'r')
settings = yaml.load(stream)
stream.close()

utKit = utKit(moduleDirectory)
log, dbConn, pathToInputDir, pathToOutputDir = utKit.setupModule()
utKit.tearDownModule()

try:
    import shutil
    shutil.rmtree(pathToOutputDir + "/thespacedoctor test presentation")
except:
    pass

try:
    # Recursively create missing directories
    if not os.path.exists(pathToOutputDir):
        os.makedirs(pathToOutputDir)
except:
    pass

pathToWriteFile = pathToOutputDir + "/nosetest_debug.log"
try:
    log.debug("attempting to open the file %s" % (pathToWriteFile,))
    writeFile = codecs.open(pathToWriteFile, encoding='utf-8', mode='w')
except IOError, e:
    message = 'could not open the file %s' % (pathToWriteFile,)
    log.critical(message)
    raise IOError(message)
writeFile.write("")
writeFile.close()


class test_start():

    def test_start_function(self):

        from deckster import start
        this = start(
            log=log,
            settings=settings,
            destinationPath=pathToOutputDir
        )

    def test_start_function_exception(self):

        from deckster import start
        try:
            this = start(
                log=log,
                settings=settings,
                fakeKey="break the code"
            )
            assert False
        except Exception, e:
            assert True
            print str(e)

        # x-print-testpage-for-pessto-marshall-web-object

    # x-class-to-test-named-worker-function
