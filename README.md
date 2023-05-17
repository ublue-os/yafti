# Yet Another First Time Installer

This application is responsible for installing Flatpaks on first boot after a user finishes installation. 
It is intended as a replacement for custom zenity dialogs. 

## Project goals

* Config file driven via JSON/YAML
* Support for arbitrary pre and post-install commands
* Configuration driven screens
* Screen independent state management with ability to set defaults
* Extensible with drop-in Python classes / plugins to extend functionality

## Core features

These are goals for each feature of the first time installer:

### Title Screen

The Title screen will be comprised of three primary elements. An image/icon, a header/primary text, and a paragraph description text.

```

         ICON
      TITLE TEXT

  this is a description
  to accompany the title
  screen.
```

### Packages screen

Display several groups of packages to install, allow for expansion of each group to individually select discrete packages or toggle the entire group on/off.

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

The application then installs the Flatpaks. Plugins for other packages systems may/can be developed.

### Configuration

```yaml
title: uBlue First Boot
properties:
  mode: "run-on-change"
  path: "~/.config/yafti/last-run"
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
      title: Package Installation
      show_terminal: true
      package_manager: yafti.plugin.flatpak
      groups:
        Core:
          description: All the good stuff
          packages:
          - Calculator: org.gnome.Calculator
          - Firefox: org.mozilla.firefox
        Gaming:
          description: GAMES GAMES GAMES
          packages:
          - Steam: com.valvesoftware.Steam
          - Games: org.gnome.Games
        Office:
          description: All the work stuff
          packages:
          - LibreOffice: org.libreoffice.LibreOffice
          - Calendar: org.gnome.Calendar
  final-screen:
    source: yafti.screen.title
    values:
      title: "All done"
      icon: "/path/to/icon"
      description: |
        Thanks for installing, join the community, next steps
```

## Development

