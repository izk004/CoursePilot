from coursepilot.rag.vector_store import VectorStore


class FakeCollection:
    def __init__(self, count: int):
        self._count = count
        self.query_called = False
        self.query_kwargs = None

    def count(self):
        return self._count

    def query(self, **kwargs):
        self.query_called = True
        self.query_kwargs = kwargs
        return {
            "ids": [[]],
            "documents": [[]],
            "metadatas": [[]],
            "distances": [[]],
        }


def test_search_skips_query_when_the_index_is_empty():
    store = VectorStore.__new__(VectorStore)
    store.collection = FakeCollection(count=0)

    assert store.search("test question") == []
    assert store.collection.query_called is False


def test_search_limits_requested_results_to_index_size():
    store = VectorStore.__new__(VectorStore)
    store.collection = FakeCollection(count=1)

    store.search("test question", limit=12)

    assert store.collection.query_kwargs["n_results"] == 1
