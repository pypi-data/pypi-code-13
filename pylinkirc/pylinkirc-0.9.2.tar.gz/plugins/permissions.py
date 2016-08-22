"""
permissions.py: Allows you to manage permissions for commands.
"""
import pickle
import collections
import threading

from pylinkirc import utils, conf, world
from pylinkirc.log import log

### Databasing portion
dbname = utils.getDatabaseName('permissions')
db = collections.defaultdict(set)
exportdb_timer = None

save_delay = conf.conf['bot'].get('save_delay', 300)

def loadDB():
    """Loads the Permissions database, silently creating a new one if this fails."""
    global db
    try:
        with open(dbname, "rb") as f:
            db.update(pickle.load(f))
    except (ValueError, IOError, OSError):
        log.info("Permissions: failed to load links database %s; creating a new one in "
                 "memory.", dbname)

def exportDB():
    """Exports the automode database."""

    log.debug("Permissions: exporting database to %s.", dbname)
    with open(dbname, 'wb') as f:
        pickle.dump(db, f, protocol=4)

def scheduleExport(starting=False):
    """
    Schedules exporting of the Permissions database in a repeated loop.
    """
    global exportdb_timer

    if not starting:
        # Export the database, unless this is being called the first
        # thing after start (i.e. DB has just been loaded).
        exportDB()

    exportdb_timer = threading.Timer(save_delay, scheduleExport)
    exportdb_timer.name = 'Permissions exportDB Loop'
    exportdb_timer.start()

def die(sourceirc):
    """Saves the Permissions database and quit."""
    exportDB()

    # Kill the scheduling for exports.
    global exportdb_timer
    if exportdb_timer:
        log.debug("Permissions: cancelling exportDB timer thread %s due to die()", threading.get_ident())
        exportdb_timer.cancel()

### A magical permissions handler
def permissions_core(irc, uid):


### Commands
@utils.add_cmd
def addperm(irc, source, args):
    """<mask> <space separated perm list>

    Adds permissions to hostmasks or exttargets. Permissions normally take the form "pluginname.commandname".

    Examples:
    ADDPERM $oper opercmds.kick
    """
    irc.checkAuthenticated(source, allowOper=False)
    try:
        mask = args[0]
        perms = map(irc.toLower, args[1:])
        assert perms
    except (AssertionError, IndexError):
        irc.reply("Error: Invalid arguments given. Needs 2: mask, permissions list.")
        return

    db[mask] |= set(perms)
    irc.reply("Done. Added permissions for \x02%s\x02." % mask)

@utils.add_cmd
def delperm(irc, source, args):
    """<mask> <space separated perm list>

    Removes permissions to hostmasks or exttargets. Permissions normally take the form "pluginname.commandname".

    Examples:
    DELPERM $oper opercmds.kick
    """
    irc.checkAuthenticated(source, allowOper=False)
    try:
        mask = args[0]
        perms = map(irc.toLower, args[1:])
        assert perms
    except (AssertionError, IndexError):
        irc.reply("Error: Invalid arguments given. Needs 2: mask, permissions list.")
        return

    db[mask] -= set(perms)
    irc.reply("Done. Removed permissions for \x02%s\x02." % mask)

@utils.add_cmd
def listperms(irc, source, args):
    """<mask> <space separated perm list>

    Lists permissions assigned to the given hostmask or target. Permissions normally take the form "pluginname.commandname".

    Examples:
    DELPERM $oper opercmds.kick
    """
    irc.checkAuthenticated(source, allowOper=False)
    try:
        mask = args[0]
    except IndexError:
        irc.reply("Error: Invalid arguments given. Needs 1: mask.")
        return

    # This replies in private to prevent command flood.
    irc.reply("Permissions for \x02%s\x02:" % mask, private=True)
    for perm in db[mask]:
        irc.reply("    %s" % perm, private=True)

@utils.add_cmd
def save(irc, source, args):
    """takes no arguments.

    Saves the relay database to disk."""
    irc.checkAuthenticated(source)
    exportDB()
    irc.reply('Done. Saved Permissions database.')
