from gi.repository import Adw, Gtk


@Gtk.Template(filename="yafti/gtk/tour.ui")
class YaftiTour(Adw.Bin):
    __gtype_name__ = "YaftiTour"

    status_page = Gtk.Template.Child()
    assets_media = Gtk.Template.Child()

    def __init__(self, window, tour, **kwargs):
        super().__init__(**kwargs)
        self.__window = window
        self.__tour = tour

        self.__build_ui()

    def __build_ui(self):
        self.assets_media.set_resource(self.__tour["resource"])
        self.status_page.set_title(self.__tour["title"])
        self.status_page.set_description(self.__tour["description"])
