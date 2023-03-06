from gi.repository import Adw, Gtk
from typing import Any, Optional
from pydantic import BaseModel


_xml = """\
<?xml version="1.0" encoding="UTF-8"?>
<interface>
    <requires lib="gtk" version="4.0"/>
    <requires lib="libadwaita" version="1.0" />
    <template class="YaftiTitleScreen" parent="AdwBin">
        <property name="halign">fill</property>
        <property name="valign">fill</property>
        <property name="hexpand">true</property>
        <child>
            <object class="AdwStatusPage" id="status_page">
                <property name="icon-name">folder</property>
                <property name="title" translatable="yes">Welcome!</property>
                <property name="description" translatable="yes">
                    Make your choices, this wizard will take care of everything.
                </property>
            </object>
        </child>
    </template>
</interface>
"""


@Gtk.Template(string=_xml)
class TitleScreen(Adw.Bin):
    __gtype_name__ = "YaftiTitleScreen"

    status_page = Gtk.Template.Child()

    class Config(BaseModel):
        title: str
        description: str
        icon: Optional[str] = None

    @classmethod
    def from_config(cls, cfg: Any) -> "TitleScreen":
        c = cls.Config.parse_obj(cfg)
        return cls(**c.dict())

    def __init__(
        self, title: str = None, description: str = None, icon: str = None, **kwargs
    ):
        super().__init__(**kwargs)
        self.status_page.set_title(title)
        self.status_page.set_description(description)
