#!/bin/bash
set -e

DAEDALUS_REDIS_DSN="${DAEDALUS_REDIS_DSN:=redis://127.0.0.1}"

case "$1" in
    web)
        gunicorn -b 0.0.0.0:8000 -k gaiohttp --access-logfile "-" \
    --access-logformat '[%(t)s]%(h)s %(l)s "%(r)s" %(s)s %(b)s "%(f)s" "%(a)s"' \
    "daedalus.app:create_app()"
        ;;
    worker)
        rq worker -u ${DAEDALUS_REDIS_DSN} -v
        ;;
    *)
        echo "usage: [web|worker]"
        exit -1
esac
