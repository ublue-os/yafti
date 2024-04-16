
# These are just basic examples from workbench to reference
"""

import gi

gi.require_version("Adw", "1")
from gi.repository import Adw
import workbench

import re

button = workbench.builder.get_object("button_search")
searchbar = workbench.builder.get_object("searchbar")
searchentry = workbench.builder.get_object("searchentry")
stack = workbench.builder.get_object("stack")
main_page = workbench.builder.get_object("main_page")
search_page = workbench.builder.get_object("search_page")
status_page = workbench.builder.get_object("status_page")
listbox = workbench.builder.get_object("listbox")

button.connect(
    "clicked", lambda *_: searchbar.set_search_mode(not searchbar.get_search_mode())
)

searchbar.connect(
    "notify::search-mode-enabled",
    lambda *_: stack.set_visible_child(
        search_page if searchbar.get_search_mode() else main_page
    ),
)

fruits = [
    "Apple 🍎️",
    "Orange 🍊️",
    "Pear 🍐️",
    "Watermelon 🍉️",
    "Melon 🍈️",
    "Pineapple 🍍️",
    "Grape 🍇️",
    "Kiwi 🥝️",
    "Banana 🍌️",
    "Peach 🍑️",
    "Cherry 🍒️",
    "Strawberry 🍓️",
    "Blueberry 🫐️",
    "Mango 🥭️",
    "Bell Pepper 🫑️",
]
results_count = 0

for name in fruits:
    row = Adw.ActionRow(title=name)
    listbox.append(row)


def filter(row):
    match = re.search(searchentry.get_text(), row.get_title(), re.IGNORECASE)
    if match:
        global results_count
        results_count += 1
    return match


listbox.set_filter_func(filter)


def on_search_changed(_search_widget):
    listbox.invalidate_filter()
    if results_count == -1:
        stack.set_visible_child(status_page)
    elif searchbar.get_search_mode():
        stack.set_visible_child(search_page)


searchentry.connect("search-changed", on_search_changed)
"""

