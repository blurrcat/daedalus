#!/bin/bash
set -e

export DAEDALUS_REDIS_URL="${DAEDALUS_REDIS_URL:=redis://127.0.0.1}"
export RQ_REDIS_URL=${DAEDALUS_REDIS_URL}

case "$1" in
    web)
        gunicorn -b 0.0.0.0:8000 -k gaiohttp --access-logfile "-" \
    --access-logformat '[%(t)s]%(h)s %(l)s "%(r)s" %(s)s %(b)s "%(f)s" "%(a)s"' \
    "daedalus.web.main:create_app()"
        ;;
    worker)
        rq worker -c daedalus.config
        ;;
    *)
        exec "$@"
        ;;
esac
