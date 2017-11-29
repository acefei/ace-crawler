#!/usr/bin/env python
# encoding: utf-8
"""
@author: Acefei
@file: redis_migration.py
@time: 17-11-27
"""
import redis
import docopt

TYPE2SIZE = {
    'set': 'scard',
    'zset': 'zcard',
    'list': 'llen',
    'hash': 'hlen',
}

TYPE2GET = {
    'set': ['smembers'],
    'zset': ['zrange', 0, -1, False, True],
    'list': ['lrange', 0, -1],
    'hash': ['hgetall'],
}

TYPE2PUT = {
    # key_type: [method_name, value_in_list_format]
    'hash': ['hmset', lambda x: [x]],
    'list': ['lpush', lambda x: x],
    'set': ['sadd', lambda x: list(x)],
    'zset': ['zadd', lambda x: list(sum(x, ()))],
}


class RedisMigration(object):
    """
    Migrates all of the key/values for a given Redis server to
    another. (Inspired by https://github.com/team-labs/redis-migrate/blob/master/redis_migrate.py)
    Currently only supports:
    - List
    - Set
    - Hash
    - SortedSet
    """
    def __init__(self, from_url, to_url):
        self.f_redis = self.redis_conn(from_url)
        self.t_redis = self.redis_conn(to_url)

    @staticmethod
    def redis_conn(url):
        return redis.from_url(url)

    @staticmethod
    def size(redis_conn, key, type):
        func = TYPE2SIZE[type]
        size = getattr(redis_conn, func)(key)
        return size

    def get_keys(self):
        """
        Returns the keys for a given redis connection
        """
        return self.f_redis.keys()

    def get_types(self, keys):
        """
        Returns a list of types for a list of keys in redis
        """
        # if there's for loop, use pipeline to accelerate the processing
        if isinstance(keys, str):
            keys = [keys]

        pipeline = self.f_redis.pipeline()
        for key in keys:
            pipeline.type(key)
        return pipeline.execute()

    def get_values(self, keys, types):
        """
        Gets the values for a set of keys and their types
        """
        pipeline = self.f_redis.pipeline()
        for k, t in zip(keys, types):
            func = TYPE2GET[t][0]
            args = [k] + TYPE2GET[t][1:]
            getattr(pipeline, func)(*args)
        return pipeline.execute()

    def migrate(self, key=None):
        """
        Uploads the given data to the given redis database connection
        """
        if key is None:
            keys = self.get_keys()
            types = self.get_types(keys)
            values = self.get_values(keys, types)
        else:
            keys = [key]
            types = [self.f_redis.type(key)]
            values = self.get_values(keys, types)

        pipeline = self.t_redis.pipeline()
        for k, t, v in zip(keys, types, values):
            # print k,t,v
            func = TYPE2PUT[t][0]
            args = [k] + TYPE2PUT[t][1](v)
            getattr(pipeline, func)(*args)

        pipeline.execute()


def usage():
    """Migrate data between redis servers, the redis url format is redis://[:password@]host[:port][/db-number]
    Usage:
        redis_migration.py -f FROM_REDIS_URL -t TO_REDIS_URL [-k REDIS_KEY]

    Options:
        -f FROM_REDIS_URL   redis server url for migrating from
        -t TO_REDIS_URL   redis server url for migrating to
        -k REDIS_KEY   redis key name
    """


if __name__ == "__main__":
    args = docopt.docopt(usage.__doc__)
    f_redis = args.get('-f')
    t_redis = args.get('-t')
    r_key = args.get('-k')
    mdd = RedisMigration(f_redis, t_redis)
    if r_key is not None:
        key_type = mdd.f_redis.type(r_key)
        f_size = mdd.size(mdd.f_redis, r_key, key_type)
        t_size = mdd.size(mdd.t_redis, r_key, key_type)
        print "Before migration: {0} in src_redis, {1} in dst_redis".format(f_size, t_size)
        mdd.migrate(r_key)
        print "After migration: {0} in dst_redis.".format(mdd.size(mdd.t_redis, r_key, key_type))
    else:
        mdd.migrate()
