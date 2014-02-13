# This file is part of LiSE, a framework for life simulation games.
# Copyright (c) 2013 Zachary Spector,  zacharyspector@gmail.com
from math import pi, sqrt
from re import match, compile, findall


"""Common utility functions and data structures.

The most important are Skeleton, a mapping used to store and maintain
all game data; and SaveableMetaclass, which generates
SQL from metadata declared as class atttributes.

"""

### Constants

SHEET_ITEM_TYPES = [
    'thing_tab',
    'place_tab',
    'portal_tab',
    'char_tab',
    'thing_cal',
    'place_cal',
    'portal_cal',
    'char_cal']


TABLE_TYPES = [
    'thing_tab',
    'place_tab',
    'portal_tab',
    'char_tab']


CALENDAR_TYPES = [
    'thing_cal',
    'place_cal',
    'portal_cal',
    'char_cal']

unicode2pytype = {
    'bool': bool,
    'boolean': bool,
    'int': int,
    'integer': int,
    'float': float,
    'str': unicode,
    'unicode': unicode,
    'text': unicode}

pytype2unicode = {
    bool: 'bool',
    int: 'int',
    float: 'float',
    unicode: 'unicode',
    str: 'unicode'}

ninety = pi / 2
"""pi / 2"""

fortyfive = pi / 4
"""pi / 4"""

phi = (1.0 + sqrt(5))/2.0
"""The golden ratio."""

portex = compile("Portal\((.+?)->(.+?)\)")
"""Regular expression to recognize portals by name"""

###
# These regexes serve to parse certain database records that represent
# function calls.
#
# Mainly, that means menu items and Effects.
###
ONE_ARG_RE = compile("(.+)")
TWO_ARG_RE = compile("(.+), ?(.+)")
ITEM_ARG_RE = compile("(.+)\.(.+)")
MAKE_SPOT_ARG_RE = compile(
    "(.+)\."
    "(.+),([0-9]+),([0-9]+),?(.*)")
MAKE_PORTAL_ARG_RE = compile(
    "(.+)\.(.+)->"
    "(.+)\.(.+)")
MAKE_THING_ARG_RE = compile(
    "(.+)\.(.+)@(.+)")
PORTAL_NAME_RE = compile(
    "Portal\((.+)->(.+)\)")
NEW_THING_RE = compile(
    "new_thing\((.+)+\)")
NEW_PLACE_RE = compile(
    "new_place\((.+)\)")
CHARACTER_RE = compile(
    "character\((.+)\)")

### End constants
### Begin functions


def passthru(_):
    return _


def upbranch(closet, bones, branch, tick):
    started = False
    first = None
    for bone in bones:
        if bone.tick >= tick:
            started = True
            yield bone._replace(branch=branch)
        if not started:
            assert(bone.tick < tick)
            first = bone
    if first is not None:
        yield first._replace(
            branch=branch, tick=tick)


def selectif(skel, key):
    if key is None:
        for sk in skel.itervalues():
            yield sk
    else:
        try:
            yield skel[key]
        except (KeyError, IndexError):
            return

### End functions


class TimestreamException(Exception):
    """Used for time travel related errors that are nothing to do with
continuity."""
    pass


class TimeParadox(Exception):
    """I tried to record some fact at some time, and in so doing,
    contradicted the historical record."""
    pass


class JourneyException(Exception):
    """There was a problem with pathfinding."""
    pass


class KnowledgeException(Exception):
    """I tried to access some information that I was not permitted access to.

    Should be treated like KeyError most of the time. For the purposes
    of the simulation, not having information is the same as
    information not existing. But there may be circumstances where
    they differ for programming purposes.

    """
    pass


class ListItemIterator:
    """Iterate over a list in a way that resembles dict.iteritems()"""
    def __init__(self, l):
        """Initialize for list l"""
        self.l = l
        self.l_iter = iter(l)
        self.i = 0

    def __iter__(self):
        """I'm an iterator"""
        return self

    def __len__(self):
        """Provide the length of the underlying list."""
        return len(self.l)

    def __next__(self):
        """Return a tuple of the current index and its item in the list"""
        it = next(self.l_iter)
        i = self.i
        self.i += 1
        return (i, it)

    def next(self):
        """Return a tuple of the current index and its item in the list"""
        return self.__next__()


class Fabulator(object):
    """Construct objects (or call functions, as you please) as described
    by strings loaded in from the database.

    This doesn't use exec(). You need to supply the functions when you
    construct the Fabulator.

    """
    def __init__(self, fabs):
        """Supply a dictionary full of callables, keyed by the names you want
        to use for them.

        """
        self.fabbers = fabs

    def __call__(self, s):
        """Parse the string into something I can make a callable from. Then
        make it, using the classes in self.fabbers.

        """
        def _call_recursively(inner, outer):
            fun = self.fabbers[outer]
            # pretty sure parentheses are meaningless inside []
            m = findall("(.+)\((.+)\)[,)] *", inner)
            if len(m) == 0:
                return fun(*inner.split(",").strip(" "))
            elif len(m) == 1:
                (infun, inarg) = m[0]
                infun = self.fabbers[infun]
                inargs = inarg.split(",").strip(" ")
                return fun(infun(*inargs))
            else:
                # This doesn't allow any mixing of function-call arguments
                # with text arguments at the same level. Not optimal.
                return fun(*[self._call_recursively(infun, inarg)
                             for (infun, inarg) in m])
        (outer, inner) = match("(.+)\((.+)\)", s).groups()
        return _call_recursively(outer, inner)


class HandleHandler(object):
    def mk_handles(self, *names):
        for name in names:
            self.mk_handle(name)

    def mk_handle(self, name):
        def register_listener(llist, listener):
            if listener not in llist:
                llist.append(listener)

        def registrar(llist):
            return lambda listener: register_listener(llist, listener)

        def unregister_listener(llist, listener):
            while listener in llist:
                llist.remove(listener)

        def unregistrar(llist):
            return lambda listener: unregister_listener(llist, listener)

        llist = []
        setattr(self, '{}_listeners'.format(name), llist)
        setattr(self, 'register_{}_listener'.format(name),
                registrar(llist))
        setattr(self, 'unregister_{}_listener'.format(name),
                unregistrar(llist))
