# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from __future__ import unicode_literals

from django.db import models


class AdobeAdditionalmetadata(models.Model):
    id_local = models.IntegerField(primary_key=True, null=False)
    id_global = models.TextField(unique=True)  # This field type is a guess.
    additionalinfoset = models.IntegerField(db_column='additionalInfoSet')  # Field name made lowercase.
    embeddedxmp = models.IntegerField(db_column='embeddedXmp')  # Field name made lowercase.
    externalxmpisdirty = models.IntegerField(db_column='externalXmpIsDirty')  # Field name made lowercase.
    image = models.IntegerField(blank=True, null=True)
    incrementalwhitebalance = models.IntegerField(db_column='incrementalWhiteBalance')  # Field name made lowercase.
    internalxmpdigest = models.TextField(db_column='internalXmpDigest', blank=True, null=True)  # Field name made lowercase. This field type is a guess.
    israwfile = models.IntegerField(db_column='isRawFile')  # Field name made lowercase.
    lastsynchronizedhash = models.TextField(db_column='lastSynchronizedHash', blank=True, null=True)  # Field name made lowercase. This field type is a guess.
    lastsynchronizedtimestamp = models.TextField(db_column='lastSynchronizedTimestamp')  # Field name made lowercase. This field type is a guess.
    metadatapresetid = models.TextField(db_column='metadataPresetID', blank=True, null=True)  # Field name made lowercase. This field type is a guess.
    metadataversion = models.TextField(db_column='metadataVersion', blank=True, null=True)  # Field name made lowercase. This field type is a guess.
    monochrome = models.IntegerField()
    xmp = models.TextField()  # This field type is a guess.

    class Meta:
        managed = False
        db_table = 'Adobe_AdditionalMetadata'


class AdobeFaceproperties(models.Model):
    id_local = models.IntegerField(primary_key=True, null=False)
    face = models.IntegerField(blank=True, null=True)
    propertiesstring = models.TextField(db_column='propertiesString', blank=True, null=True)  # Field name made lowercase. This field type is a guess.

    class Meta:
        managed = False
        db_table = 'Adobe_faceProperties'


