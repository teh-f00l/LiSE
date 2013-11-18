# This file is part of LiSE, a framework for life simulation games.
# Copyright (c) 2013 Zachary Spector,  zacharyspector@gmail.com
from __future__ import print_function
from kivybits import SaveableWidgetMetaclass
from pawn import Pawn
from spot import Spot
from arrow import Arrow
from kivy.properties import (
    DictProperty,
    NumericProperty,
    ObjectProperty)
from kivy.uix.scrollview import ScrollView
from kivy.uix.relativelayout import RelativeLayout
from kivy.uix.image import Image


"""Class for user's view on gameworld, and support functions."""


class Board(ScrollView):
    __metaclass__ = SaveableWidgetMetaclass
    tables = [(
        "board",
        {"dimension": "text not null default 'Physical'",
         "wallpaper": "text not null default 'default_wallpaper'",
         "x": "float not null default 0.0",
         "y": "float not null default 0.0"},
        ("dimension",),
        {"wallpaper": ("img", "name")},
        ["x>=0", "y>=0", "x<=1", "y<=1"])]
    arrow_width = 1.4
    arrowhead_size = 10
    auto_bring_to_front = False
    closet = ObjectProperty()
    dimension = ObjectProperty()
    spotdict = DictProperty({})
    pawndict = DictProperty({})
    arrowdict = DictProperty({})
    rowdict = DictProperty({})
    offx = NumericProperty(0)
    offy = NumericProperty(0)
    wallwidth = NumericProperty(0)
    wallheight = NumericProperty(0)
    dragging = ObjectProperty(None, allownone=True)

    def __init__(self, **kwargs):
        if kwargs["dimension"].__class__ in (str, unicode):
            kwargs["dimension"] = kwargs["closet"].get_dimension(
                kwargs["dimension"])
        ScrollView.__init__(self, scroll_y=0, **kwargs)
        self.last_touch = None
        self.closet.boarddict[unicode(self.dimension)] = self
        self.upd_rowdict()
        self.closet.skeleton["board"][unicode(
            self.dimension)].listener = self.upd_rowdict
        tex = self.get_texture()
        (self.wallwidth, self.wallheight) = tex.size
        content = RelativeLayout(size_hint=(None, None), size=tex.size)
        content.add_widget(Image(pos=(0, 0), texture=tex, size=tex.size))
        self.add_widget(content)
        if (
                "spot_coords" in self.closet.skeleton and
                unicode(self.dimension) in self.dimension.closet.skeleton[
                    "spot_coords"]):
            for rd in self.dimension.closet.skeleton[
                    "spot_coords"][unicode(self.dimension)].iterrows():
                place = self.dimension.get_place(rd["place"])
                spot = Spot(board=self, place=place)
                self.spotdict[unicode(place)] = spot
        if (
                "pawn_img" in self.closet.skeleton and
                unicode(self.dimension) in self.dimension.closet.skeleton[
                    "pawn_img"]):
            for rd in self.dimension.closet.skeleton[
                    "pawn_img"][unicode(self.dimension)].iterrows():
                thing = self.dimension.get_thing(rd["thing"])
                pawn = Pawn(board=self, thing=thing)
                self.pawndict[unicode(thing)] = pawn
        for portal in self.dimension.portals:
            arrow = Arrow(board=self, portal=portal)
            self.arrowdict[unicode(portal)] = arrow
            content.add_widget(arrow)
        for spot in self.spotdict.itervalues():
            content.add_widget(spot)
        for pawn in self.pawndict.itervalues():
            content.add_widget(pawn)

    def __str__(self):
        return str(self.dimension)

    def upd_rowdict(self, *args):
        self.rowdict = dict(self.closet.skeleton["board"][unicode(self)])

    def get_texture(self):
        return self.closet.get_texture(self.rowdict["wallpaper"])

    def new_branch(self, parent, branch, tick):
        for spot in self.spotdict.itervalues():
            spot.new_branch(parent, branch, tick)
        for pawn in self.pawndict.itervalues():
            pawn.new_branch(parent, branch, tick)