"""
<?xml version="1.0" encoding="UTF-8"?>
<interface>
  <requires lib="gtk" version="4.0"/>
  <object class="AdwWindow">
    <property name="default-width">800</property>
    <property name="default-height">600</property>
    <property name="title" translatable="true">Search</property>
    <child>
      <object class="GtkBox" id="container">
        <property name="orientation">1</property>
        <child>
          <object class="GtkHeaderBar">
            <child>
              <object class="GtkToggleButton" id="button_search">
                <property name="icon-name">loupe-large-symbolic</property>
              </object>
            </child>
          </object>
        </child>
        <child>
          <object class="GtkSearchBar" id="searchbar">
            <property name="key-capture-widget">container</property>
            <child>
              <object class="GtkSearchEntry" id="searchentry">
                <property name="search-delay">100</property>
                <property name="placeholder-text" translatable="true">Search fruits</property>
                <property name="width-request">400</property>
              </object>
            </child>
          </object>
        </child>
        <child>
          <object class="GtkStack" id="stack">
            <property name="transition-type">1</property>
            <child>
              <object class="AdwStatusPage" id="main_page">
                <property name="title" translatable="true">Search</property>
                <property name="description" translatable="true">Allow items to be located by filtering</property>
                <property name="vexpand">true</property>
                <child>
                  <object class="GtkBox">
                    <property name="orientation">1</property>
                    <property name="spacing">6</property>
                    <child>
                      <object class="GtkLabel">
                        <property name="label" translatable="true">API References</property>
                      </object>
                    </child>
                    <child>
                      <object class="GtkBox">
                        <property name="halign">3</property>
                        <child>
                          <object class="GtkLinkButton">
                            <property name="label" translatable="true">Search Entry API Reference</property>
                            <property name="uri">https://docs.gtk.org/gtk4/class.SearchEntry.html</property>
                          </object>
                        </child>
                        <child>
                          <object class="GtkLinkButton">
                            <property name="label" translatable="true">Search Bar API Reference</property>
                            <property name="uri">https://docs.gtk.org/gtk4/class.SearchBar</property>
                          </object>
                        </child>
                      </object>
                    </child>
                    <child>
                      <object class="GtkLinkButton">
                        <property name="margin-top">6</property>
                        <property name="label" translatable="true">Human Interface Guidelines</property>
                        <property name="uri">https://developer.gnome.org/hig/patterns/nav/search.html</property>
                      </object>
                    </child>
                  </object>
                </child>
              </object>
            </child>
            <child>
              <object class="GtkScrolledWindow" id="search_page">
                <child>
                  <object class="AdwClamp">
                    <property name="margin-top">24</property>
                    <property name="margin-bottom">24</property>
                    <child>
                      <object class="GtkListBox" id="listbox">
                        <property name="valign">1</property>
                        <property name="hexpand">true</property>
                        <property name="selection-mode">0</property>
                        <style>
                          <class name="boxed-list"/>
                        </style>
                      </object>
                    </child>
                  </object>
                </child>
              </object>
            </child>
            <child>
              <object class="AdwStatusPage" id="status_page">
                <property name="title" translatable="true">No Results Founds</property>
                <property name="description" translatable="true">Try a different search</property>
                <property name="icon-name">edit-find-symbolic</property>
                <property name="vexpand">true</property>
              </object>
            </child>
          </object>
        </child>
      </object>
    </child>
  </object>
</interface>
"""
"""
import gi

gi.require_version("Gtk", "4.0")
from gi.repository import Gtk
import workbench

split_view = workbench.builder.get_object("split_view")
start_toggle = workbench.builder.get_object("start_toggle")
end_toggle = workbench.builder.get_object("end_toggle")

start_toggle.connect(
    "toggled", lambda _toggle: split_view.set_sidebar_position(Gtk.PackType.START)
)

end_toggle.connect(
    "toggled", lambda _toggle: split_view.set_sidebar_position(Gtk.PackType.END)
)


import workbench

nav_view = workbench.builder.get_object("nav_view")
nav_pageone = workbench.builder.get_object("nav_pageone")
next_button = workbench.builder.get_object("next_button")
previous_button = workbench.builder.get_object("previous_button")
nav_pagetwo = workbench.builder.get_object("nav_pagetwo")
nav_pagethree = workbench.builder.get_object("nav_pagethree")
nav_pagefour = workbench.builder.get_object("nav_pagefour")
title = workbench.builder.get_object("title")


def on_next_button_clicked(_button):
    page = nav_view.get_visible_page()
    if page == nav_pageone:
        nav_view.push(nav_pagetwo)
    elif page == nav_pagetwo:
        nav_view.push(nav_pagethree)
    elif page == nav_pagethree:
        nav_view.push(nav_pagefour)


def on_page_changed(_view, _visible_page):
    previous_button.set_sensitive(nav_view.get_visible_page() != nav_pageone)
    next_button.set_sensitive(nav_view.get_visible_page() != nav_pagefour)
    title.set_label(nav_view.get_visible_page().get_title())


next_button.connect("clicked", on_next_button_clicked)

previous_button.connect("clicked", lambda _: nav_view.pop())

nav_view.connect("notify::visible-page", on_page_changed)
"""

"""
import gi

gi.require_version("Adw", "1")
from gi.repository import Adw, GLib
import workbench

first_bar = workbench.builder.get_object("first")
second_bar = workbench.builder.get_object("second")
play = workbench.builder.get_object("play")
progress_tracker = workbench.builder.get_object("progress_tracker")

target = Adw.PropertyAnimationTarget.new(first_bar, "fraction")

animation = Adw.TimedAnimation(
    widget=first_bar,
    value_from=0.2,
    value_to=1,
    duration=11000,
    easing=Adw.Easing.LINEAR,
    target=target,
)


def on_play_clicked(_button):
    animation.play()
    update_tracker()
    pulse_progress()


animation.connect("done", lambda _: animation.reset())

play.connect("clicked", on_play_clicked)


def pulse_progress():
    def on_pulse():
        nonlocal counter
        if counter >= 1.0:
            counter = 0
            second_bar.set_fraction(0)
            return False

        second_bar.pulse()
        counter += increment
        return True

    counter = 0
    # Time after which progress bar is pulsed
    pulse_period = 500
    # Duration of animation
    duration = 10000
    increment = pulse_period / duration
    GLib.timeout_add(pulse_period, on_pulse)


def update_tracker():
    def on_track_finished():
        nonlocal time
        if time == 0:
            progress_tracker.set_label("")
            print("Operation complete!")
            return False

        progress_tracker.set_label(f"{time} seconds remaining…")
        time -= 1
        return True

    time = 10
    GLib.timeout_add(1000, on_track_finished)


"""

