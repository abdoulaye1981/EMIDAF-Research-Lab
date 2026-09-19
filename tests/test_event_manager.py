from emidaf_core.managers.event_manager import EventManager


def test_manager_creation():

    manager = EventManager()

    assert manager is not None


def test_subscribe():

    manager = EventManager()

    def callback(value):
        pass

    manager.subscribe("TEST_EVENT", callback)

    assert manager.exists("TEST_EVENT")
    assert manager.subscribers("TEST_EVENT") == 1


def test_duplicate_subscribe():

    manager = EventManager()

    def callback(value):
        pass

    manager.subscribe("TEST_EVENT", callback)
    manager.subscribe("TEST_EVENT", callback)

    assert manager.subscribers("TEST_EVENT") == 1


def test_publish():

    manager = EventManager()

    results = []

    def callback(value):
        results.append(value)

    manager.subscribe("TEST_EVENT", callback)

    manager.publish("TEST_EVENT", "OK")

    assert results == ["OK"]


def test_unsubscribe():

    manager = EventManager()

    def callback(value):
        pass

    manager.subscribe("TEST_EVENT", callback)

    assert manager.subscribers("TEST_EVENT") == 1

    manager.unsubscribe("TEST_EVENT", callback)

    assert manager.subscribers("TEST_EVENT") == 0


def test_list():

    manager = EventManager()

    def callback(value):
        pass

    manager.subscribe("EVENT_A", callback)
    manager.subscribe("EVENT_B", callback)

    events = manager.list()

    assert isinstance(events, list)
    assert "EVENT_A" in events
    assert "EVENT_B" in events


def test_clear():

    manager = EventManager()

    def callback(value):
        pass

    manager.subscribe("EVENT_A", callback)
    manager.subscribe("EVENT_B", callback)

    manager.clear()

    assert manager.list() == []
