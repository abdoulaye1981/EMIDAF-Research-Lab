from collections import defaultdict


class EventManager:

    def __init__(self):

        self._events = defaultdict(list)

    # ==========================================================
    # Abonnement
    # ==========================================================

    def subscribe(self, event_name, callback):

        if callback not in self._events[event_name]:

            self._events[event_name].append(callback)

    # ==========================================================
    # Désabonnement
    # ==========================================================

    def unsubscribe(self, event_name, callback):

        if callback in self._events[event_name]:

            self._events[event_name].remove(callback)

    # ==========================================================
    # Publication
    # ==========================================================

    def publish(self, event_name, *args, **kwargs):

        for callback in self._events[event_name]:

            callback(*args, **kwargs)

    # ==========================================================
    # Nettoyage
    # ==========================================================

    def clear(self):

        self._events.clear()

    # ==========================================================
    # Informations
    # ==========================================================

    def exists(self, event_name):

        return event_name in self._events

    def list(self):

        return list(self._events.keys())

    def subscribers(self, event_name):

        return len(self._events[event_name])