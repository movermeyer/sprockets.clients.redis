Examples
========
The following example ...

.. code:: python

    import os
    os.environ['REDIS_URI'] = 'redis://localhost/'

    shard = ShardedRedisConnection()

    shard.set('foo', 1)
    value = shard.get('foo')
    shard.delete('foo')
