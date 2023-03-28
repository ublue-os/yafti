---
hide:
  - navigation
  - toc
  - path
  - title
---

# Yet another first time installer

![](/assets/logo.png)

This application is responsible for installing Flatpaks on first boot after a user finishes installation. 
It is intended as a replacement for custom zenity dialogs. 

## Project goals

* Config file driven via JSON/YAML
* Support for arbitrary pre and post-install commands
* Configuration driven screens
* Screen independent state management with ability to set defaults
* Extensible with drop-in Python classes / plugins to extend functionality
