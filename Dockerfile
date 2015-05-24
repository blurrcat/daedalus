FROM python:3.4-onbuild
MAINTAINER blurrcat <blurrcat@gmail.com>
ENV WEB_CONCURRENCY 1
CMD gunicorn -b 0.0.0.0:8000 -k gaiohttp --access-logfile "-" \
    --access-logformat '[%(t)]s%(h)s %(l)s "%(r)s" %(s)s %(b)s "%(f)s" "%(a)s"' \
    "daedalus.app:create_app()"
