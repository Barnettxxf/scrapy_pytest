"""
Just for ymspider
"""

import pytest


@pytest.fixture(autouse=True)
def scheduler(monkeypatch):
    def fake_publish(*args, **kwargs):
        pass

    def fake_ack(*args, **kwargs):
        pass

    def fake_nack(*args, **kwargs):
        pass

    monkeypatch.setattr('scheduler.Scheduler.publish', fake_publish)
    monkeypatch.setattr('scheduler.Scheduler.ack', fake_ack)
    monkeypatch.setattr('scheduler.Scheduler.fake_nack', fake_nack)


@pytest.fixture(autouse=True)
def monitor(monkeypatch):
    class FakeMonitor:
        def inc(self, *args, **kwargs):
            pass

        def labels(self, *args, **kwargs):
            return FakeMonitor()

        def counter(self, *args, **kwargs):
            return FakeMonitor()

    monkeypatch.setattr('scrapy.Spider.monitor', FakeMonitor(), raising=False)
    monkeypatch.setattr('cyborg.downloaders.scrapy.IdleSpider.monitor', FakeMonitor(), raising=False)
