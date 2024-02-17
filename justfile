set shell := ["bash", "-uc"]

default:
  just --list

enter:
  distrobox-enter yaftibox

spinup-container:
  distrobox-assemble create --file yaftibox.ini

run-yafti :
  poetry run yafti tests/example.yml -f