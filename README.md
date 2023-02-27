# Yet another first time installer

## Project goals

* Config (YAML/JSON) file driven
* Support for pre-install and post-install arbitrary commands
* Configuration driven screens
* Screen independent state management with ability to set defaults
* Extensible with drop-in python classes / plugins to extend functionality

## Core features

These are goals for each feature of the first time installer

### Title screen

Title screen will be comprised of three primary elements. An image/icon, a header/primary text, and a paragraph description text.

```

         ICON
      TITLE TEXT

  this is a description
  to accompany the title
  screen.
```

### Packages screen

Display several groups of packages to install, allow for expansion of each group to individually select descrete packages or toggle the entire group on/off.

eg:
```
Core                [/] >
Gaming              [/] >
Office              [/] >
```

Expanding Core would reveal

```
Core                [/] v
  firefox           [x]
  calculator        [x]
  text editor       [x]
  clocks            [x]
  fonts             [x]
Gaming              [/] >
Office              [/] >
```

By default these will be flatpaks. Plugins for other packages systems may/can be developed.


### Configuration

```yaml
title: uBlue First Boot
actions:
  pre:
  - run: /full/path/to/bin --with --params
  - run: /another/command run
  - yafti.plugin.flatpak:
      install: org.gnome.Calculator
  post:
  - run: /run/these/commands --after --all --screens
screens:
  first-screen:
    source: yafti.screen.title
    values:
      title: "That was pretty cool"
      icon: "/path/to/icon"
      description: |
        Time to play overwatch
  applications:
    source: yafti.screen.package
    values:
      show_terminal: true
      package_manager: yafti.plugin.flatpak
      Core:
      - Calculator: org.gnome.Calculator
      - Firefox: org.mozilla.firefox
      Gaming:
      - Steam: com.valvesoftware.Steam
      - Games: org.gnome.Games
      Office:
      - LibreOffice: org.libreoffice.LibreOffice
      - Calendar: org.gnome.Calendar
  final-screen:
    source: yafti.screen.title
    values:
      title: "All done"
      icon: "/atph/to/icon"
      description: |
        Thanks for installing, join the community, next steps
```