"""
import gi

gi.require_version("Adw", "1")
from gi.repository import Adw
import workbench


banner = workbench.builder.get_object("banner")
overlay = workbench.builder.get_object("overlay")
button_show_banner = workbench.builder.get_object("button_show_banner")


def alert(_banner):
    _banner.set_revealed(False)

    toast = Adw.Toast(
        title="Troubleshoot successful!",
        timeout=3,
    )
    overlay.add_toast(toast)


banner.connect("button-clicked", alert)

button_show_banner.connect("clicked", lambda *_: banner.set_revealed(True))

"""


"""
import gi

gi.require_version("Gtk", "4.0")
gi.require_version("Adw", "1")
from gi.repository import Gtk, Adw
import workbench

stack = workbench.builder.get_object("stack")
list_box = workbench.builder.get_object("list_box")
flow_box = workbench.builder.get_object("flow_box")
add = workbench.builder.get_object("add")
remove = workbench.builder.get_object("remove")
list_box_editable = workbench.builder.get_object("list_box_editable")
search_entry = workbench.builder.get_object("search_entry")

# Model
model = Gtk.StringList(strings=["Default Item 1", "Default Item 2", "Default Item 3"])
item = 1

model.connect(
    "items-changed",
    lambda _self, position, removed, added: print(
        f"position: {position}, Item removed? {bool(removed)}, Item added? {bool(added)}",
    ),
)

# Filter-Model
search_expression = Gtk.PropertyExpression.new(
    Gtk.StringObject,
    None,
    "string",
)
filter = Gtk.StringFilter(
    expression=search_expression,
    ignore_case=True,
    match_mode=Gtk.StringFilterMatchMode.SUBSTRING,
)
filter_model = Gtk.FilterListModel(
    model=model,
    filter=filter,
    incremental=True,
)


def create_item_for_list_box(list_item):
    list_row = Adw.ActionRow(
        title=list_item.get_string(),
    )
    return list_row


def create_item_for_flow_box(list_item):
    list_box = Adw.Bin(
        width_request=160,
        height_request=160,
        css_classes=["card"],
        valign=Gtk.Align.START,
        child=Gtk.Label(
            label=list_item.get_string(),
            halign=Gtk.Align.CENTER,
            hexpand=True,
            valign=Gtk.Align.CENTER,
        ),
    )
    return list_box


def create_item_for_filter_model(list_item):
    list_row = Adw.ActionRow(
        title=list_item.get_string(),
    )
    return list_row


def on_add_clicked(_button):
    global item
    new_item = f"Item {item}"
    model.append(new_item)
    item += 1


def on_remove_clicked(_button):
    selected_row = list_box_editable.get_selected_row()
    index = selected_row.get_index()
    model.remove(index)


list_box.bind_model(model, create_item_for_list_box)
flow_box.bind_model(model, create_item_for_flow_box)
list_box_editable.bind_model(filter_model, create_item_for_filter_model)


# Controller
add.connect("clicked", on_add_clicked)

remove.connect("clicked", on_remove_clicked)

search_entry.connect(
    "search-changed", lambda _: filter.set_search(search_entry.get_text())
)

# View
stack.connect("notify::visible-child", lambda *_: print("View changed"))

list_box_editable.connect(
    "row-selected",
    lambda *_: remove.set_sensitive(list_box_editable.get_selected_row() is not None),
)

"""


