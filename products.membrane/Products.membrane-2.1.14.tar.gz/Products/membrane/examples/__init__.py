
from Products.CMFCore.utils import ContentInit
from Products.CMFCore.permissions import (
    AddPortalContent as ADD_CONTENT_PERMISSION)

from Products.Archetypes import process_types
from Products.Archetypes.public import listTypes

from Products.membrane.config import PROJECTNAME
from Products.membrane.examples import simplemember
from Products.membrane.examples import simplegroup

simplemember, simplegroup       # make pyflakes happy


def initialize(context):

    content_types, constructors, ftis = process_types(
        listTypes(PROJECTNAME), PROJECTNAME)

    ContentInit(
        PROJECTNAME + ' Content',
        content_types=content_types,
        permission=ADD_CONTENT_PERMISSION,
        extra_constructors=constructors,
        fti=ftis,
    ).initialize(context)
