FROM redis:6.2

ARG REDIS_PORT

WORKDIR /redis-workdir

# Installing OS level dependencies
RUN apt-get update
RUN apt-get install -y wget
RUN apt-get install -y gettext-base

# Downloading redis default config
RUN wget https://raw.githubusercontent.com/redis/redis/6.2/redis.conf
RUN mv redis.conf redis.default.conf

COPY . .

ENV REDIS_PORT $REDIS_PORT
RUN envsubst < redis.conf > updated_redis.conf
RUN mv updated_redis.conf redis.conf

CMD redis-server ./redis.conf