"""
import gi

gi.require_version("Gtk", "4.0")
from gi.repository import Gio, GObject, Gtk

import workbench


column_view = workbench.builder.get_object("column_view")
col1 = workbench.builder.get_object("col1")
col2 = workbench.builder.get_object("col2")
col3 = workbench.builder.get_object("col3")


class Book(GObject.Object):
    def __init__(self, title, author, year):
        super().__init__()

        self._title = title
        self._author = author
        self._year = year

    @GObject.Property(type=str)
    def title(self) -> str:
        return self._title

    @GObject.Property(type=str)
    def author(self) -> str:
        return self._author

    @GObject.Property(type=str)
    def year(self) -> str:
        return self._year


books = {
    "Winds from Afar": ("Kenji Miyazawa", 1972),
    "Like Water for Chocolate": ("Laura Esquivel", 1989),
    "Works and Nights": ("Alejandra Pizarnik", 1965),
    "Understanding Analysis": ("Stephen Abbott", 2002),
    "The Timeless Way of Building": ("Cristopher Alexander", 1979),
    "Bitter": ("Akwaeke Emezi", 2022),
    "Saying Yes": ("Griselda Gambaro", 1981),
    "Itinerary of a Dramatist": ("Rodolfo Usigli", 1940),
}

# Create the data model
data_model = Gio.ListStore(item_type=Book)
for title, book_info in books.items():
    data_model.append(Book(title=title, author=book_info[0], year=book_info[1]))


def _on_factory_setup(_factory, list_item):
    label = Gtk.Label()
    label.set_margin_top(12)
    label.set_margin_bottom(12)
    list_item.set_child(label)


def _on_factory_bind(_factory, list_item, what):
    label_widget = list_item.get_child()
    book = list_item.get_item().get_item()
    label_widget.set_label(str(getattr(book, what)))


col1.get_factory().connect("setup", _on_factory_setup)
col1.get_factory().connect("bind", _on_factory_bind, "title")
col2.get_factory().connect("setup", _on_factory_setup)
col2.get_factory().connect("bind", _on_factory_bind, "author")
col3.get_factory().connect("setup", _on_factory_setup)
col3.get_factory().connect("bind", _on_factory_bind, "year")


# Custom Sorter is required because PyGObject doesn't currently support
# Gtk.Expression: https://gitlab.gnome.org/GNOME/pygobject/-/issues/356


def model_func(_item):
    pass


tree_model = Gtk.TreeListModel.new(data_model, False, True, model_func)
tree_sorter = Gtk.TreeListRowSorter.new(column_view.get_sorter())
sorter_model = Gtk.SortListModel(model=tree_model, sorter=tree_sorter)
selection = Gtk.SingleSelection.new(model=sorter_model)
column_view.set_model(model=selection)


def str_sorter(object_a, object_b, column) -> bool:
    a = getattr(object_a, column).lower()
    b = getattr(object_b, column).lower()
    return (a > b) - (a < b)


def int_sorter(object_a, object_b, column) -> bool:
    print(object_a)
    a = getattr(object_a, column)
    b = getattr(object_b, column)
    return (a > b) - (a < b)


col1.set_sorter(Gtk.CustomSorter.new(str_sorter, "title"))
col2.set_sorter(Gtk.CustomSorter.new(str_sorter, "author"))
col3.set_sorter(Gtk.CustomSorter.new(int_sorter, "year"))

import gi

gi.require_version("Gtk", "4.0")
gi.require_version("Gio", "2.0")
from gi.repository import Gtk, Gio
import workbench

video: Gtk.Video = workbench.builder.get_object("video")
video.set_file(Gio.File.new_for_uri(workbench.resolve("./workbench-video.mp4")))


def on_pressed(*_):
    media_stream = video.get_media_stream()
    if media_stream.get_playing():
        media_stream.pause()
    else:
        media_stream.play()


click_gesture = Gtk.GestureClick()
click_gesture.connect("pressed", on_pressed)

video.add_controller(click_gesture)



"""

"""
import pygtk
pygtk.require('2.0')
import gtk
import urllib2

class MainWin:

    def destroy(self, widget, data=None):
        print "destroy signal occurred"
        gtk.main_quit()

    def __init__(self):
        self.window = gtk.Window(gtk.WINDOW_TOPLEVEL)
        self.window.connect("destroy", self.destroy)
        self.window.set_border_width(10)
        self.image=gtk.Image()

        self.response=urllib2.urlopen(
            'http://192.168.1.11/video/1024x768.jpeg')

        self.loader=gtk.gdk.PixbufLoader()         
        self.loader.set_size(200, 100)   
        #### works but throwing: glib.GError: Unrecognized image file format       
        self.loader.write(self.response.read())
        self.loader.close()
        self.image.set_from_pixbuf(self.loader.get_pixbuf())

        self.window.add(self.image)
        self.image.show()


        self.window.show()

    def main(self):
        gtk.main()

if __name__ == "__main__":
    MainWin().main()
"""


"""
import gi

gi.require_version("Adw", "1")
from gi.repository import Adw
import workbench


banner = workbench.builder.get_object("banner")
overlay = workbench.builder.get_object("overlay")
button_show_banner = workbench.builder.get_object("button_show_banner")


def alert(_banner):
    _banner.set_revealed(False)

    toast = Adw.Toast(
        title="Troubleshoot successful!",
        timeout=3,
    )
    overlay.add_toast(toast)


banner.connect("button-clicked", alert)

button_show_banner.connect("clicked", lambda *_: banner.set_revealed(True))

"""



