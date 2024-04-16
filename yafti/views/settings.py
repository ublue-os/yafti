from gi.repository import Adw, Gdk, Gio, GObject, Gtk


class Settings:
    def __init__(self):
        self.scrolled_window = Gtk.ScrolledWindow()
        self.scrolled_window.set_vexpand(True)

        self.preference = Adw.PreferencesPage()
        self.preferences_group = Adw.PreferencesGroup()

        # Connect to root application to get config object
        application = Gio.Application.get_default()

        # https://gnome.pages.gitlab.gnome.org/libadwaita/doc/1-latest/class.SpinRow.html
        # This setting is intended to allow yafti to run as a daemon and check for changes or updates
        self.interval_seconds = Adw.SpinRow(
            title="Interval (Seconds)",
            subtitle="Set the metric update interval",
            digits=1,
            snap_to_ticks=True,
            can_focus=True,
            selectable=False,
            adjustment=Gtk.Adjustment(
                value=application.config.settings.get_value("interval").get_double(),
                lower=0.1,
                upper=10.0,
                step_increment=0.1,
                page_increment=1,
                page_size=0,
            ),
        )

        application.config.settings.bind(
            "interval",
            self.interval_seconds,
            "value",
            Gio.SettingsBindFlags.GET_NO_CHANGES,
        )

        self.consent_accepted = Adw.SwitchRow(
            title="Consent Acceptance",
            subtitle="Accepted application consent policy",
            selectable=False,
            can_focus=False,
            can_target=False,
            active=False,
            # activatable=False,
        )
        application.config.settings.bind(
            "consent-accepted",
            self.consent_accepted,
            "active",
            Gio.SettingsBindFlags.DEFAULT,
        )

        self.disable_yafti = Adw.SwitchRow(
            title="Disable Yafti",
            subtitle="Disable Yafti from running on the system.",
            selectable=False,
            can_focus=False,
            can_target=False,
            active=False,
            activatable=True,
        )
        application.config.settings.bind(
            "disabled",
            self.disable_yafti,
            "active",
            Gio.SettingsBindFlags.DEFAULT,
        )

        self.included_packages = Adw.EntryRow(
            title="Included Packages",
            can_focus=False,
            can_target=False,

        )
        application.config.settings.bind(
            'included-packages',
            self.included_packages,
            "active",
            Gio.SettingsBindFlags.DEFAULT
        )

        self.excluded_packages = Adw.EntryRow(
            title="Excluded Packages",
            can_focus=False,
            can_target=False,

        )
        application.config.settings.bind(
            'excluded-packages',
            self.excluded_packages,
            "active",
            Gio.SettingsBindFlags.DEFAULT
        )

        # self.preferences_group.add(self.included_packages)
        # self.consent_accepted.set_data(True)
        self.preferences_group.add(self.consent_accepted)
        self.preferences_group.add(self.interval_seconds)
        self.preferences_group.add(self.disable_yafti)
        self.preference.add(self.preferences_group)

        # TODO: clean up an hide.
        self._new_pref = Adw.PreferencesPage()
        self._new_perf_group = Adw.PreferencesGroup()
        self._new_perf_group.add(self.included_packages)
        self._new_pref.add(self.preferences_group)
        self.preference.add(self._new_perf_group)

        # TODO: clean up an hide.
        self._old_new_pref = Adw.PreferencesPage()
        self._old_new_perf_group = Adw.PreferencesGroup()
        self._old_new_perf_group.add(self.excluded_packages)
        self._old_new_pref.add(self.preferences_group)
        self.preference.add(self._old_new_perf_group)

        self.scrolled_window.set_child(self.preference)

    def set_content(self, button):
        """
        set_content sets the Settings pane content in the navigation split view
        """
        content = Gio.Application.get_default().split_view.get_content()
        content.set_title("Settings")
        content.set_visible(True)
        content.pane.set_content(self.scrolled_window)
        content.pane.set_reveal_bottom_bars(False)
