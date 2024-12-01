FROM kong:latest

USER root

# Install envsubst
RUN apt-get update && \
    apt-get install -y gettext-base && \
    rm -rf /var/lib/apt/lists/*

# Copy config files
COPY kong.conf /etc/kong/kong.conf
COPY kong.yml /etc/kong/kong.yml.template
COPY docker-entrypoint.sh /docker-entrypoint.sh

RUN chmod +x /docker-entrypoint.sh && \
    chown -R kong:kong /etc/kong

USER kong

ENTRYPOINT ["/docker-entrypoint.sh"]