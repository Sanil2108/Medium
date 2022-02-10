FROM redis:6.2

WORKDIR /redis-workdir

# Installing OS level dependencies
RUN apt-get update
RUN apt-get install -y wget

# Downloading redis default config
RUN wget https://raw.githubusercontent.com/redis/redis/6.2/redis.conf
RUN mv redis.conf redis.default.conf

COPY . .

CMD redis-server ./redis.conf
