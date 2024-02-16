# just for local development

set shell := ["bash", "-uc"]

default:
  just --list

test :
  poetry run yafti tests/example.yml -f