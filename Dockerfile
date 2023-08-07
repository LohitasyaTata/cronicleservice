FROM       cronicle-master:4
ENV        CRONICLE_VERSION 0.9.25
ENV        CRONICLE_base_app_url 'http://localhost:8080'
ENV        CRONICLE_WebServer__http_port 8080
ENV        CRONICLE_WebServer__https_port 443
ENV        EDITOR=nano

#RUN        apk add --no-cache nodejs npm git curl wget perl bash perl-pathtools tar procps nano tini python3
# RUN        mkdir -p /opt/cronicle \
#                 && cd /opt/cronicle \
#                 && curl -L https://github.com/jhuckaby/Cronicle/archive/v${CRONICLE_VERSION}.tar.gz | tar zxvf - --strip-components 1 \
#                 && npm install \
#                 && node bin/build.js dist \
#                 && rm -Rf /root/.npm

ADD       entrypoint.sh /entrypoint.sh
ADD       config.json /opt/cronicle/conf/config.json

# SHELL ["/bin/bash", "--login", "-c"]

# RUN apt-get install unzip
# RUN curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.38.0/install.sh | bash
# RUN nvm install v16.2.0 \
#     && nvm use v16.2.0

# Runtime user
# RUN        adduser cronicle -D -h /opt/cronicle
# RUN        adduser cronicle docker

WORKDIR    /opt/cronicle/


ADD       code.zip /home/bflmfuser/code.zip
# ADD       venv/ /home/bflmfuser/venv/
COPY      code/ps-verification-bflmfutilslib/PS-Verification-BFLMFutilsLib/ /bflmfutilslib
RUN       pip install -e /bflmfutilslib
# RUN       curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.1/install.sh | bash

EXPOSE     8080

# data volume is also configured in entrypoint.sh
VOLUME     ["/opt/cronicle/data", "/opt/cronicle/logs", "/opt/cronicle/plugins"]

CMD        ["/bin/sh", "/entrypoint.sh"]