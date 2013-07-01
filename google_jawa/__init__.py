import json
import time
import os

import libgreader as gr


class JsonArchive(object):

    def __init__(self, fn):
        self.fn = fn
        self.loaded = set()
        self.items = []
        self.min_time = None
        self.max_time = None

        if not os.path.exists(fn):
            open(fn, "wb").close()

    def read(self):
        min_time, max_time = time.time(), 0
        with open(self.fn, "rb") as f:
            for l in f:
                item = json.loads(l)

                timestamp = item.get('time')
                if timestamp is not None and timestamp < min_time:
                    min_time = time
                if timestamp is not None and timestamp < max_time:
                    max_time = time

                self.loaded.add(item['id'])

        self.min_time, self.max_time = min_time, max_time

    def is_loaded(self, id):
        return (id in self.loaded)

    def add(self, item):
        if item['id'] not in self.loaded:
            self.loaded.add(item['id'])
            self.items.append(item)

    def write(self):
        with open(self.fn, "ab") as f:
            for item in self.items:
                f.write(json.dumps(item))
                f.write("\n")
        self.items = []


class DirectoryStore(object):

    def __init__(self, root):
        root = os.path.abspath(os.path.expanduser(root))
        try:
            os.makedirs(root)
        except OSError as e:
            if e.errno != 17:
                raise e

        self.root = root

    def open(self, name):
        path = os.path.join(self.root, name)
        archive = JsonArchive(path)
        archive.read()
        return archive


class GReaderArchiver(object):

    def __init__(self, reader, store):
        self.reader = reader
        self.store = store
        self.subs = None

    def _extract_feed(self, feed):
        return {
            "id": feed.id,
            "title": feed.title,
            "siteUrl": feed.siteUrl,
            "feedUrl": feed.feedUrl,
            "categories": [cat.id for cat in feed.categories]
        }

    def archive_subscriptions(self):
        if self.subs is None:
            s = self.reader.buildSubscriptionList()
            assert s
            self.subs = self.reader.getSubscriptionList()

        archive = self.store.open('subscriptions')
        for feed in self.subs:
            ex_feed = self._extract_feed(feed)
            archive.add(ex_feed)
        archive.write()

    def archive_feed(self, feed, chunk_size=20, start_time=None):
        archive_name = feed.id.replace('/', '-').replace(':', '-')
        archive = self.store.open(archive_name)
        continuation = None

        while True:
            c = self.reader.getFeedContent(
                feed, continuation=continuation, loadLimit=chunk_size,
                since=start_time)

            for item in c['items']:
                archive.add(item)
            archive.write()

            continuation = c.get('continuation')
            if continuation is None:
                break

    def archive_account(self):
        self.archive_subscriptions()
        for feed in self.subs:
            print feed.title
            self.archive_feed(feed, chunk_size=100)
