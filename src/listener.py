from caches import cache
from caches import channel

pubsub = cache.pubsub()
pubsub.psubscribe(channel)

print('start listening')

def event_handler(msg):
    print(msg)
    listen_thread.stop()
    print('listen_thread complete')

pubsub = cache.pubsub()
pubsub.psubscribe(**{channel: event_handler})
listen_thread = pubsub.run_in_thread(sleep_time=0.01)