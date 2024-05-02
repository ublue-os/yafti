# justfile docs https://just.systems/man/en/
# justfile cheatsheet https://cheatography.com/linux-china/cheat-sheets/justfile/
set dotenv-load := true
set export

project := "yafti"
host := `uname -a`
python_exe := `which python`
pip_exe := `which pip3`
project_path := invocation_directory()
module_path := join(project_path, 'yafti')

###
# need to add readme to docs and run a full suite of test etc
# absolute_path  parent_directory justfile_directory
# https://github.com/python-poetry/poetry python package and venv manager.
# https://unicode.org/emoji/charts/emoji-list.html#1fae1 emoji's
###
bt := '0'

export RUST_BACKTRACE_1 := bt
export JUST_LOG := "warn"

sys-info:
    @echo '{{host}}'

python:
    @echo 'Python:' `poetry run python --version`
    @echo 'Python Path:' `poetry env info`
    @echo 'Python Path:' `which python`
#
@dev deps="yes":
    pip install poetry pip --upgrade
    poetry install --with docs

build deps="yes": (dev deps)
    @echo "building wheel"
    poetry build

# set-hooks: dev
#    pre-commit
#    poetry run pre-commit install --install-hooks # uninstall: `pre-commit uninstall`

unit-test deps="no": (dev deps)
    @echo 'unit-tests'
    poetry run pytest --cov={{ module_path}} --cov-report=term-missing

type-checks deps="no": (dev deps)
    @echo 'type checking'
    poetry run mypy {{ module_path }}

format deps="no": (dev deps)
    @echo 'black isort and ruff being called into action'
    poetry run black {{ module_path }}
    poetry run isort {{ module_path }}
    poetry run ruff check {{ module_path }}

# TODO: i like flake8
#lint deps="no": (dev deps)
#    @echo "linting code base"
#    poetry run flake8 {{ module_path }} \
#    --max-line-length 100 \
#    --ignore=F401,E731,F403,E501,W503 \
#    --count

coverage-report:
    @echo "Building test coverage report"
    # poetry run pytest --cov=yafti --cov-report=term-missing
    poetry run pytest --cov={{ module_path }}  --cov-config=.coveragerc --cov-report html

sphinx deps="no": (dev deps)
    @echo "Building application documentation"
    mkdir -p docs/html
    touch docs/.nojekyll
    cd docs/ && poetry run sphinx-build -b html . _build
    cp -r docs/_build/* docs/html

docs deps="no": (dev deps)
    @echo "Run auto build and start http server."
    poetry run sphinx-autobuild docs docs/_build/html

run deps="no": (dev deps)
    # not sure why GTK_IM_MODULE is required in the distrobox.  I need to test on a physical installation.
    export GTK_IM_MODULE=ibus
    # poetry run python -m {{ project }}.cli start tests/bazzite.yaml --debug -f
    poetry run python -m {{ project }}.cli start tests/bluefin.yml --debug -f
    # poetry run python -m {{ project }}.cli start tests/example.yml --debug

create-distrobox:
  distrobox-assemble create --file {{ project_path }}/distrobox.ini

enter-distrobox:
  distrobox-enter yaftibox

help:
    just -l


###
# Need to add a just command for glib-compile-schemas
###

###
# Add just command for running act local github runners
###

###
# gnome extension mangement.
# https://github.com/essembeh/gnome-extensions-cli/
###

