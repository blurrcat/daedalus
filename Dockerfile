FROM python:3.4-onbuild
MAINTAINER blurrcat <blurrcat@gmail.com>

ENV WEB_CONCURRENCY=1 \
    DAEDALUS_REDIS_URL=redis://127.0.0.1:6379/0 \
    DAEDALUS_DEBUG=False
EXPOSE 8000

RUN pip install -e .

ENTRYPOINT ["./entry.sh"]
CMD ["web"]
