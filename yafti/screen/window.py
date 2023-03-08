from functools import partial

from gi.repository import Adw, Gtk

import yafti.share
from yafti import events
from yafti.registry import SCREENS

_xml = """\
<?xml version="1.0" encoding="UTF-8"?>
<interface>
  <requires lib="gtk" version="4.0"/>
  <requires lib="libadwaita" version="1.0" />
  <template class="YaftiWindow" parent="AdwApplicationWindow">
    <property name="default-width">750</property>
    <property name="default-height">640</property>
    <property name="title">Welcome!</property>
    <child>
      <object class="GtkBox">
        <property name="orientation">vertical</property>
        <child>
          <object class="AdwHeaderBar" id="headerbar">
            <style>
              <class name="flat" />
            </style>
            <property name="title_widget">
              <object class="AdwCarouselIndicatorDots" id="carousel_indicator">
                <property name="carousel">carousel</property>
                <property name="orientation">horizontal</property>
              </object>
            </property>
            <child type="start">
              <object class="GtkButton" id="btn_back">
                <property name="label" translatable="yes">Back</property>
                <property name="halign">center</property>
                <property name="visible">False</property>
              </object>
            </child>
            <child>
              <object class="GtkButton" id="btn_next">
                <property name="label" translatable="yes">Next</property>
                <property name="halign">center</property>
                <property name="visible">True</property>
                <style>
                  <class name="suggested-action" />
                </style>
              </object>
            </child>
          </object>
        </child>
        <child>
          <object class="AdwToastOverlay" id="toasts">
            <child>
              <object class="AdwCarousel" id="carousel">
                <property name="vexpand">True</property>
                <property name="hexpand">True</property>
                <property name="allow_scroll_wheel">False</property>
                <property name="allow_mouse_drag">False</property>
                <property name="allow_long_swipes">False</property>
              </object>
            </child>
          </object>
        </child>
      </object>
    </child>
  </template>
</interface>
"""


@Gtk.Template(string=_xml)
class Window(Adw.ApplicationWindow):
    __gtype_name__ = "YaftiWindow"

    carousel_indicator = Gtk.Template.Child()
    carousel = Gtk.Template.Child()
    headerbar = Gtk.Template.Child()
    btn_back = Gtk.Template.Child()
    btn_next = Gtk.Template.Child()
    toasts = Gtk.Template.Child()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.app = kwargs.get("application")
        events.register("btn_next")
        events.register("btn_back")
        events.on("btn_next", self.next)
        events.on("btn_back", self.back)

        # not a huge fan of this
        yafti.share.BTN_BACK = self.btn_back
        yafti.share.BTN_NEXT = self.btn_next

        _next = partial(events.emit, "btn_next")
        _back = partial(events.emit, "btn_back")
        self.btn_next.connect("clicked", _next)
        self.btn_back.connect("clicked", _back)
        self.carousel.connect("page-changed", self.changed)

        self.draw()

    def draw(self):
        screens = self.app.config.screens
        for name, details in screens.items():
            if details.source not in SCREENS:
                continue
            screen = SCREENS.get(details.source)
            self.carousel.append(screen.from_config(details.values))

    @property
    def idx(self):
        return self.carousel.get_position()

    def goto(self, page: int, animate: bool = True):
        if page < 0:
            page = 0

        if page >= self.carousel.get_n_pages():
            page = self.carousel.get_n_pages()

        current_screen = self.carousel.get_nth_page(self.idx)
        next_screen = self.carousel.get_nth_page(page)

        current_screen.deactivate()
        self.carousel.scroll_to(next_screen, animate)

    def next(self, _):
        if self.idx + 1 >= self.carousel.get_n_pages():
            self.app.quit()
            self.app.loop.stop()

        else:
            self.goto(self.idx + 1)

    def back(self, _):
        self.goto(self.idx - 1)

    def changed(self, *args):
        self.btn_back.set_visible(self.idx > 0)
        current_screen = self.carousel.get_nth_page(self.idx)
        if self.idx + 1 >= self.carousel.get_n_pages():
            self.btn_next.set_label("Done")
            self.btn_back.set_visible(False)
        else:
            self.btn_next.set_label("Next")
        current_screen.activate()
