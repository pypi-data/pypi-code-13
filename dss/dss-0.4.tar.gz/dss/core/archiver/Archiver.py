from threading import Timer, Thread, Event
import os
import sys
import time
import shutil
from tarFormat import tar, untar
from zipFormat import zip, unzip

__all__ = ['Archive']
DEST_DIR = "compressed"
DEBUG = 0

SIZE_REACHED = "Archived reason: SIZE reached"
TIME_REACHED = "Archived reason: TIME reached"

class Archive():
    """ Archiver is a dynamic class that allows each plugin to have their own settings for:
        - fileFormat: 'zip' and 'tar' (tar-with bzip2 compression)
        - archiverSize: data is compressed when limit is reached (in bytes).
        - sizeCheckPeriod: how often to check if the data's size has been exceeded (in seconds).
        - archiverTimeInterval: data is compressed, regardless of size, at set intervals (in seconds).
        - logSource: the path location where the data to compress is located (path location). """

    def __init__(self, plugin, archiverConfigs):
        self.plugin = plugin
        self.fileFormat = archiverConfigs["File Format"]["Selected"]
        self.archiverSize = archiverConfigs["Archive Size"]["Value"]
        self.sizeCheckPeriod = archiverConfigs["Size Check Period"]["Value"]
        self.archiverTimeInterval = archiverConfigs["Archive Time Interval"]["Value"]

        self.logSource = os.path.join(plugin.output_dir, '')
        self.logDest = self.getDestPath()

        #Flag to execute or not
        self.executeArchiverFunction = 1    #1 for true, yes

        # keep for checks in method start/stop
        self.timeIntervalArchiver = None
        self.fileSizeArchiver = None
        self.currentFileSize = 0

        # 2 Archivers (2 threads) could run if both archiverTimeInterval and sizeCheckPeriod are given.
        # If archiver time is given, it has precedence above the checkFileSize option
        if self.archiverTimeInterval > 0:
            self.timeIntervalArchiver = PerpetualTimer(self.archiverTimeInterval, self.compress)

        if self.archiverSize > 0 and self.sizeCheckPeriod > 0:
            self.fileSizeArchiver = PerpetualTimer(self.sizeCheckPeriod, self.checkFileSize)

    def getDestPath(self):
        # Returns the full destination path with newly appended file name without the file extension
        # e.g. "../Users/../log"

        compressDir = os.path.join(self.plugin.base_dir, DEST_DIR)
        fileName = os.path.splitext(os.path.basename(self.logSource))[0]
        dest_path = os.path.join(compressDir, fileName)

        if not os.path.exists(dest_path):
            if os.path.isdir(dest_path):
                print("  Creating archiver destination directory: %s" % dest_path)
                os.makedirs(dest_path)

        return dest_path


    def getSourceSize(self):
        if os.path.isfile(self.logSource):
            return os.path.getsize(self.logSource)
        elif os.path.isdir(self.logSource):
            totalSize = 0
            for dirPath, dirNames, fileNames in os.walk(self.logSource):
                for aFile in fileNames:
                    filePath = os.path.join(dirPath, aFile)
                    totalSize += os.path.getsize(filePath)
            return totalSize

    def checkFileSize(self):
        self.currentFileSize = self.getSourceSize()
        if self.currentFileSize >= self.archiverSize:
            print("   File size limit %i-B reached, compressing: %s" % (self.archiverSize, self.logSource))
            print(" Current file size: %s " % self.currentFileSize)
            self.compress()

    def compress(self):
        if self.executeArchiverFunction == 1:
            self.suspend()
            self.printDebugInfo("Compress function")

            doPluginInterrupt = self.plugin.is_live()
            if doPluginInterrupt:
                self.plugin.terminate()

            self.append_to_metafile()

            if self.fileFormat == "zip":
                zip(self.logSource, self.logDest)
            elif self.fileFormat == "tar":
                tar(self.logSource, self.logDest)
            else:
                print ("   Invalid file format given: %s (compression will continue with zip)" % self.fileFormat)
                zip(self.logSource, self.logDest)

            self.delDirContents(self.logSource)

            if doPluginInterrupt:
                print(" [Archiver starting: %s]" % self.plugin.name)
                self.plugin.process = self.plugin.run()

            self.resume()

    # TODO test decompress further
    def decompress(self):
        if self.executeArchiverFunction == 1:
            self.suspend()                      # Make sure no compression is done while un-compressing
            self.plugin.stop()

            if self.fileFormat == "zip":
                unzip(self.logSource, self.logDest)
                self.delDirContents(self.logDest)
            elif self.fileFormat == "tar":
                untar(self.logSource, self.logDest)
                self.delDirContents(self.logDest)
            else:
                print ("   Could not decompress plugin: %s" % self.plugin.name)

            self.plugin.process = self.plugin.start()
            self.resume()                       # Resume Archiver compression

    # Removes the contents inside a directory, but not the directory itself.
    def delDirContents(self, dir):
        if os.path.exists(dir):
            for aFile in os.listdir(dir):
                path = os.path.join(dir, aFile)
                try:
                    if os.path.isfile(path):
                        os.unlink(path)
                    elif os.path.isdir(path):
                        shutil.rmtree(path, ignore_errors=True)
                except Exception as e:
                    print (e)

    def append_to_metafile(self):
        epoch_time = str(int(time.time()))

        with open(self.plugin.metadata_file_path, "a") as metafile:
            metafile.write("\n\n" + "ARCHIVER ################################################" + "\n")

            if self.currentFileSize > self.archiverSize:
                metafile.write("Reason= reached SIZE" + "\n")
            else:
                metafile.write("Reason= reached TIME" + "\n")

            metafile.write("Time archived= " + epoch_time + "\n")
            metafile.write("Size Limit= " + str(self.archiverSize)+"\n")
            metafile.write("Size Check= " + str(self.currentFileSize) + "\n")
            metafile.write("Size Check Interval= " + str(self.sizeCheckPeriod) + "\n")
            metafile.write("Archive Time Interval= " + str(self.archiverTimeInterval) + "\n")
            metafile.write("Type of file= " + str(self.plugin.ext) + "\n")

    def start(self):
        if self.timeIntervalArchiver is not None:
            self.timeIntervalArchiver.start()

        if self.fileSizeArchiver is not None:
            self.fileSizeArchiver.start();

    def stop(self):
        if self.timeIntervalArchiver is not None:
            self.timeIntervalArchiver.cancel()

        if self.fileSizeArchiver is not None:
            self.fileSizeArchiver.cancel()

    def suspend(self):
        # The threads cannot be suspended that easy, so a way to do it is to keep the timer threads running,
        # but do not execute the archiver function if it is in the suspend state
        if self.timeIntervalArchiver is not None:
            self.executeArchiverFunction = 0

        if self.archiverTimeInterval is not None:
            self.executeArchiverFunction = 0

    def resume(self):
        # if the archiver function is suspended, then resume it to enable execution
        if self.timeIntervalArchiver is not None:
            self.executeArchiverFunction = 1

        if self.archiverTimeInterval is not None:
            self.executeArchiverFunction = 1

    def printDebugInfo(self, callerKey):
        # Debug info:
        if DEBUG:
            print ("------------------------------------------------------------------")
            print ("Archiver DEBUG info, from %s"% callerKey)
            print ("    File Format: %s" % self.fileFormat)
            print ("    Archiver Size: %s" % self.archiverSize)
            print ("    Size Check Period: %s" % self.sizeCheckPeriod)
            print ("    Archiver TImer Interval: %s" % self.archiverTimeInterval)
            print ("    Log Source: %s" % self.logSource)
            print ("    Log Destination: %s" % self.logDest)
            print ("------------------------------------------------------------------")

# TODO Source file might need to be rotated in order to compress. Then, raw duplicate data is deleted afterwards.

class PerpetualTimer:
    def __init__(self, t, hFunction):
        self.t = t
        self.hFunction = hFunction
        self.thread = Timer(self.t, self.handle_function)

    def handle_function(self):
        self.hFunction()
        self.thread = Timer(self.t, self.handle_function)
        self.thread.start()

    def start(self):
        self.thread.start()

    def cancel(self):
        self.thread.cancel()
