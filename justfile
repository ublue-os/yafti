set shell := ["bash", "-uc"]

default:
  just --list

create-yaftibox:
  distrobox-assemble create --file yaftibox.ini
  just yaftibox

enter-yaftibox:
  distrobox-enter yaftibox

yafti :
  poetry run yafti tests/example.yml -f