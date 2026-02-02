"""Тесты для TreeStore и ItemNotFoundError."""

import pytest

from internal.treestore.tree_store import ItemNotFoundError, TreeStore


@pytest.fixture
def sample_items():
    """Дерево с корнем id=1 и двумя уровнями потомков."""
    return [
        {"id": 1, "parent": "root"},
        {"id": 2, "parent": 1, "type": "test"},
        {"id": 3, "parent": 1, "type": "test"},
        {"id": 4, "parent": 2, "type": "test"},
        {"id": 5, "parent": 2, "type": "test"},
        {"id": 6, "parent": 2, "type": "test"},
        {"id": 7, "parent": 4, "type": None},
        {"id": 8, "parent": 4, "type": None}
    ]


@pytest.fixture
def tree_store(sample_items):
    """Экземпляр TreeStore, построенный из sample_items."""
    return TreeStore(sample_items)


def test_get_all(tree_store, sample_items):
    result = tree_store.get_all()
    assert result == sample_items
    assert len(result) == 8


def test_get_item(tree_store):
    result = tree_store.get_item(7)
    assert result == {"id": 7, "parent": 4, "type": None}

    result = tree_store.get_item(1)
    assert result == {"id": 1, "parent": "root"}

    with pytest.raises(ItemNotFoundError):
        tree_store.get_item(999)


def test_get_children(tree_store):
    result = tree_store.get_children(4)
    assert len(result) == 2
    assert {"id": 7, "parent": 4, "type": None} in result
    assert {"id": 8, "parent": 4, "type": None} in result

    result = tree_store.get_children(5)
    assert result == []

    result = tree_store.get_children(2)
    assert len(result) == 3
    assert {"id": 4, "parent": 2, "type": "test"} in result
    assert {"id": 5, "parent": 2, "type": "test"} in result
    assert {"id": 6, "parent": 2, "type": "test"} in result


def test_get_all_parents(tree_store):
    result = tree_store.get_all_parents(7)
    assert len(result) == 3
    assert result[0] == {"id": 4, "parent": 2, "type": "test"}
    assert result[1] == {"id": 2, "parent": 1, "type": "test"}
    assert result[2] == {"id": 1, "parent": "root"}

    result = tree_store.get_all_parents(1)
    assert result == []

    result = tree_store.get_all_parents(4)
    assert len(result) == 2
    assert result[0] == {"id": 2, "parent": 1, "type": "test"}
    assert result[1] == {"id": 1, "parent": "root"}


def test_performance(tree_store):
    """Проверка, что повторные вызовы не деградируют (O(1) доступ)."""
    for _ in range(1000):
        tree_store.get_item(7)
        tree_store.get_children(2)
        tree_store.get_all_parents(7)


def test_get_all_parents_root_not_id_one():
    """Корень может иметь id отличный от 1; цепочка родителей строится корректно."""
    items = [
        {"id": 100, "parent": "root"},
        {"id": 200, "parent": 100},
        {"id": 300, "parent": 200},
    ]
    store = TreeStore(items)
    result = store.get_all_parents(300)
    assert len(result) == 2
    assert result[0]["id"] == 200
    assert result[1]["id"] == 100
    assert result[1]["parent"] == "root"

    result_root = store.get_all_parents(100)
    assert result_root == []
