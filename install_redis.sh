#!/bin/bash

wget   http://download.redis.io/releases/redis-4.0.1.tar.gz
tar xzf redis-4.0.1.tar.gz
cd redis-4.0.1
make

##启动redis
nohup  src/redis-server  > /dev/null  2>&1  &


