from kivy.properties import (
    ListProperty,
    ObjectProperty)
from kivy.uix.label import Label
from kivy.uix.gridlayout import GridLayout
from kivy.uix.scrollview import ScrollView

from kivy.clock import Clock


class TableCell(Label):
    text_getter = ObjectProperty()

    def __init__(self, **kwargs):
        kwargs['size_hint_y'] = None
        super(TableCell, self).__init__(**kwargs)

    def upd_text(self, *args):
        self.text = self.text_getter()


class TableHeader(TableCell):
    pass


class TableBody(TableCell):
    pass


class TableContent(GridLayout):
    closet = ObjectProperty()

    def __init__(self, **kwargs):
        super(TableContent, self).__init__(**kwargs)
        self.trigger_repop = Clock.create_trigger(self.repop)

    def on_parent(self, *args):
        self.trigger_repop()

    def repop(self, *args):
        self.clear_widgets()
        self.cols = len(self.parent.headers) + len(self.parent.stats)
        for header in self.parent.headers + self.parent.stats:
            hwid = TableHeader(
                text_getter=lambda: self.closet.get_text(header))
            self.closet.register_text_listener(header, hwid.upd_text)
            hwid.upd_text()
            self.add_widget(hwid)
        for item in self.parent.items:
            for fieldname in self.parent.fieldnames:
                bwid = TableBody(
                    text_getter=lambda: unicode(getattr(item, fieldname)))
                self.closet.register_time_listener(bwid.upd_text)
                self.add_widget(bwid)
                bwid.upd_text()
            for stat in self.parent.stats:
                bwid = TableBody(
                    text_getter=lambda: unicode(item.get_stat(stat)))
                self.closet.register_time_listener(bwid.upd_text)
                self.add_widget(bwid)
                bwid.upd_text()


class TableView(ScrollView):
    character = ObjectProperty()
    headers = ListProperty()
    fieldnames = ListProperty()
    items = ListProperty()
    stats = ListProperty()
    edbut = ObjectProperty()


class CharStatTableContent(GridLayout):
    closet = ObjectProperty()

    def __init__(self, **kwargs):
        kwargs['cols'] = 2
        super(CharStatTableContent, self).__init__(**kwargs)

    def repop(self, *args):
        self.clear_widgets()
        for stat in self.parent.stats:
            statwid = TableBody(
                text_getter=lambda: self.closet.get_text(stat))
            self.add_widget(statwid)
            valwid = TableBody(
                text_getter=lambda: unicode(
                    self.parent.character.get_stat(stat)))
            self.closet.register_time_listener(valwid.upd_text)


class CharStatTableView(ScrollView):
    character = ObjectProperty()
    stats = ListProperty()
    edbut = ObjectProperty()
