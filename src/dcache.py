import sys
import time
import diskcache
import threading

from caches import cache
from caches import channel

dc = diskcache.Deque()

class CWEThreadUpdater(threading.Thread):
    def __init__(self, callback=None, callback_args=None, *args, **kwargs):
        target = kwargs.pop('target')
        super(CWEThreadUpdater, self).__init__(target=self.target_with_callback, *args, **kwargs)
        self.callback = callback
        self.method = target
        self.callback_args = callback_args

    def target_with_callback(self):
        self.method()
        if self.callback is not None:
            self.callback(self.callback)


def update_cwe_job():
    print('start modelling of CWE updater')
    for i in range(0, 10):
        payload = dict(
            source='cwe',
            data=dict(
                id=i,
                message="tests message N %s" % (i)
            )
        )
        dc.append(payload)
        time.sleep(1)
    print('complete CWE updater')


def update_cwe_callback(args):
    print('Now in diskcache {} elements'.format(len(dc)))
    notify_redis_cache()

def notify_redis_cache():
    message = dict(
        source='cwe',
        status='complete',
        length=len(dc)
    )
    cache.publish(channel, message)

def main(args):
    thr = CWEThreadUpdater(
        name='cwe',
        target=update_cwe_job,
        callback=update_cwe_callback,
        callback_args=args
    )
    thr.start()
    print('work complete...')
    return 0


if __name__ == '__main__':
    sys.exit(main([]))