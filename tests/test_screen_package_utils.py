from yafti.screen.package.utils import parse_packages


def test_parse_packages_groups():
    cfg = {
        "Core": {
            "description": "hello world",
            "packages": [
                {"Calculator": "org.gnome.Calculator"},
                {"Firefox": "org.mozilla.firefox"},
            ],
        },
        "Gaming": {
            "description": "hello games",
            "default": False,
            "packages": [
                {"Steam": "com.valvesoftware.Steam"},
                {"Games": "org.gnome.Games"},
            ],
        },
    }

    expected = {
        "group:Core": True,
        "pkg:org.gnome.Calculator": True,
        "pkg:org.mozilla.firefox": True,
        "group:Gaming": True,
        "pkg:com.valvesoftware.Steam": True,
        "pkg:org.gnome.Games": True,
    }

    assert expected == parse_packages(cfg)


def test_parse_packages_list():
    cfg = [
        {"Calculator": "org.gnome.Calculator"},
        {"Firefox": "org.mozilla.firefox"},
        {"Steam": "com.valvesoftware.Steam"},
        {"Games": "org.gnome.Games"},
    ]

    expected = {
        "pkg:org.gnome.Calculator": True,
        "pkg:org.mozilla.firefox": True,
        "pkg:com.valvesoftware.Steam": True,
        "pkg:org.gnome.Games": True,
    }

    assert expected == parse_packages(cfg)