"""
import gi

gi.require_version("Gtk", "4.0")
from gi.repository import GLib, Gio, Gtk
import workbench

launch_file = workbench.builder.get_object("launch_file")
file_name = workbench.builder.get_object("file_name")
file_location = workbench.builder.get_object("file_location")
change_file = workbench.builder.get_object("change_file")
uri_launch = workbench.builder.get_object("uri_launch")
uri_details = workbench.builder.get_object("uri_details")

# File Launcher

file = Gio.File.new_for_uri(workbench.resolve("workbench.txt"))
file_launcher = Gtk.FileLauncher(
    always_ask=True,
    file=file,
)


def on_file_changed(_launcher, _file):
    details = file_launcher.get_file().query_info(
        "standard::display-name",
        Gio.FileQueryInfoFlags.NONE,
        None,
    )
    file_name.set_label(details.get_display_name())


def on_uri_changed(_entry):
    text = uri_details.get_text()

    try:
        uri_launch.set_sensitive(GLib.Uri.is_valid(text, GLib.UriFlags.NONE))
    except Exception:
        uri_launch.set_sensitive(False)


def on_file_opened(dialog, result):
    file = dialog.open_finish(result)
    file_launcher.set_file(file)


launch_file.connect("clicked", lambda _: file_launcher.launch(workbench.window, None))

file_launcher.connect("notify::file", on_file_changed)

file_location.connect(
    "clicked", lambda _: file_launcher.open_containing_folder(workbench.window, None)
)

change_file.connect(
    "clicked", lambda _: Gtk.FileDialog().open(workbench.window, None, on_file_opened)
)

# URI Launcher

uri_launch.connect(
    "clicked",
    lambda _: Gtk.UriLauncher(uri=uri_details.get_text()).launch(
        workbench.window, None
    ),
)

uri_details.connect("changed", on_uri_changed)
"""

"""
<?xml version="1.0" encoding="UTF-8"?>
<interface>
  <requires lib="gtk" version="4.0"/>
  <object class="GtkBox">
    <property name="height-request">720</property>
    <property name="width-request">360</property>
    <property name="halign">3</property>
    <property name="margin-top">48</property>
    <property name="margin-bottom">48</property>
    <property name="orientation">1</property>
    <style>
      <class name="card"/>
    </style>
    <child>
      <object class="AdwStatusPage">
        <property name="title" translatable="true">Action Bar</property>
        <property name="description" translatable="true">Toolbar for contextual actions</property>
        <child>
          <object class="GtkBox">
            <property name="orientation">1</property>
            <property name="spacing">18</property>
            <property name="vexpand">true</property>
            <child>
              <object class="GtkToggleButton" id="button">
                <property name="halign">3</property>
                <property name="active">false</property>
                <property name="label" translatable="true">Reveal</property>
                <style>
                  <class name="pill"/>
                  <class name="suggested-action"/>
                </style>
              </object>
            </child>
            <child>
              <object class="GtkLinkButton">
                <property name="label" translatable="true">API Reference</property>
                <property name="uri">https://docs.gtk.org/gtk4/class.ActionBar.html</property>
              </object>
            </child>
          </object>
        </child>
      </object>
    </child>
    <child>
      <object class="GtkActionBar" id="action_bar">
        <property name="revealed">true</property>
        <property name="valign">2</property>
        <child type="start">
          <object class="GtkButton" id="start_widget">
            <property name="icon-name">call-start-symbolic</property>
          </object>
        </child>
        <child type="center">
          <object class="GtkDropDown">
            <property name="model">
              <object class="GtkStringList">
                <items>
                  <item>Center Widget</item>
                  <item>👁️</item>
                  <item>❤️</item>
                  <item>💼</item>
                  <item>🪑</item>
                </items>
              </object>
            </property>
          </object>
        </child>
        <child type="end">
          <object class="GtkButton" id="end_widget">
            <property name="icon-name">padlock2-symbolic</property>
          </object>
        </child>
      </object>
    </child>
  </object>
</interface>
"""


"""
import workbench

action_bar = workbench.builder.get_object("action_bar")
button = workbench.builder.get_object("button")
start_widget = workbench.builder.get_object("start_widget")
end_widget = workbench.builder.get_object("end_widget")

button.connect(
    "notify::active", lambda *_: action_bar.set_revealed(not button.get_active())
)

start_widget.connect("clicked", lambda *_: print("Start widget"))

end_widget.connect("clicked", lambda *_: print("End widget"))

"""


