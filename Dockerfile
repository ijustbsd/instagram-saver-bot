FROM alpine

ADD script/entrypoint.sh /entrypoint.sh

ADD requirements.txt /requirements.txt

RUN \
    apk add --update --no-cache python3 py3-pip && \
    pip3 install --upgrade pip && \
    pip3 install -r requirements.txt && \
    chmod +x /entrypoint.sh && \
    rm -rf /var/cache/apk/*

CMD ["/entrypoint.sh"]