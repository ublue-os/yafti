from gi.repository import Adw, Gtk
from yafti.windows.dialog import YaftiDialog


# TODO: not working please make work.
@Gtk.Template(resource_path="/org/ublue-os/yafti/confirm.ui")
class YaftiConfirm(Adw.Bin):
    __gtype_name__ = "YaftiConfirm"

    status_page = Gtk.Template.Child()
    reject_btn = Gtk.Template.Child()
    accept_btn = Gtk.Template.Child()
    info_btn = Gtk.Template.Child()

    def __init__(self, window, distro_info, key, step, **kwargs):
        super().__init__(**kwargs)
        self.__window = window
        self.__distro_info = distro_info
        self.__key = key
        self.__step = step
        self.__response = False
        self.__build_ui()

        # signals
        self.accept_btn.connect("clicked", self.__on_response, True)
        self.reject_btn.connect("clicked", self.__on_response, False)
        self.info_btn.connect("clicked", self.__on_info)

    def __build_ui(self):
        self.status_page.set_icon_name(self.__step["icon"])
        self.status_page.set_title(self.__step["title"])
        self.status_page.set_description(self.__step["description"])

        self.accept_btn.set_label(self.__step["buttons"]["yes"])
        self.reject_btn.set_label(self.__step["buttons"]["no"])

        if "info" in self.__step["buttons"]:
            self.info_btn.set_visible(True)

    def __on_response(self, _, response):
        self.__response = response
        self.__window.next()

    def __on_info(self, _):
        if "info" not in self.__step["buttons"]:
            return

        dialog = YaftiDialog(
            self.__window,
            self.__step["buttons"]["info"]["title"],
            self.__step["buttons"]["info"]["text"],
        )
        dialog.show()

    def get_finals(self):
        return {
            "vars": {self.__key: self.__response},
            "funcs": [x for x in self.__step["final"]],
        }
