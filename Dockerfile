FROM registry.access.redhat.com/ubi8/ubi:8.5 as builder

# hadolint ignore=DL3033
RUN set -ex \
    && mkdir -p /mnt/rootfs \
    && yum install -y \
        --setopt install_weak_deps=false \
        --nodocs \
        python39 \
        python39-pip \
    && yum install -y \
        --installroot=/mnt/rootfs \
        --releasever=8 \
        --setopt install_weak_deps=false \
        --nodocs \
        curl \
        # required by fedmsg (zmq)
        libstdc++ \
        python39 \
    && yum --installroot=/mnt/rootfs clean all \
    && rm -rf /mnt/rootfs/var/cache/* /mnt/rootfs/var/log/dnf* /mnt/rootfs/var/log/yum.*

ARG GITHUB_REF
ARG GITHUB_SHA

ENV \
    GITHUB_REF=$GITHUB_REF \
    GITHUB_SHA=$GITHUB_SHA \
    PIP_DEFAULT_TIMEOUT=100 \
    PIP_DISABLE_PIP_VERSION_CHECK=1 \
    PIP_NO_CACHE_DIR=1 \
    PYTHONFAULTHANDLER=1 \
    PYTHONHASHSEED=random \
    PYTHONUNBUFFERED=1

WORKDIR /build
COPY . .
# hadolint ignore=SC1091
RUN set -ex \
    && pip3 install --no-cache-dir -r requirements-builder.txt \
    && python3 -m venv /venv \
    && . /venv/bin/activate \
    && pip install --no-cache-dir -r requirements-builder2.txt \
    && version=$(./get-version.sh) \
    && test -n "$version" \
    && poetry version "$version" \
    && poetry build \
    && pip install --no-cache-dir dist/greenwave-"$version"-py3*.whl \
    && deactivate \
    && mv /venv /mnt/rootfs \
    && mkdir -p /mnt/rootfs/src/docker \
    && cp -v docker/docker-entrypoint.sh /mnt/rootfs/src/docker \
    && cp -vr conf /mnt/rootfs/src

# --- Final image
FROM scratch
ARG GITHUB_SHA
LABEL \
    summary="Greenwave application" \
    description="Decision-making service for gating in a software delivery pipeline." \
    maintainer="Red Hat, Inc." \
    license="GPLv2+" \
    url="https://github.com/release-engineering/greenwave" \
    vcs-type="git" \
    vcs-ref=$GITHUB_SHA \
    io.k8s.display-name="Greenwave"

ENV \
    PYTHONFAULTHANDLER=1 \
    PYTHONHASHSEED=random \
    PYTHONUNBUFFERED=1 \
    WEB_CONCURRENCY=8

COPY --from=builder /mnt/rootfs/ /
COPY --from=builder /etc/yum.repos.d/ubi.repo /etc/yum.repos.d/ubi.repo
WORKDIR /src

# This will allow a non-root user to install a custom root CA at run-time
RUN chmod 777 /etc/pki/tls/certs/ca-bundle.crt

USER 1001
EXPOSE 8080
ENTRYPOINT ["/src/docker/docker-entrypoint.sh"]
CMD ["gunicorn", "--bind", "0.0.0.0:8080", "--access-logfile", "-", "--enable-stdio-inheritance", "greenwave.wsgi:app"]
