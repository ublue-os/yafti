from typing import Optional

from gi.repository import Adw, Gtk

import yafti.share
from yafti import events
from yafti.abc import YaftiScreen, YaftiScreenConfig
from yafti.screen.package.models import PackageConfig, PackageGroupConfig
from yafti.screen.package.screen import PackageInstallScreen, PackagePickerScreen
from yafti.screen.package.state import PackageScreenState
from yafti.screen.package.utils import parse_packages, generate_fingerprint

_xml = """\
<?xml version="1.0" encoding="UTF-8"?>
<interface>
  <requires lib="gtk" version="4.0"/>
  <template class="YaftiPackageScreen" parent="AdwBin">
    <property name="halign">fill</property>
    <property name="valign">fill</property>
    <property name="hexpand">true</property>
    <child>
      <object class="AdwCarousel" id="pkg_carousel">
        <property name="vexpand">True</property>
        <property name="hexpand">True</property>
        <property name="allow_scroll_wheel">False</property>
        <property name="allow_mouse_drag">False</property>
        <property name="allow_long_swipes">False</property>
      </object>
    </child>
  </template>
</interface>
"""


@Gtk.Template(string=_xml)
class PackageScreen(YaftiScreen, Adw.Bin):
    __gtype_name__ = "YaftiPackageScreen"

    pkg_carousel = Gtk.Template.Child()

    class Config(YaftiScreenConfig):
        title: str
        show_terminal: bool = True
        package_manager: str
        groups: Optional[PackageGroupConfig] = None
        packages: Optional[list[PackageConfig]] = None
        package_manager_defaults: Optional[dict] = None

    def __init__(
        self,
        title: str = "Package Installation",
        package_manager: str = "yafti.plugin.flatpak",
        packages: list[PackageConfig] = None,
        groups: PackageGroupConfig = None,
        show_terminal: bool = True,
        package_manager_defaults: Optional[dict] = None,
        **kwargs,
    ):
        super().__init__(**kwargs)
        self.title = title
        self.packages = groups or packages
        self.show_terminal = show_terminal
        self.package_manager = package_manager
        self.package_manager_defaults = package_manager_defaults
        self.fingerprint = generate_fingerprint(self.packages)
        self.state = PackageScreenState(self.fingerprint)
        self.state.load(parse_packages(self.packages))
        self.pkg_carousel.connect("page-changed", self.changed)
        self.draw()

    def draw(self):
        self.pkg_carousel.append(
            PackagePickerScreen(
                state=self.state, title=self.title, packages=self.packages
            )
        )
        self.pkg_carousel.append(
            PackageInstallScreen(
                title=self.title,
                state=self.state,
                package_manager=self.package_manager,
                package_manager_defaults=self.package_manager_defaults,
            )
        )

    def on_activate(self):
        events.on("btn_next", self.next)
        events.on("btn_back", self.back)
        yafti.share.BTN_NEXT.set_label("Install")

    def on_deactivate(self):
        events.detach("btn_next", self.next)
        events.detach("btn_back", self.back)

    @property
    def idx(self):
        return self.pkg_carousel.get_position()

    @property
    def total(self):
        return self.pkg_carousel.get_n_pages()

    def goto(self, page: int, animate: bool = True):
        if page < 0:
            page = 0

        if page >= self.pkg_carousel.get_n_pages():
            page = self.pkg_carousel.get_n_pages()

        current_screen = self.pkg_carousel.get_nth_page(self.idx)
        next_screen = self.pkg_carousel.get_nth_page(page)

        current_screen.deactivate()
        self.pkg_carousel.scroll_to(next_screen, animate)

    def changed(self, *args):
        current_screen = self.pkg_carousel.get_nth_page(self.idx)
        current_screen.activate()

    async def next(self, _):
        if not self.active:
            return False
        if self.idx + 1 == self.total:
            return False
        self.goto(self.idx + 1)

    async def back(self, _):
        if not self.active:
            return False

        if self.idx - 1 < 0:
            return False
        self.goto(self.idx - 1)
