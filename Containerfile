###
# This needs to be updated to use fedora
###
FROM python:3.11.8-bookworm
ENV REFRESHED_AT 2024/03/07

ADD . /tmp
WORKDIR /tmp

# install python requirements
RUN set -ex && \
    build_deps='curl gpg lsb-release' && \
    apt update && \
    apt install -y $build_deps --no-install-recommends && \
    curl -q 'https://proget.makedeb.org/debian-feeds/prebuilt-mpr.pub' | gpg --dearmor | tee /usr/share/keyrings/prebuilt-mpr-archive-keyring.gpg 1> /dev/null && \
    echo "deb [arch=amd64 signed-by=/usr/share/keyrings/prebuilt-mpr-archive-keyring.gpg] https://proget.makedeb.org prebuilt-mpr $(lsb_release -cs)" | tee /etc/apt/sources.list.d/prebuilt-mpr.list && \
    build_deps="${build_deps}" && \
    apt update && \
    apt install -y just --no-install-recommends && \
    pip install --upgrade pip poetry --no-cache && \
    just dev install && \
    apt purge -y --auto-remove $build_deps && \
    poetry build && \
    rm -rf /var/lib/apt/lists/*

VOLUME /tmp

RUN just build

################################
FROM python:3.11.4-slim-bookworm

# Application environment variables.
ENV APP_NAME="yafti"
ENV REFRESHED_AT="2024/03/07"
ENV USER="yafti"
ENV HOME="/app"

RUN set -ex && \
    apt-get update -y && \
    apt-get upgrade -y && \
    mkdir -p $HOME && \
    groupadd -r $USER &&  \
    useradd --no-log-init -r -g $USER $USER && \
    chown -R $USER $HOME && \
    rm -f /tmp/*

COPY --from=builder --chown=$USER /tmp/dist/ /tmp/dist

# Version needs to be updated dynamically etc.
RUN pip install /tmp/dist/yafti-0.1.0-py3-none-any.whl

USER $USER
WORKDIR $HOME

ENTRYPOINT ["yafti"]
