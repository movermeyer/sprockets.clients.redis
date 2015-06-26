"""
Tests for the sprockets.clients.redis package

"""
import os
import time
import unittest
import uuid

from sprockets.clients.redis import ShardedRedisConnection, RedisConnection


class TestShardedRedisConnectionClass(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        super(TestShardedRedisConnectionClass, cls).setUpClass()
        cls._old_environ = os.environ.get('REDIS_URI', '')
        os.environ['REDIS_URI'] = 'redis://localhost?ttl=10'
        cls.conn = ShardedRedisConnection()

    @classmethod
    def tearDownClass(cls):
        super(TestShardedRedisConnectionClass, cls).tearDownClass()
        os.environ['REDIS_URI'] = cls._old_environ

    def setUp(self):
        self.key = uuid.uuid4().hex
        self.value = uuid.uuid4().hex
        super(TestShardedRedisConnectionClass, self).setUp()

    def test_saving_a_new_key(self):
        self.conn.set(self.key, self.value)
        self.assertEqual(self.conn.get(self.key), self.value)

    def test_deleting_a_key(self):
        self.conn.set(self.key, self.value)
        self.conn.delete(self.key)
        self.assertIsNone(self.conn.get(self.key))

    def test_expiring_a_key(self):
        self.conn.set(self.key, self.value, ttl=1)
        time.sleep(2)
        self.assertIsNone(self.conn.get(self.key))

    def test_adding_to_set_at_a_key(self):
        self.conn.sadd(self.key, self.value)
        self.assertEqual(self.conn.smembers(self.key), set([self.value]))

    def test_checking_membership_of_value_at_key(self):
        self.conn.sadd(self.key, self.value)
        self.assertTrue(self.conn.sismember(self.key, self.value))

    def test_getting_health_info(self):
        self.assertIsNotNone(self.conn.info())

    def test_bad_redis_uri(self):
        old = os.environ['REDIS_URI']
        os.environ['REDIS_URI'] = 'http://example.com'
        with self.assertRaises(Exception):
            ShardedRedisConnection()

        os.environ['REDIS_URI'] = old

    def test_bad_redis_hosts(self):
        old = os.environ['REDIS_URI']
        os.environ['REDIS_URI'] = 'redis://gooblegobble.foo.bar'

        conn = ShardedRedisConnection()
        self.assertEqual(conn.config.hosts, ['127.0.0.1'])

        os.environ['REDIS_URI'] = old


class TestRedisConnectionClass(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        super(TestRedisConnectionClass, cls).setUpClass()
        cls._old_environ = os.environ.get('REDIS_URI', '')
        os.environ['REDIS_URI'] = 'redis://localhost?ttl=10'
        cls.conn = RedisConnection()

    @classmethod
    def tearDownClass(cls):
        super(TestRedisConnectionClass, cls).tearDownClass()
        os.environ['REDIS_URI'] = cls._old_environ

    def setUp(self):
        self.key = uuid.uuid4().hex
        self.value = uuid.uuid4().hex
        super(TestRedisConnectionClass, self).setUp()

    def test_saving_a_new_key(self):
        self.conn.set(self.key, self.value)
        self.assertEqual(self.conn.get(self.key), self.value)

    def test_deleting_a_key(self):
        self.conn.set(self.key, self.value)
        self.conn.delete(self.key)
        self.assertIsNone(self.conn.get(self.key))

    def test_expiring_a_key(self):
        self.conn.set(self.key, self.value, ex=1)
        time.sleep(2)
        self.assertIsNone(self.conn.get(self.key))

    def test_adding_to_set_at_a_key(self):
        self.conn.sadd(self.key, self.value)
        self.assertEqual(self.conn.smembers(self.key), set([self.value]))

    def test_checking_membership_of_value_at_key(self):
        self.conn.sadd(self.key, self.value)
        self.assertTrue(self.conn.sismember(self.key, self.value))

    def test_getting_health_info(self):
        self.assertIsNotNone(self.conn.info())

    def test_bad_redis_uri(self):
        old = os.environ['REDIS_URI']
        os.environ['REDIS_URI'] = 'http://example.com'
        with self.assertRaises(Exception):
            RedisConnection()

        os.environ['REDIS_URI'] = old

    def test_bad_redis_hosts(self):
        old = os.environ['REDIS_URI']
        os.environ['REDIS_URI'] = 'redis://gooblegobble.foo.bar'
        with self.assertRaises(Exception):
            RedisConnection()

        os.environ['REDIS_URI'] = old