This project uses Poetry and Python 3.11. Make sure you have Python 3.11 and [Poetry installed](https://python-poetry.org/docs/). Checkout the repository and navigate to root project directory.

### Prerequisites

If you're on a Ublue / immutable OS, you'll need to run these and the poetry install in a toolbox.

```
sudo dnf install python3-devel cairo-devel gobject-introspection-devel cairo-gobject-devel
poetry install
```

### Running

```
poetry run python -m yafti tests/example.yml
```

This will launch the Yafti window.

#### Running from a Containerfile

One of yafti's main use cases is to be used in Containerfiles to handle installation of Flatpaks on first boot.
Add this to your Containerfile to add yafti to your image:

    RUN pip install --prefix=/usr yafti
    
Additionally, you need a script to copy over the .desktop file to the user's home directory:
- [Example firstboot script](https://github.com/ublue-os/bluefin/blob/main/etc/profile.d/bluefin-firstboot.sh)
- [Example firstboot .desktop file](https://github.com/ublue-os/bluefin/blob/main/etc/skel.d/.config/autostart/bluefin-firstboot.desktop)

Then add a file in `/etc/yafti.yml` with your customizations. Check the [example file](https://github.com/ublue-os/yafti/blob/main/tests/example.yml) for ideas. 

### Testing

This project uses pytest, black, isort, and ruff for testing and linting.

```
poetry run pytest --cov=yafti --cov-report=term-missing
poetry run black yafti
poetry run isort yafti
poetry run ruff yafti
```

## Contributing

This project follows a fork and pull request syle of contribution.

### Creating a Fork

Just head over to the GitHub page and [click the "Fork" button](https://help.github.com/articles/fork-a-repo). Once you've done that, you can use your favorite git client to clone your repo or just head straight to the command line:

```shell
# Clone your fork to your local machine
git clone git@github.com:USERNAME/FORKED-PROJECT.git
```

### Keeping Your Fork Up to Date

While this isn't an absolutely necessary step, if you plan on doing anything more than just a tiny quick fix, you'll want to make sure you keep your fork up to date by tracking the original "upstream" repo that you forked. You can do this by using [the Github UI](https://help.github.com/articles/syncing-a-fork) or locally by adding this repo as an upstream.

```shell
# Add 'upstream' repo to list of remotes
git remote add upstream https://github.com/ublue-os/yafti.git

# Verify the new remote named 'upstream'
git remote -v
```

Whenever you want to update your fork with the latest upstream changes, you'll need to first fetch the upstream repo's branches and latest commits to bring them into your repository:

```shell
# Fetch from upstream remote
git fetch upstream

# View all branches, including those from upstream
git branch -va
```

Now, checkout your own main branch and merge the upstream repo's main branch:

```shell
# Checkout your main branch and merge upstream
git checkout main
git merge --ff-only upstream/main
```

If there are no unique commits on the local main branch, git will simply perform a fast-forward. However, if you have been making changes on main (in the vast majority of cases you probably shouldn't be - [see the next section](#doing-your-work), you may have to deal with conflicts. When doing so, be careful to respect the changes made upstream.

Now, your local main branch is up-to-date with everything modified upstream.

### Doing Your Work

#### Create a Branch

Whenever you begin work on a new feature or bugfix, it's important that you create a new branch. Not only is it proper git workflow, but it also keeps your changes organized and separated from the main branch so that you can easily submit and manage multiple pull requests for every task you complete.

To create a new branch and start working on it:

```shell
# Checkout the main branch - you want your new branch to come from main
git checkout main

# Create a new branch named newfeature (give your branch its own simple informative name)
git checkbout -b newfeature
```

Now, go to town hacking away and making whatever changes you want to.

#### Commit Messages

We use [Conventional Commits](https://www.conventionalcommits.org/en/v1.0.0/) and enforce them with a bot to keep the changelogs tidy:

```
chore: add Oyster build script
docs: explain hat wobble
feat: add beta sequence
fix: remove broken confirmation message
refactor: share logic between 4d3d3d3 and flarhgunnstow
style: convert tabs to spaces
test: ensure Tayne retains clothing
```

If you have multiple commits, when [submitting your chages](#submitting-a-pull-request), make sure to use a conventional commit style PR title as this project does squash merges and that will be used as your contribution.

### Submitting a Pull Request

#### Cleaning Up Your Work

Prior to submitting your pull request, you might want to do a few things to clean up your branch and make it as simple as possible for the original repo's maintainer to test, accept, and merge your work.

If any commits have been made to the upstream main branch, you should rebase your feature branch so that merging it will be a simple fast-forward that won't require any conflict resolution work.

```shell
# Fetch upstream main and merge with your repo's main branch
git fetch upstream
git checkout main
git merge upstream/main

# If there were any new commits, rebase your feature branch
git checkout newfeature
git rebase main
```

#### Submitting

Once you've committed and pushed all of your changes to GitHub, go to the page for your fork on GitHub, select your feature branch, and click the pull request button. If you need to make any adjustments to your pull request, just push the updates to GitHub. Your pull request will automatically track the changes on your feature branch and update.

### Accepting and Merging a Pull Request

Take note that unlike the previous sections which were written from the perspective of someone that created a fork and generated a pull request, this section is written from the perspective of the original repository owner who is handling an incoming pull request. Thus, where the "forker" was referring to the original repository as `upstream`, we're now looking at it as the owner of that original repository and the standard `origin` remote.

#### Checking Out and Testing Pull Requests

There are multiple ways to [check out a pull request locally](https://help.github.com/articles/checking-out-pull-requests-locally). This way uses standard git operations to complete. Open up the `.git/config` file and add a new line under `[remote "origin"]`:

```
fetch = +refs/pull/*/head:refs/pull/origin/*
```

Now you can fetch and checkout any pull request so that you can test them:

```shell
# Fetch all pull request branches
git fetch origin

# Checkout out a given pull request branch based on its number
git checkout -b 9001 pull/origin/9001
```

Keep in mind that these branches will be read only and you won't be able to push any changes.

#### Automatically Merging a Pull Request
In cases where the merge would be a simple fast-forward, you can automatically do the merge by  clicking the button on the pull request page on GitHub.