class AdobeImagedevelopbeforesettings(models.Model):
    id_local = models.IntegerField(primary_key=True, null=False)
    beforedigest = models.TextField(db_column='beforeDigest', blank=True, null=True)  # Field name made lowercase. This field type is a guess.
    beforehasdevelopadjustments = models.TextField(db_column='beforeHasDevelopAdjustments', blank=True, null=True)  # Field name made lowercase. This field type is a guess.
    beforepresetid = models.TextField(db_column='beforePresetID', blank=True, null=True)  # Field name made lowercase. This field type is a guess.
    beforetext = models.TextField(db_column='beforeText', blank=True, null=True)  # Field name made lowercase. This field type is a guess.
    developsettings = models.IntegerField(db_column='developSettings', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Adobe_imageDevelopBeforeSettings'


class AdobeImagedevelopsettings(models.Model):
    id_local = models.IntegerField(primary_key=True, null=False)
    allowfastrender = models.IntegerField(db_column='allowFastRender', blank=True, null=True)  # Field name made lowercase.
    beforesettingsidcache = models.TextField(db_column='beforeSettingsIDCache', blank=True, null=True)  # Field name made lowercase. This field type is a guess.
    croppedheight = models.TextField(db_column='croppedHeight', blank=True, null=True)  # Field name made lowercase. This field type is a guess.
    croppedwidth = models.TextField(db_column='croppedWidth', blank=True, null=True)  # Field name made lowercase. This field type is a guess.
    digest = models.TextField(blank=True, null=True)  # This field type is a guess.
    fileheight = models.TextField(db_column='fileHeight', blank=True, null=True)  # Field name made lowercase. This field type is a guess.
    filewidth = models.TextField(db_column='fileWidth', blank=True, null=True)  # Field name made lowercase. This field type is a guess.
    grayscale = models.IntegerField(blank=True, null=True)
    hasdevelopadjustments = models.IntegerField(db_column='hasDevelopAdjustments', blank=True, null=True)  # Field name made lowercase.
    hasdevelopadjustmentsex = models.TextField(db_column='hasDevelopAdjustmentsEx', blank=True, null=True)  # Field name made lowercase. This field type is a guess.
    historysettingsid = models.TextField(db_column='historySettingsID', blank=True, null=True)  # Field name made lowercase. This field type is a guess.
    image = models.IntegerField(blank=True, null=True)
    processversion = models.TextField(db_column='processVersion', blank=True, null=True)  # Field name made lowercase. This field type is a guess.
    settingsid = models.TextField(db_column='settingsID', blank=True, null=True)  # Field name made lowercase. This field type is a guess.
    snapshotid = models.TextField(db_column='snapshotID', blank=True, null=True)  # Field name made lowercase. This field type is a guess.
    text = models.TextField(blank=True, null=True)  # This field type is a guess.
    validatedforversion = models.TextField(db_column='validatedForVersion', blank=True, null=True)  # Field name made lowercase. This field type is a guess.
    whitebalance = models.TextField(db_column='whiteBalance', blank=True, null=True)  # Field name made lowercase. This field type is a guess.

    class Meta:
        managed = False
        db_table = 'Adobe_imageDevelopSettings'


class AdobeImageproofsettings(models.Model):
    id_local = models.IntegerField(primary_key=True, null=False)
    colorprofile = models.TextField(db_column='colorProfile', blank=True, null=True)  # Field name made lowercase. This field type is a guess.
    image = models.IntegerField(blank=True, null=True)
    renderingintent = models.TextField(db_column='renderingIntent', blank=True, null=True)  # Field name made lowercase. This field type is a guess.

    class Meta:
        managed = False
        db_table = 'Adobe_imageProofSettings'


class AdobeImageproperties(models.Model):
    id_local = models.IntegerField(primary_key=True, null=False)
    id_global = models.TextField(unique=True)  # This field type is a guess.
    image = models.IntegerField(blank=True, null=True)
    propertiesstring = models.TextField(db_column='propertiesString', blank=True, null=True)  # Field name made lowercase. This field type is a guess.

    class Meta:
        managed = False
        db_table = 'Adobe_imageProperties'


class AdobeImages(models.Model):
    id_local = models.IntegerField(primary_key=True, null=False)
    id_global = models.TextField(unique=True)  # This field type is a guess.
    aspectratiocache = models.TextField(db_column='aspectRatioCache')  # Field name made lowercase. This field type is a guess.
    bitdepth = models.TextField(db_column='bitDepth')  # Field name made lowercase. This field type is a guess.
    capturetime = models.TextField(db_column='captureTime', blank=True, null=True)  # Field name made lowercase. This field type is a guess.
    colorchannels = models.TextField(db_column='colorChannels')  # Field name made lowercase. This field type is a guess.
    colorlabels = models.TextField(db_column='colorLabels')  # Field name made lowercase. This field type is a guess.
    colormode = models.TextField(db_column='colorMode')  # Field name made lowercase. This field type is a guess.
    copycreationtime = models.TextField(db_column='copyCreationTime')  # Field name made lowercase. This field type is a guess.
    copyname = models.TextField(db_column='copyName', blank=True, null=True)  # Field name made lowercase. This field type is a guess.
    copyreason = models.TextField(db_column='copyReason', blank=True, null=True)  # Field name made lowercase. This field type is a guess.
    developsettingsidcache = models.TextField(db_column='developSettingsIDCache', blank=True, null=True)  # Field name made lowercase. This field type is a guess.
    fileformat = models.TextField(db_column='fileFormat')  # Field name made lowercase. This field type is a guess.
    fileheight = models.TextField(db_column='fileHeight', blank=True, null=True)  # Field name made lowercase. This field type is a guess.
    filewidth = models.TextField(db_column='fileWidth', blank=True, null=True)  # Field name made lowercase. This field type is a guess.
    hasmissingsidecars = models.IntegerField(db_column='hasMissingSidecars', blank=True, null=True)  # Field name made lowercase.
    masterimage = models.IntegerField(db_column='masterImage', blank=True, null=True)  # Field name made lowercase.
    orientation = models.TextField(blank=True, null=True)  # This field type is a guess.
    originalcapturetime = models.TextField(db_column='originalCaptureTime', blank=True, null=True)  # Field name made lowercase. This field type is a guess.
    originalrootentity = models.IntegerField(db_column='originalRootEntity', blank=True, null=True)  # Field name made lowercase.
    panningdistanceh = models.TextField(db_column='panningDistanceH', blank=True, null=True)  # Field name made lowercase. This field type is a guess.
    panningdistancev = models.TextField(db_column='panningDistanceV', blank=True, null=True)  # Field name made lowercase. This field type is a guess.
    pick = models.TextField()  # This field type is a guess.
    positioninfolder = models.TextField(db_column='positionInFolder')  # Field name made lowercase. This field type is a guess.
    propertiescache = models.TextField(db_column='propertiesCache', blank=True, null=True)  # Field name made lowercase. This field type is a guess.
    pyramididcache = models.TextField(db_column='pyramidIDCache', blank=True, null=True)  # Field name made lowercase. This field type is a guess.
    rating = models.TextField(blank=True, null=True)  # This field type is a guess.
    rootfile = models.IntegerField(db_column='rootFile')  # Field name made lowercase.
    sidecarstatus = models.TextField(db_column='sidecarStatus', blank=True, null=True)  # Field name made lowercase. This field type is a guess.
    touchcount = models.TextField(db_column='touchCount')  # Field name made lowercase. This field type is a guess.
    touchtime = models.TextField(db_column='touchTime')  # Field name made lowercase. This field type is a guess.

    class Meta:
        managed = False
        db_table = 'Adobe_images'


class AdobeLibraryimagedevelophistorystep(models.Model):
    id_local = models.IntegerField(primary_key=True, null=False)
    id_global = models.TextField(unique=True)  # This field type is a guess.
    datecreated = models.TextField(db_column='dateCreated', blank=True, null=True)  # Field name made lowercase. This field type is a guess.
    digest = models.TextField(blank=True, null=True)  # This field type is a guess.
    hasdevelopadjustments = models.TextField(db_column='hasDevelopAdjustments', blank=True, null=True)  # Field name made lowercase. This field type is a guess.
    image = models.IntegerField(blank=True, null=True)
    name = models.TextField(blank=True, null=True)  # This field type is a guess.
    relvaluestring = models.TextField(db_column='relValueString', blank=True, null=True)  # Field name made lowercase. This field type is a guess.
    text = models.TextField(blank=True, null=True)  # This field type is a guess.
    valuestring = models.TextField(db_column='valueString', blank=True, null=True)  # Field name made lowercase. This field type is a guess.

    class Meta:
        managed = False
        db_table = 'Adobe_libraryImageDevelopHistoryStep'


class AdobeLibraryimagedevelopsnapshot(models.Model):
    id_local = models.IntegerField(primary_key=True, null=False)
    id_global = models.TextField(unique=True)  # This field type is a guess.
    digest = models.TextField(blank=True, null=True)  # This field type is a guess.
    hasdevelopadjustments = models.TextField(db_column='hasDevelopAdjustments', blank=True, null=True)  # Field name made lowercase. This field type is a guess.
    image = models.IntegerField(blank=True, null=True)
    locked = models.TextField(blank=True, null=True)  # This field type is a guess.
    name = models.TextField(blank=True, null=True)  # This field type is a guess.
    snapshotid = models.TextField(db_column='snapshotID', blank=True, null=True)  # Field name made lowercase. This field type is a guess.
    text = models.TextField(blank=True, null=True)  # This field type is a guess.

    class Meta:
        managed = False
        db_table = 'Adobe_libraryImageDevelopSnapshot'


class AdobeLibraryimagefaceprocesshistory(models.Model):
    id_local = models.IntegerField(primary_key=True, null=False)
    image = models.IntegerField()
    lastfacedetector = models.TextField(db_column='lastFaceDetector', blank=True, null=True)  # Field name made lowercase. This field type is a guess.
    lastfacerecognizer = models.TextField(db_column='lastFaceRecognizer', blank=True, null=True)  # Field name made lowercase. This field type is a guess.
    lastimageindexer = models.TextField(db_column='lastImageIndexer', blank=True, null=True)  # Field name made lowercase. This field type is a guess.
    lastimageorientation = models.TextField(db_column='lastImageOrientation', blank=True, null=True)  # Field name made lowercase. This field type is a guess.
    lasttrystatus = models.TextField(db_column='lastTryStatus', blank=True, null=True)  # Field name made lowercase. This field type is a guess.
    usertouched = models.TextField(db_column='userTouched', blank=True, null=True)  # Field name made lowercase. This field type is a guess.

    class Meta:
        managed = False
        db_table = 'Adobe_libraryImageFaceProcessHistory'


class AdobeNamedidentityplate(models.Model):
    id_local = models.IntegerField(primary_key=True, null=False)
    id_global = models.TextField(unique=True)  # This field type is a guess.
    description = models.TextField(blank=True, null=True)  # This field type is a guess.
    identityplate = models.TextField(db_column='identityPlate', blank=True, null=True)  # Field name made lowercase. This field type is a guess.
    identityplatehash = models.TextField(db_column='identityPlateHash', blank=True, null=True)  # Field name made lowercase. This field type is a guess.
    modulefont = models.TextField(db_column='moduleFont', blank=True, null=True)  # Field name made lowercase. This field type is a guess.
    moduleselectedtextcolor = models.TextField(db_column='moduleSelectedTextColor', blank=True, null=True)  # Field name made lowercase. This field type is a guess.
    moduletextcolor = models.TextField(db_column='moduleTextColor', blank=True, null=True)  # Field name made lowercase. This field type is a guess.

    class Meta:
        managed = False
        db_table = 'Adobe_namedIdentityPlate'


class AdobeVariables(models.Model):
    id_local = models.IntegerField(primary_key=True, null=False)
    id_global = models.TextField(unique=True)  # This field type is a guess.
    name = models.TextField(blank=True, null=True)  # This field type is a guess.
    value = models.TextField(blank=True, null=True)  # This field type is a guess.

    class Meta:
        managed = False
        db_table = 'Adobe_variables'


class AdobeVariablestable(models.Model):
    id_local = models.IntegerField(primary_key=True, null=False)
    id_global = models.TextField(unique=True)  # This field type is a guess.
    name = models.TextField(blank=True, null=True)  # This field type is a guess.
    type = models.TextField(blank=True, null=True)  # This field type is a guess.
    value = models.TextField()  # This field type is a guess.

    class Meta:
        managed = False
        db_table = 'Adobe_variablesTable'


class Agdngproxyinfo(models.Model):
    id_local = models.IntegerField(primary_key=True, null=False)
    fileuuid = models.TextField(db_column='fileUUID')  # Field name made lowercase. This field type is a guess.
    status = models.TextField()  # This field type is a guess.
    statusdatetime = models.TextField(db_column='statusDateTime')  # Field name made lowercase. This field type is a guess.

    class Meta:
        managed = False
        db_table = 'AgDNGProxyInfo'


class Agdngproxyinfoupdater(models.Model):
    id_local = models.IntegerField(primary_key=True, null=False)
    taskid = models.TextField(db_column='taskID', unique=True)  # Field name made lowercase. This field type is a guess.
    taskstatus = models.TextField(db_column='taskStatus')  # Field name made lowercase. This field type is a guess.
    whenposted = models.TextField(db_column='whenPosted')  # Field name made lowercase. This field type is a guess.

    class Meta:
        managed = False
        db_table = 'AgDNGProxyInfoUpdater'


class Agdeletedozalbumassetids(models.Model):
    ozcatalogid = models.TextField(db_column='ozCatalogId')  # Field name made lowercase. This field type is a guess.
    ozalbumassetid = models.TextField(db_column='ozAlbumAssetId')  # Field name made lowercase. This field type is a guess.
    changecounter = models.TextField(db_column='changeCounter', blank=True, null=True)  # Field name made lowercase. This field type is a guess.

    class Meta:
        managed = False
        db_table = 'AgDeletedOzAlbumAssetIds'
        unique_together = (('ozcatalogid', 'ozalbumassetid'),)


class Agdeletedozalbumids(models.Model):
    ozcatalogid = models.TextField(db_column='ozCatalogId')  # Field name made lowercase. This field type is a guess.
    ozalbumid = models.TextField(db_column='ozAlbumId')  # Field name made lowercase. This field type is a guess.
    changecounter = models.TextField(db_column='changeCounter', blank=True, null=True)  # Field name made lowercase. This field type is a guess.

    class Meta:
        managed = False
        db_table = 'AgDeletedOzAlbumIds'
        unique_together = (('ozcatalogid', 'ozalbumid'),)


class Agdeletedozassetids(models.Model):
    ozcatalogid = models.TextField(db_column='ozCatalogId')  # Field name made lowercase. This field type is a guess.
    ozassetid = models.TextField(db_column='ozAssetId')  # Field name made lowercase. This field type is a guess.
    changecounter = models.TextField(db_column='changeCounter', blank=True, null=True)  # Field name made lowercase. This field type is a guess.

    class Meta:
        managed = False
        db_table = 'AgDeletedOzAssetIds'
        unique_together = (('ozcatalogid', 'ozassetid'),)


class Agdeletedozspaceids(models.Model):
    ozcatalogid = models.TextField(db_column='ozCatalogId')  # Field name made lowercase. This field type is a guess.
    ozspaceid = models.TextField(db_column='ozSpaceId')  # Field name made lowercase. This field type is a guess.
    changecounter = models.TextField(db_column='changeCounter', blank=True, null=True)  # Field name made lowercase. This field type is a guess.

    class Meta:
        managed = False
        db_table = 'AgDeletedOzSpaceIds'
        unique_together = (('ozcatalogid', 'ozspaceid'),)


class Agfoldercontent(models.Model):
    id_local = models.IntegerField(primary_key=True, null=False)
    id_global = models.TextField(unique=True)  # This field type is a guess.
    containingfolder = models.IntegerField(db_column='containingFolder')  # Field name made lowercase.
    content = models.TextField(blank=True, null=True)  # This field type is a guess.
    name = models.TextField(blank=True, null=True)  # This field type is a guess.
    owningmodule = models.TextField(db_column='owningModule', blank=True, null=True)  # Field name made lowercase. This field type is a guess.

    class Meta:
        managed = False
        db_table = 'AgFolderContent'


class Agharvesteddngmetadata(models.Model):
    id_local = models.IntegerField(primary_key=True, null=False)
    image = models.IntegerField(blank=True, null=True)
    hasfastloaddata = models.IntegerField(db_column='hasFastLoadData', blank=True, null=True)  # Field name made lowercase.
    haslossycompression = models.IntegerField(db_column='hasLossyCompression', blank=True, null=True)  # Field name made lowercase.
    isdng = models.IntegerField(db_column='isDNG', blank=True, null=True)  # Field name made lowercase.
    ishdr = models.IntegerField(db_column='isHDR', blank=True, null=True)  # Field name made lowercase.
    ispano = models.IntegerField(db_column='isPano', blank=True, null=True)  # Field name made lowercase.
    isreducedresolution = models.IntegerField(db_column='isReducedResolution', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'AgHarvestedDNGMetadata'


class Agharvestedexifmetadata(models.Model):
    id_local = models.IntegerField(primary_key=True, null=False)
    image = models.IntegerField(blank=True, null=True)
    aperture = models.TextField(blank=True, null=True)  # This field type is a guess.
    cameramodelref = models.IntegerField(db_column='cameraModelRef', blank=True, null=True)  # Field name made lowercase.
    camerasnref = models.IntegerField(db_column='cameraSNRef', blank=True, null=True)  # Field name made lowercase.
    dateday = models.TextField(db_column='dateDay', blank=True, null=True)  # Field name made lowercase. This field type is a guess.
    datemonth = models.TextField(db_column='dateMonth', blank=True, null=True)  # Field name made lowercase. This field type is a guess.
    dateyear = models.TextField(db_column='dateYear', blank=True, null=True)  # Field name made lowercase. This field type is a guess.
    flashfired = models.IntegerField(db_column='flashFired', blank=True, null=True)  # Field name made lowercase.
    focallength = models.TextField(db_column='focalLength', blank=True, null=True)  # Field name made lowercase. This field type is a guess.
    gpslatitude = models.TextField(db_column='gpsLatitude', blank=True, null=True)  # Field name made lowercase. This field type is a guess.
    gpslongitude = models.TextField(db_column='gpsLongitude', blank=True, null=True)  # Field name made lowercase. This field type is a guess.
    gpssequence = models.TextField(db_column='gpsSequence')  # Field name made lowercase. This field type is a guess.
    hasgps = models.IntegerField(db_column='hasGPS', blank=True, null=True)  # Field name made lowercase.
    isospeedrating = models.TextField(db_column='isoSpeedRating', blank=True, null=True)  # Field name made lowercase. This field type is a guess.
    lensref = models.IntegerField(db_column='lensRef', blank=True, null=True)  # Field name made lowercase.
    shutterspeed = models.TextField(db_column='shutterSpeed', blank=True, null=True)  # Field name made lowercase. This field type is a guess.

    class Meta:
        managed = False
        db_table = 'AgHarvestedExifMetadata'


class Agharvestediptcmetadata(models.Model):
    id_local = models.IntegerField(primary_key=True, null=False)
    image = models.IntegerField(blank=True, null=True)
    cityref = models.IntegerField(db_column='cityRef', blank=True, null=True)  # Field name made lowercase.
    copyrightstate = models.IntegerField(db_column='copyrightState', blank=True, null=True)  # Field name made lowercase.
    countryref = models.IntegerField(db_column='countryRef', blank=True, null=True)  # Field name made lowercase.
    creatorref = models.IntegerField(db_column='creatorRef', blank=True, null=True)  # Field name made lowercase.
    isocountrycoderef = models.IntegerField(db_column='isoCountryCodeRef', blank=True, null=True)  # Field name made lowercase.
    jobidentifierref = models.IntegerField(db_column='jobIdentifierRef', blank=True, null=True)  # Field name made lowercase.
    locationdataorigination = models.TextField(db_column='locationDataOrigination')  # Field name made lowercase. This field type is a guess.
    locationgpssequence = models.TextField(db_column='locationGPSSequence')  # Field name made lowercase. This field type is a guess.
    locationref = models.IntegerField(db_column='locationRef', blank=True, null=True)  # Field name made lowercase.
    stateref = models.IntegerField(db_column='stateRef', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'AgHarvestedIptcMetadata'


class Agharvestedmetadataworklist(models.Model):
    id_local = models.IntegerField(primary_key=True, null=False)
    taskid = models.TextField(db_column='taskID', unique=True)  # Field name made lowercase. This field type is a guess.
    taskstatus = models.TextField(db_column='taskStatus')  # Field name made lowercase. This field type is a guess.
    whenposted = models.TextField(db_column='whenPosted')  # Field name made lowercase. This field type is a guess.

    class Meta:
        managed = False
        db_table = 'AgHarvestedMetadataWorklist'


class Aginternedexifcameramodel(models.Model):
    id_local = models.IntegerField(primary_key=True, null=False)
    searchindex = models.TextField(db_column='searchIndex', blank=True, null=True)  # Field name made lowercase. This field type is a guess.
    value = models.TextField(blank=True, null=True)  # This field type is a guess.

    class Meta:
        managed = False
        db_table = 'AgInternedExifCameraModel'


class Aginternedexifcamerasn(models.Model):
    id_local = models.IntegerField(primary_key=True, null=False)
    searchindex = models.TextField(db_column='searchIndex', blank=True, null=True)  # Field name made lowercase. This field type is a guess.
    value = models.TextField(blank=True, null=True)  # This field type is a guess.

    class Meta:
        managed = False
        db_table = 'AgInternedExifCameraSN'


class Aginternedexiflens(models.Model):
    id_local = models.IntegerField(primary_key=True, null=False)
    searchindex = models.TextField(db_column='searchIndex', blank=True, null=True)  # Field name made lowercase. This field type is a guess.
    value = models.TextField(blank=True, null=True)  # This field type is a guess.

    class Meta:
        managed = False
        db_table = 'AgInternedExifLens'


class Aginternediptccity(models.Model):
    id_local = models.IntegerField(primary_key=True, null=False)
    searchindex = models.TextField(db_column='searchIndex', blank=True, null=True)  # Field name made lowercase. This field type is a guess.
    value = models.TextField(blank=True, null=True)  # This field type is a guess.

    class Meta:
        managed = False
        db_table = 'AgInternedIptcCity'


class Aginternediptccountry(models.Model):
    id_local = models.IntegerField(primary_key=True, null=False)
    searchindex = models.TextField(db_column='searchIndex', blank=True, null=True)  # Field name made lowercase. This field type is a guess.
    value = models.TextField(blank=True, null=True)  # This field type is a guess.

    class Meta:
        managed = False
        db_table = 'AgInternedIptcCountry'


class Aginternediptccreator(models.Model):
    id_local = models.IntegerField(primary_key=True, null=False)
    searchindex = models.TextField(db_column='searchIndex', blank=True, null=True)  # Field name made lowercase. This field type is a guess.
    value = models.TextField(blank=True, null=True)  # This field type is a guess.

    class Meta:
        managed = False
        db_table = 'AgInternedIptcCreator'


class Aginternediptcisocountrycode(models.Model):
    id_local = models.IntegerField(primary_key=True, null=False)
    searchindex = models.TextField(db_column='searchIndex', blank=True, null=True)  # Field name made lowercase. This field type is a guess.
    value = models.TextField(blank=True, null=True)  # This field type is a guess.

    class Meta:
        managed = False
        db_table = 'AgInternedIptcIsoCountryCode'


class Aginternediptcjobidentifier(models.Model):
    id_local = models.IntegerField(primary_key=True, null=False)
    searchindex = models.TextField(db_column='searchIndex', blank=True, null=True)  # Field name made lowercase. This field type is a guess.
    value = models.TextField(blank=True, null=True)  # This field type is a guess.

    class Meta:
        managed = False
        db_table = 'AgInternedIptcJobIdentifier'


class Aginternediptclocation(models.Model):
    id_local = models.IntegerField(primary_key=True, null=False)
    searchindex = models.TextField(db_column='searchIndex', blank=True, null=True)  # Field name made lowercase. This field type is a guess.
    value = models.TextField(blank=True, null=True)  # This field type is a guess.

    class Meta:
        managed = False
        db_table = 'AgInternedIptcLocation'


class Aginternediptcstate(models.Model):
    id_local = models.IntegerField(primary_key=True, null=False)
    searchindex = models.TextField(db_column='searchIndex', blank=True, null=True)  # Field name made lowercase. This field type is a guess.
    value = models.TextField(blank=True, null=True)  # This field type is a guess.

    class Meta:
        managed = False
        db_table = 'AgInternedIptcState'


class Aglastcatalogexport(models.Model):
    image = models.IntegerField(primary_key=True, null=False)

    class Meta:
        managed = False
        db_table = 'AgLastCatalogExport'


class Aglibrarycollection(models.Model):
    id_local = models.IntegerField(primary_key=True, null=False)
    creationid = models.TextField(db_column='creationId')  # Field name made lowercase. This field type is a guess.
    genealogy = models.TextField()  # This field type is a guess.
    imagecount = models.TextField(db_column='imageCount', blank=True, null=True)  # Field name made lowercase. This field type is a guess.
    name = models.TextField()  # This field type is a guess.
    parent = models.IntegerField(blank=True, null=True)
    systemonly = models.TextField(db_column='systemOnly')  # Field name made lowercase. This field type is a guess.

    class Meta:
        managed = False
        db_table = 'AgLibraryCollection'


class Aglibrarycollectionchangecounter(models.Model):
    collection = models.TextField(primary_key=True, null=False)  # This field type is a guess.
    changecounter = models.TextField(db_column='changeCounter', blank=True, null=True)  # Field name made lowercase. This field type is a guess.

    class Meta:
        managed = False
        db_table = 'AgLibraryCollectionChangeCounter'


class Aglibrarycollectioncontent(models.Model):
    id_local = models.IntegerField(primary_key=True, null=False)
    collection = models.IntegerField()
    content = models.TextField(blank=True, null=True)  # This field type is a guess.
    owningmodule = models.TextField(db_column='owningModule', blank=True, null=True)  # Field name made lowercase. This field type is a guess.

    class Meta:
        managed = False
        db_table = 'AgLibraryCollectionContent'


class Aglibrarycollectioncoverimage(models.Model):
    collection = models.TextField(primary_key=True, null=False)  # This field type is a guess.
    collectionimage = models.TextField(db_column='collectionImage')  # Field name made lowercase. This field type is a guess.

    class Meta:
        managed = False
        db_table = 'AgLibraryCollectionCoverImage'


class Aglibrarycollectionimage(models.Model):
    id_local = models.IntegerField(primary_key=True, null=False)
    collection = models.IntegerField()
    image = models.IntegerField()
    pick = models.TextField()  # This field type is a guess.
    positionincollection = models.TextField(db_column='positionInCollection', blank=True, null=True)  # Field name made lowercase. This field type is a guess.

    class Meta:
        managed = False
        db_table = 'AgLibraryCollectionImage'


class Aglibrarycollectionimagechangecounter(models.Model):
    collectionimage = models.TextField(db_column='collectionImage', primary_key=True, null=False)  # Field name made lowercase. This field type is a guess.
    collection = models.TextField()  # This field type is a guess.
    image = models.TextField()  # This field type is a guess.
    changecounter = models.TextField(db_column='changeCounter', blank=True, null=True)  # Field name made lowercase. This field type is a guess.

    class Meta:
        managed = False
        db_table = 'AgLibraryCollectionImageChangeCounter'


class Aglibrarycollectionimageozalbumassetids(models.Model):
    collectionimage = models.TextField(db_column='collectionImage')  # Field name made lowercase. This field type is a guess.
    collection = models.TextField()  # This field type is a guess.
    image = models.TextField()  # This field type is a guess.
    ozcatalogid = models.TextField(db_column='ozCatalogId')  # Field name made lowercase. This field type is a guess.
    ozalbumassetid = models.TextField(db_column='ozAlbumAssetId', blank=True, null=True)  # Field name made lowercase. This field type is a guess.

    class Meta:
        managed = False
        db_table = 'AgLibraryCollectionImageOzAlbumAssetIds'
        unique_together = (('collectionimage', 'ozcatalogid', 'collection', 'image'),)


class Aglibrarycollectionimageozsortorder(models.Model):
    collectionimage = models.TextField(db_column='collectionImage', primary_key=True, null=False)  # Field name made lowercase. This field type is a guess.
    collection = models.TextField()  # This field type is a guess.
    positionincollection = models.TextField(db_column='positionInCollection')  # Field name made lowercase. This field type is a guess.
    ozsortorder = models.TextField(db_column='ozSortOrder')  # Field name made lowercase. This field type is a guess.

    class Meta:
        managed = False
        db_table = 'AgLibraryCollectionImageOzSortOrder'


class Aglibrarycollectionozalbumids(models.Model):
    collection = models.TextField()  # This field type is a guess.
    ozcatalogid = models.TextField(db_column='ozCatalogId')  # Field name made lowercase. This field type is a guess.
    ozalbumid = models.TextField(db_column='ozAlbumId', blank=True, null=True)  # Field name made lowercase. This field type is a guess.

    class Meta:
        managed = False
        db_table = 'AgLibraryCollectionOzAlbumIds'
        unique_together = (('collection', 'ozcatalogid'),)


class Aglibrarycollectionstack(models.Model):
    id_local = models.IntegerField(primary_key=True, null=False)
    id_global = models.TextField(unique=True)  # This field type is a guess.
    collapsed = models.IntegerField()
    collection = models.IntegerField()
    text = models.TextField()  # This field type is a guess.

    class Meta:
        managed = False
        db_table = 'AgLibraryCollectionStack'


class Aglibrarycollectionstackdata(models.Model):
    stack = models.IntegerField(blank=True, null=True)
    collection = models.IntegerField()
    stackcount = models.IntegerField(db_column='stackCount')  # Field name made lowercase.
    stackparent = models.IntegerField(db_column='stackParent', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'AgLibraryCollectionStackData'


class Aglibrarycollectionstackimage(models.Model):
    id_local = models.IntegerField(primary_key=True, null=False)
    collapsed = models.IntegerField()
    collection = models.IntegerField()
    image = models.IntegerField()
    position = models.TextField()  # This field type is a guess.
    stack = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'AgLibraryCollectionStackImage'


class Aglibrarycollectionsyncedalbumdata(models.Model):
    collection = models.TextField()  # This field type is a guess.
    payloadkey = models.TextField(db_column='payloadKey')  # Field name made lowercase. This field type is a guess.
    payloaddata = models.TextField(db_column='payloadData')  # Field name made lowercase. This field type is a guess.

    class Meta:
        managed = False
        db_table = 'AgLibraryCollectionSyncedAlbumData'
        unique_together = (('collection', 'payloadkey'),)


class Aglibrarycollectiontrackedassets(models.Model):
    collection = models.TextField()  # This field type is a guess.
    ozcatalogid = models.TextField(db_column='ozCatalogId', blank=True, null=True)  # Field name made lowercase. This field type is a guess.

    class Meta:
        managed = False
        db_table = 'AgLibraryCollectionTrackedAssets'
        unique_together = (('collection', 'ozcatalogid'),)


class Aglibraryface(models.Model):
    id_local = models.IntegerField(primary_key=True, null=False)
    bl_x = models.TextField(blank=True, null=True)  # This field type is a guess.
    bl_y = models.TextField(blank=True, null=True)  # This field type is a guess.
    br_x = models.TextField(blank=True, null=True)  # This field type is a guess.
    br_y = models.TextField(blank=True, null=True)  # This field type is a guess.
    cluster = models.IntegerField(blank=True, null=True)
    compatibleversion = models.TextField(db_column='compatibleVersion', blank=True, null=True)  # Field name made lowercase. This field type is a guess.
    ignored = models.IntegerField(blank=True, null=True)
    image = models.IntegerField()
    imageorientation = models.TextField(db_column='imageOrientation')  # Field name made lowercase. This field type is a guess.
    orientation = models.TextField(blank=True, null=True)  # This field type is a guess.
    origination = models.TextField()  # This field type is a guess.
    propertiescache = models.TextField(db_column='propertiesCache', blank=True, null=True)  # Field name made lowercase. This field type is a guess.
    regiontype = models.TextField(db_column='regionType')  # Field name made lowercase. This field type is a guess.
    skipsuggestion = models.IntegerField(db_column='skipSuggestion', blank=True, null=True)  # Field name made lowercase.
    tl_x = models.TextField()  # This field type is a guess.
    tl_y = models.TextField()  # This field type is a guess.
    touchcount = models.TextField(db_column='touchCount')  # Field name made lowercase. This field type is a guess.
    touchtime = models.TextField(db_column='touchTime')  # Field name made lowercase. This field type is a guess.
    tr_x = models.TextField(blank=True, null=True)  # This field type is a guess.
    tr_y = models.TextField(blank=True, null=True)  # This field type is a guess.
    version = models.TextField(blank=True, null=True)  # This field type is a guess.

    class Meta:
        managed = False
        db_table = 'AgLibraryFace'


class Aglibraryfacecluster(models.Model):
    id_local = models.IntegerField(primary_key=True, null=False)
    keyface = models.IntegerField(db_column='keyFace', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'AgLibraryFaceCluster'


class Aglibraryfacedata(models.Model):
    id_local = models.IntegerField(primary_key=True, null=False)
    data = models.TextField(blank=True, null=True)  # This field type is a guess.
    face = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'AgLibraryFaceData'


class Aglibraryfile(models.Model):
    id_local = models.IntegerField(primary_key=True, null=False)
    id_global = models.TextField(unique=True)  # This field type is a guess.
    basename = models.TextField(db_column='baseName')  # Field name made lowercase. This field type is a guess.
    errormessage = models.TextField(db_column='errorMessage', blank=True, null=True)  # Field name made lowercase. This field type is a guess.
    errortime = models.TextField(db_column='errorTime', blank=True, null=True)  # Field name made lowercase. This field type is a guess.
    extension = models.TextField()  # This field type is a guess.
    externalmodtime = models.TextField(db_column='externalModTime', blank=True, null=True)  # Field name made lowercase. This field type is a guess.
    folder = models.IntegerField()
    idx_filename = models.TextField()  # This field type is a guess.
    importhash = models.TextField(db_column='importHash', blank=True, null=True)  # Field name made lowercase. This field type is a guess.
    lc_idx_filename = models.TextField()  # This field type is a guess.
    lc_idx_filenameextension = models.TextField(db_column='lc_idx_filenameExtension')  # Field name made lowercase. This field type is a guess.
    md5 = models.TextField(blank=True, null=True)  # This field type is a guess.
    modtime = models.TextField(db_column='modTime', blank=True, null=True)  # Field name made lowercase. This field type is a guess.
    originalfilename = models.TextField(db_column='originalFilename')  # Field name made lowercase. This field type is a guess.
    sidecarextensions = models.TextField(db_column='sidecarExtensions', blank=True, null=True)  # Field name made lowercase. This field type is a guess.

    class Meta:
        managed = False
        db_table = 'AgLibraryFile'
        unique_together = (('lc_idx_filename', 'folder'),)


class Aglibraryfileassetmetadata(models.Model):
    fileid = models.TextField(db_column='fileId', primary_key=True, null=False)  # Field name made lowercase. This field type is a guess.
    sha256 = models.TextField()  # This field type is a guess.
    filesize = models.TextField(db_column='fileSize', blank=True, null=True)  # Field name made lowercase. This field type is a guess.

    class Meta:
        managed = False
        db_table = 'AgLibraryFileAssetMetadata'


class Aglibraryfolder(models.Model):
    id_local = models.IntegerField(primary_key=True, null=False)
    id_global = models.TextField(unique=True)  # This field type is a guess.
    pathfromroot = models.TextField(db_column='pathFromRoot')  # Field name made lowercase. This field type is a guess.
    rootfolder = models.IntegerField(db_column='rootFolder')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'AgLibraryFolder'
        unique_together = (('rootfolder', 'pathfromroot'),)


class Aglibraryfolderstack(models.Model):
    id_local = models.IntegerField(primary_key=True, null=False)
    id_global = models.TextField(unique=True)  # This field type is a guess.
    collapsed = models.IntegerField()
    text = models.TextField()  # This field type is a guess.

    class Meta:
        managed = False
        db_table = 'AgLibraryFolderStack'


class Aglibraryfolderstackdata(models.Model):
    stack = models.IntegerField(blank=True, null=True)
    stackcount = models.IntegerField(db_column='stackCount')  # Field name made lowercase.
    stackparent = models.IntegerField(db_column='stackParent', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'AgLibraryFolderStackData'


class Aglibraryfolderstackimage(models.Model):
    id_local = models.IntegerField(primary_key=True, null=False)
    collapsed = models.IntegerField()
    image = models.IntegerField()
    position = models.TextField()  # This field type is a guess.
    stack = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'AgLibraryFolderStackImage'


class Aglibraryiptc(models.Model):
    id_local = models.IntegerField(primary_key=True, null=False)
    caption = models.TextField(blank=True, null=True)  # This field type is a guess.
    copyright = models.TextField(blank=True, null=True)  # This field type is a guess.
    image = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'AgLibraryIPTC'


class Aglibraryimagechangecounter(models.Model):
    image = models.TextField(primary_key=True, null=False)  # This field type is a guess.
    changecounter = models.TextField(db_column='changeCounter', blank=True, null=True)  # Field name made lowercase. This field type is a guess.
    changedattime = models.TextField(db_column='changedAtTime', blank=True, null=True)  # Field name made lowercase. This field type is a guess.
    localtimeoffsetsecs = models.TextField(db_column='localTimeOffsetSecs', blank=True, null=True)  # Field name made lowercase. This field type is a guess.

    class Meta:
        managed = False
        db_table = 'AgLibraryImageChangeCounter'


class Aglibraryimageozassetids(models.Model):
    image = models.TextField()  # This field type is a guess.
    ozcatalogid = models.TextField(db_column='ozCatalogId')  # Field name made lowercase. This field type is a guess.
    ozassetid = models.TextField(db_column='ozAssetId', blank=True, null=True)  # Field name made lowercase. This field type is a guess.
    ownedbycatalog = models.TextField(db_column='ownedByCatalog', blank=True, null=True)  # Field name made lowercase. This field type is a guess.

    class Meta:
        managed = False
        db_table = 'AgLibraryImageOzAssetIds'
        unique_together = (('image', 'ozcatalogid'),)


class Aglibraryimagesearchdata(models.Model):
    id_local = models.IntegerField(primary_key=True, null=False)
    featinfo = models.TextField(db_column='featInfo', blank=True, null=True)  # Field name made lowercase. This field type is a guess.
    height = models.TextField(blank=True, null=True)  # This field type is a guess.
    iddesc = models.TextField(db_column='idDesc', blank=True, null=True)  # Field name made lowercase. This field type is a guess.
    iddescch = models.TextField(db_column='idDescCh', blank=True, null=True)  # Field name made lowercase. This field type is a guess.
    image = models.IntegerField()
    width = models.TextField(blank=True, null=True)  # This field type is a guess.

    class Meta:
        managed = False
        db_table = 'AgLibraryImageSearchData'


class Aglibraryimagesyncedassetdata(models.Model):
    image = models.TextField()  # This field type is a guess.
    payloadkey = models.TextField(db_column='payloadKey')  # Field name made lowercase. This field type is a guess.
    payloaddata = models.TextField(db_column='payloadData')  # Field name made lowercase. This field type is a guess.

    class Meta:
        managed = False
        db_table = 'AgLibraryImageSyncedAssetData'
        unique_together = (('image', 'payloadkey'),)


class Aglibraryimagexmpupdater(models.Model):
    id_local = models.IntegerField(primary_key=True, null=False)
    taskid = models.TextField(db_column='taskID', unique=True)  # Field name made lowercase. This field type is a guess.
    taskstatus = models.TextField(db_column='taskStatus')  # Field name made lowercase. This field type is a guess.
    whenposted = models.TextField(db_column='whenPosted')  # Field name made lowercase. This field type is a guess.

    class Meta:
        managed = False
        db_table = 'AgLibraryImageXMPUpdater'


class Aglibraryimport(models.Model):
    id_local = models.IntegerField(primary_key=True, null=False)
    imagecount = models.TextField(db_column='imageCount', blank=True, null=True)  # Field name made lowercase. This field type is a guess.
    importdate = models.TextField(db_column='importDate')  # Field name made lowercase. This field type is a guess.
    name = models.TextField(blank=True, null=True)  # This field type is a guess.

    class Meta:
        managed = False
        db_table = 'AgLibraryImport'


class Aglibraryimportimage(models.Model):
    id_local = models.IntegerField(primary_key=True, null=False)
    image = models.IntegerField()
    import_field = models.IntegerField(db_column='import')  # Field renamed because it was a Python reserved word.

    class Meta:
        managed = False
        db_table = 'AgLibraryImportImage'
        unique_together = (('image', 'import_field'),)


class Aglibrarykeyword(models.Model):
    id_local = models.IntegerField(primary_key=True, null=False)
    id_global = models.TextField(unique=True)  # This field type is a guess.
    datecreated = models.TextField(db_column='dateCreated')  # Field name made lowercase. This field type is a guess.
    genealogy = models.TextField()  # This field type is a guess.
    imagecountcache = models.TextField(db_column='imageCountCache', blank=True, null=True)  # Field name made lowercase. This field type is a guess.
    includeonexport = models.IntegerField(db_column='includeOnExport')  # Field name made lowercase.
    includeparents = models.IntegerField(db_column='includeParents')  # Field name made lowercase.
    includesynonyms = models.IntegerField(db_column='includeSynonyms')  # Field name made lowercase.
    keywordtype = models.TextField(db_column='keywordType', blank=True, null=True)  # Field name made lowercase. This field type is a guess.
    lastapplied = models.TextField(db_column='lastApplied', blank=True, null=True)  # Field name made lowercase. This field type is a guess.
    lc_name = models.TextField(blank=True, null=True)  # This field type is a guess.
    name = models.TextField(blank=True, null=True)  # This field type is a guess.
    parent = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'AgLibraryKeyword'


class Aglibrarykeywordcooccurrence(models.Model):
    id_local = models.IntegerField(primary_key=True, null=False)
    tag1 = models.TextField()  # This field type is a guess.
    tag2 = models.TextField()  # This field type is a guess.
    value = models.TextField()  # This field type is a guess.

    class Meta:
        managed = False
        db_table = 'AgLibraryKeywordCooccurrence'


class Aglibrarykeywordface(models.Model):
    id_local = models.IntegerField(primary_key=True, null=False)
    face = models.IntegerField()
    keyface = models.IntegerField(db_column='keyFace', blank=True, null=True)  # Field name made lowercase.
    rankorder = models.TextField(db_column='rankOrder', blank=True, null=True)  # Field name made lowercase. This field type is a guess.
    tag = models.IntegerField()
    userpick = models.IntegerField(db_column='userPick', blank=True, null=True)  # Field name made lowercase.
    userreject = models.IntegerField(db_column='userReject', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'AgLibraryKeywordFace'


class Aglibrarykeywordimage(models.Model):
    id_local = models.IntegerField(primary_key=True, null=False)
    image = models.IntegerField()
    tag = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'AgLibraryKeywordImage'


class Aglibrarykeywordpopularity(models.Model):
    id_local = models.IntegerField(primary_key=True, null=False)
    occurrences = models.TextField()  # This field type is a guess.
    popularity = models.TextField()  # This field type is a guess.
    tag = models.TextField(unique=True)  # This field type is a guess.

    class Meta:
        managed = False
        db_table = 'AgLibraryKeywordPopularity'


class Aglibrarykeywordsynonym(models.Model):
    id_local = models.IntegerField(primary_key=True, null=False)
    keyword = models.IntegerField()
    lc_name = models.TextField(blank=True, null=True)  # This field type is a guess.
    name = models.TextField(blank=True, null=True)  # This field type is a guess.

    class Meta:
        managed = False
        db_table = 'AgLibraryKeywordSynonym'


class Aglibraryozcommentids(models.Model):
    ozcatalogid = models.TextField(db_column='ozCatalogId')  # Field name made lowercase. This field type is a guess.
    ozspaceid = models.TextField(db_column='ozSpaceId')  # Field name made lowercase. This field type is a guess.
    ozassetid = models.TextField(db_column='ozAssetId')  # Field name made lowercase. This field type is a guess.
    ozcommentid = models.TextField(db_column='ozCommentId')  # Field name made lowercase. This field type is a guess.
    timestamp = models.TextField()  # This field type is a guess.

    class Meta:
        managed = False
        db_table = 'AgLibraryOzCommentIds'
        unique_together = (('ozcatalogid', 'ozcommentid'),)


class Aglibraryozfavoriteids(models.Model):
    ozcatalogid = models.TextField(db_column='ozCatalogId')  # Field name made lowercase. This field type is a guess.
    ozspaceid = models.TextField(db_column='ozSpaceId')  # Field name made lowercase. This field type is a guess.
    ozassetid = models.TextField(db_column='ozAssetId')  # Field name made lowercase. This field type is a guess.
    ozfavoriteid = models.TextField(db_column='ozFavoriteId')  # Field name made lowercase. This field type is a guess.
    timestamp = models.TextField()  # This field type is a guess.

    class Meta:
        managed = False
        db_table = 'AgLibraryOzFavoriteIds'
        unique_together = (('ozcatalogid', 'ozfavoriteid'),)


class Aglibraryozfeedbackinfo(models.Model):
    id_local = models.IntegerField(primary_key=True, null=False)
    image = models.TextField()  # This field type is a guess.
    lastfeedbacktime = models.TextField(db_column='lastFeedbackTime', blank=True, null=True)  # Field name made lowercase. This field type is a guess.
    lastreadtime = models.TextField(db_column='lastReadTime', blank=True, null=True)  # Field name made lowercase. This field type is a guess.
    newcommentcount = models.TextField(db_column='newCommentCount')  # Field name made lowercase. This field type is a guess.
    newfavoritecount = models.TextField(db_column='newFavoriteCount')  # Field name made lowercase. This field type is a guess.
    ozassetid = models.TextField(db_column='ozAssetId')  # Field name made lowercase. This field type is a guess.
    ozcatalogid = models.TextField(db_column='ozCatalogId')  # Field name made lowercase. This field type is a guess.
    ozspaceid = models.TextField(db_column='ozSpaceId')  # Field name made lowercase. This field type is a guess.

    class Meta:
        managed = False
        db_table = 'AgLibraryOzFeedbackInfo'
        unique_together = (('ozassetid', 'ozspaceid', 'ozcatalogid'),)


class Aglibrarypublishedcollection(models.Model):
    id_local = models.IntegerField(primary_key=True, null=False)
    creationid = models.TextField(db_column='creationId')  # Field name made lowercase. This field type is a guess.
    genealogy = models.TextField()  # This field type is a guess.
    imagecount = models.TextField(db_column='imageCount', blank=True, null=True)  # Field name made lowercase. This field type is a guess.
    isdefaultcollection = models.TextField(db_column='isDefaultCollection', blank=True, null=True)  # Field name made lowercase. This field type is a guess.
    name = models.TextField()  # This field type is a guess.
    parent = models.IntegerField(blank=True, null=True)
    publishedurl = models.TextField(db_column='publishedUrl', blank=True, null=True)  # Field name made lowercase. This field type is a guess.
    remotecollectionid = models.TextField(db_column='remoteCollectionId', blank=True, null=True)  # Field name made lowercase. This field type is a guess.
    systemonly = models.TextField(db_column='systemOnly')  # Field name made lowercase. This field type is a guess.

    class Meta:
        managed = False
        db_table = 'AgLibraryPublishedCollection'


class Aglibrarypublishedcollectioncontent(models.Model):
    id_local = models.IntegerField(primary_key=True, null=False)
    collection = models.IntegerField()
    content = models.TextField(blank=True, null=True)  # This field type is a guess.
    owningmodule = models.TextField(db_column='owningModule', blank=True, null=True)  # Field name made lowercase. This field type is a guess.

    class Meta:
        managed = False
        db_table = 'AgLibraryPublishedCollectionContent'


class Aglibrarypublishedcollectionimage(models.Model):
    id_local = models.IntegerField(primary_key=True, null=False)
    collection = models.IntegerField()
    image = models.IntegerField()
    pick = models.TextField()  # This field type is a guess.
    positionincollection = models.TextField(db_column='positionInCollection', blank=True, null=True)  # Field name made lowercase. This field type is a guess.

    class Meta:
        managed = False
        db_table = 'AgLibraryPublishedCollectionImage'


class Aglibraryrootfolder(models.Model):
    id_local = models.IntegerField(primary_key=True, null=False)
    id_global = models.TextField(unique=True)  # This field type is a guess.
    absolutepath = models.TextField(db_column='absolutePath', unique=True)  # Field name made lowercase. This field type is a guess.
    name = models.TextField()  # This field type is a guess.
    relativepathfromcatalog = models.TextField(db_column='relativePathFromCatalog', blank=True, null=True)  # Field name made lowercase. This field type is a guess.

    class Meta:
        managed = False
        db_table = 'AgLibraryRootFolder'


class Aglibraryupdatedimages(models.Model):
    image = models.IntegerField(primary_key=True, null=False)

    class Meta:
        managed = False
        db_table = 'AgLibraryUpdatedImages'


class Agmrulists(models.Model):
    id_local = models.IntegerField(primary_key=True, null=False)
    listid = models.TextField(db_column='listID')  # Field name made lowercase. This field type is a guess.
    timestamp = models.TextField()  # This field type is a guess.
    value = models.TextField()  # This field type is a guess.

    class Meta:
        managed = False
        db_table = 'AgMRULists'


class Agmetadatasearchindex(models.Model):
    id_local = models.IntegerField(primary_key=True, null=False)
    exifsearchindex = models.TextField(db_column='exifSearchIndex')  # Field name made lowercase. This field type is a guess.
    image = models.IntegerField(blank=True, null=True)
    iptcsearchindex = models.TextField(db_column='iptcSearchIndex')  # Field name made lowercase. This field type is a guess.
    othersearchindex = models.TextField(db_column='otherSearchIndex')  # Field name made lowercase. This field type is a guess.
    searchindex = models.TextField(db_column='searchIndex')  # Field name made lowercase. This field type is a guess.

    class Meta:
        managed = False
        db_table = 'AgMetadataSearchIndex'


class Agoutputimageasset(models.Model):
    id_local = models.IntegerField(primary_key=True, null=False)
    assetid = models.TextField(db_column='assetId')  # Field name made lowercase. This field type is a guess.
    collection = models.IntegerField()
    image = models.IntegerField()
    moduleid = models.TextField(db_column='moduleId')  # Field name made lowercase. This field type is a guess.

    class Meta:
        managed = False
        db_table = 'AgOutputImageAsset'


class Agozspacealbumids(models.Model):
    ozcatalogid = models.TextField(db_column='ozCatalogId')  # Field name made lowercase. This field type is a guess.
    ozalbumid = models.TextField(db_column='ozAlbumId')  # Field name made lowercase. This field type is a guess.
    ozspaceid = models.TextField(db_column='ozSpaceId')  # Field name made lowercase. This field type is a guess.
    ozspacealbumid = models.TextField(db_column='ozSpaceAlbumId', unique=True)  # Field name made lowercase. This field type is a guess.

    class Meta:
        managed = False
        db_table = 'AgOzSpaceAlbumIds'


class Agozspaceids(models.Model):
    ozcatalogid = models.TextField(db_column='ozCatalogId')  # Field name made lowercase. This field type is a guess.
    ozspaceid = models.TextField(db_column='ozSpaceId')  # Field name made lowercase. This field type is a guess.

    class Meta:
        managed = False
        db_table = 'AgOzSpaceIds'
        unique_together = (('ozcatalogid', 'ozspaceid'),)


class Agpendingozalbumassetids(models.Model):
    ozcatalogid = models.TextField(db_column='ozCatalogId')  # Field name made lowercase. This field type is a guess.
    ozalbumassetid = models.TextField(db_column='ozAlbumAssetId')  # Field name made lowercase. This field type is a guess.
    ozassetid = models.TextField(db_column='ozAssetId')  # Field name made lowercase. This field type is a guess.
    ozalbumid = models.TextField(db_column='ozAlbumId')  # Field name made lowercase. This field type is a guess.
    ozsortorder = models.TextField(db_column='ozSortOrder', blank=True, null=True)  # Field name made lowercase. This field type is a guess.
    oziscover = models.TextField(db_column='ozIsCover', blank=True, null=True)  # Field name made lowercase. This field type is a guess.

    class Meta:
        managed = False
        db_table = 'AgPendingOzAlbumAssetIds'
        unique_together = (('ozcatalogid', 'ozalbumassetid', 'ozassetid', 'ozalbumid'),)


class Agpendingozassetbinarydownloads(models.Model):
    ozassetid = models.TextField(db_column='ozAssetId')  # Field name made lowercase. This field type is a guess.
    ozcatalogid = models.TextField(db_column='ozCatalogId')  # Field name made lowercase. This field type is a guess.
    whenqueued = models.TextField(db_column='whenQueued')  # Field name made lowercase. This field type is a guess.
    path = models.TextField()  # This field type is a guess.
    state = models.TextField(blank=True, null=True)  # This field type is a guess.

    class Meta:
        managed = False
        db_table = 'AgPendingOzAssetBinaryDownloads'
        unique_together = (('ozassetid', 'ozcatalogid'),)


class Agpendingozassets(models.Model):
    ozassetid = models.TextField(db_column='ozAssetId')  # Field name made lowercase. This field type is a guess.
    ozcatalogid = models.TextField(db_column='ozCatalogId')  # Field name made lowercase. This field type is a guess.
    state = models.TextField(blank=True, null=True)  # This field type is a guess.
    path = models.TextField()  # This field type is a guess.
    payload = models.TextField()  # This field type is a guess.

    class Meta:
        managed = False
        db_table = 'AgPendingOzAssets'
        unique_together = (('ozassetid', 'ozcatalogid'),)


class Agphotocomment(models.Model):
    id_local = models.IntegerField(primary_key=True, null=False)
    id_global = models.TextField(unique=True)  # This field type is a guess.
    comment = models.TextField(blank=True, null=True)  # This field type is a guess.
    commentrealname = models.TextField(db_column='commentRealname', blank=True, null=True)  # Field name made lowercase. This field type is a guess.
    commentusername = models.TextField(db_column='commentUsername', blank=True, null=True)  # Field name made lowercase. This field type is a guess.
    datecreated = models.TextField(db_column='dateCreated', blank=True, null=True)  # Field name made lowercase. This field type is a guess.
    photo = models.IntegerField()
    remoteid = models.TextField(db_column='remoteId')  # Field name made lowercase. This field type is a guess.
    remotephoto = models.IntegerField(db_column='remotePhoto', blank=True, null=True)  # Field name made lowercase.
    url = models.TextField(blank=True, null=True)  # This field type is a guess.

    class Meta:
        managed = False
        db_table = 'AgPhotoComment'


class Agphotoproperty(models.Model):
    id_local = models.IntegerField(primary_key=True, null=False)
    id_global = models.TextField(unique=True)  # This field type is a guess.
    datatype = models.TextField(db_column='dataType', blank=True, null=True)  # Field name made lowercase. This field type is a guess.
    internalvalue = models.TextField(db_column='internalValue', blank=True, null=True)  # Field name made lowercase. This field type is a guess.
    photo = models.IntegerField()
    propertyspec = models.IntegerField(db_column='propertySpec')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'AgPhotoProperty'
        unique_together = (('photo', 'propertyspec'),)


class Agphotopropertyarrayelement(models.Model):
    id_local = models.IntegerField(primary_key=True, null=False)
    id_global = models.TextField(unique=True)  # This field type is a guess.
    arrayindex = models.TextField(db_column='arrayIndex')  # Field name made lowercase. This field type is a guess.
    datatype = models.TextField(db_column='dataType', blank=True, null=True)  # Field name made lowercase. This field type is a guess.
    internalvalue = models.TextField(db_column='internalValue', blank=True, null=True)  # Field name made lowercase. This field type is a guess.
    photo = models.IntegerField()
    propertyspec = models.IntegerField(db_column='propertySpec')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'AgPhotoPropertyArrayElement'
        unique_together = (('photo', 'propertyspec', 'arrayindex'),)


class Agphotopropertyspec(models.Model):
    id_local = models.IntegerField(primary_key=True, null=False)
    id_global = models.TextField(unique=True)  # This field type is a guess.
    flattenedattributes = models.TextField(db_column='flattenedAttributes', blank=True, null=True)  # Field name made lowercase. This field type is a guess.
    key = models.TextField()  # This field type is a guess.
    pluginversion = models.TextField(db_column='pluginVersion')  # Field name made lowercase. This field type is a guess.
    sourceplugin = models.TextField(db_column='sourcePlugin')  # Field name made lowercase. This field type is a guess.
    uservisiblename = models.TextField(db_column='userVisibleName', blank=True, null=True)  # Field name made lowercase. This field type is a guess.

    class Meta:
        managed = False
        db_table = 'AgPhotoPropertySpec'
        unique_together = (('sourceplugin', 'key', 'pluginversion'),)


class Agpublishlistenerworklist(models.Model):
    id_local = models.IntegerField(primary_key=True, null=False)
    taskid = models.TextField(db_column='taskID', unique=True)  # Field name made lowercase. This field type is a guess.
    taskstatus = models.TextField(db_column='taskStatus')  # Field name made lowercase. This field type is a guess.
    whenposted = models.TextField(db_column='whenPosted')  # Field name made lowercase. This field type is a guess.

    class Meta:
        managed = False
        db_table = 'AgPublishListenerWorklist'


class Agremotephoto(models.Model):
    id_local = models.IntegerField(primary_key=True, null=False)
    id_global = models.TextField(unique=True)  # This field type is a guess.
    collection = models.IntegerField()
    commentcount = models.TextField(db_column='commentCount', blank=True, null=True)  # Field name made lowercase. This field type is a guess.
    developsettingsdigest = models.TextField(db_column='developSettingsDigest', blank=True, null=True)  # Field name made lowercase. This field type is a guess.
    filecontentshash = models.TextField(db_column='fileContentsHash', blank=True, null=True)  # Field name made lowercase. This field type is a guess.
    filemodtimestamp = models.TextField(db_column='fileModTimestamp', blank=True, null=True)  # Field name made lowercase. This field type is a guess.
    metadatadigest = models.TextField(db_column='metadataDigest', blank=True, null=True)  # Field name made lowercase. This field type is a guess.
    mostrecentcommenttime = models.TextField(db_column='mostRecentCommentTime', blank=True, null=True)  # Field name made lowercase. This field type is a guess.
    orientation = models.TextField(blank=True, null=True)  # This field type is a guess.
    photo = models.IntegerField()
    photoneedsupdating = models.TextField(db_column='photoNeedsUpdating', blank=True, null=True)  # Field name made lowercase. This field type is a guess.
    publishcount = models.TextField(db_column='publishCount', blank=True, null=True)  # Field name made lowercase. This field type is a guess.
    remoteid = models.TextField(db_column='remoteId', blank=True, null=True)  # Field name made lowercase. This field type is a guess.
    serviceaggregaterating = models.TextField(db_column='serviceAggregateRating', blank=True, null=True)  # Field name made lowercase. This field type is a guess.
    url = models.TextField(blank=True, null=True)  # This field type is a guess.

    class Meta:
        managed = False
        db_table = 'AgRemotePhoto'
        unique_together = (('collection', 'remoteid'), ('collection', 'photo'),)


class Agsearchablephotoproperty(models.Model):
    id_local = models.IntegerField(primary_key=True, null=False)
    id_global = models.TextField(unique=True)  # This field type is a guess.
    datatype = models.TextField(db_column='dataType', blank=True, null=True)  # Field name made lowercase. This field type is a guess.
    internalvalue = models.TextField(db_column='internalValue', blank=True, null=True)  # Field name made lowercase. This field type is a guess.
    lc_idx_internalvalue = models.TextField(db_column='lc_idx_internalValue', blank=True, null=True)  # Field name made lowercase. This field type is a guess.
    photo = models.IntegerField()
    propertyspec = models.IntegerField(db_column='propertySpec')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'AgSearchablePhotoProperty'
        unique_together = (('photo', 'propertyspec'),)


class Agsearchablephotopropertyarrayelement(models.Model):
    id_local = models.IntegerField(primary_key=True, null=False)
    id_global = models.TextField(unique=True)  # This field type is a guess.
    arrayindex = models.TextField(db_column='arrayIndex')  # Field name made lowercase. This field type is a guess.
    datatype = models.TextField(db_column='dataType', blank=True, null=True)  # Field name made lowercase. This field type is a guess.
    internalvalue = models.TextField(db_column='internalValue', blank=True, null=True)  # Field name made lowercase. This field type is a guess.
    lc_idx_internalvalue = models.TextField(db_column='lc_idx_internalValue', blank=True, null=True)  # Field name made lowercase. This field type is a guess.
    photo = models.IntegerField()
    propertyspec = models.IntegerField(db_column='propertySpec')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'AgSearchablePhotoPropertyArrayElement'
        unique_together = (('photo', 'propertyspec', 'arrayindex'),)


class Agsourcecolorprofileconstants(models.Model):
    id_local = models.IntegerField(primary_key=True, null=False)
    image = models.IntegerField()
    profilename = models.TextField(db_column='profileName')  # Field name made lowercase. This field type is a guess.

    class Meta:
        managed = False
        db_table = 'AgSourceColorProfileConstants'


class Agspecialsourcecontent(models.Model):
    id_local = models.IntegerField(primary_key=True, null=False)
    content = models.TextField(blank=True, null=True)  # This field type is a guess.
    owningmodule = models.TextField(db_column='owningModule', blank=True, null=True)  # Field name made lowercase. This field type is a guess.
    source = models.TextField()  # This field type is a guess.

    class Meta:
        managed = False
        db_table = 'AgSpecialSourceContent'
        unique_together = (('source', 'owningmodule'),)


class Agtempimages(models.Model):
    image = models.IntegerField(primary_key=True, null=False)

    class Meta:
        managed = False
        db_table = 'AgTempImages'


class Agvideoinfo(models.Model):
    id_local = models.IntegerField(primary_key=True, null=False)
    duration = models.TextField(blank=True, null=True)  # This field type is a guess.
    frame_rate = models.TextField(blank=True, null=True)  # This field type is a guess.
    has_audio = models.IntegerField()
    has_video = models.IntegerField()
    image = models.IntegerField()
    poster_frame = models.TextField()  # This field type is a guess.
    poster_frame_set_by_user = models.IntegerField()
    trim_end = models.TextField()  # This field type is a guess.
    trim_start = models.TextField()  # This field type is a guess.

    class Meta:
        managed = False
        db_table = 'AgVideoInfo'


class Lrmobilesyncchangecounter(models.Model):
    id = models.TextField(primary_key=True, null=False)  # This field type is a guess.
    changecounter = models.TextField(db_column='changeCounter')  # Field name made lowercase. This field type is a guess.

    class Meta:
        managed = False
        db_table = 'LrMobileSyncChangeCounter'


class SqliteStat1(models.Model):
    tbl = models.TextField(blank=True, null=True)  # This field type is a guess.
    idx = models.TextField(blank=True, null=True)  # This field type is a guess.
    stat = models.TextField(blank=True, null=True)  # This field type is a guess.

    class Meta:
        managed = False
        db_table = 'sqlite_stat1'
