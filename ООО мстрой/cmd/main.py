"""Демо-скрипт: загрузка дерева из JSON и вызов методов TreeStore."""

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from configs.settings import settings
from internal.treestore.tree_store import TreeStore

with open(settings.data_file, encoding="utf-8") as f:
    items = json.load(f)

ts = TreeStore(items)

if __name__ == "__main__":
    print("get_all():")
    print(ts.get_all())
    print()

    print("get_item(7):")
    print(ts.get_item(7))
    print()

    print("get_children(4):")
    print(ts.get_children(4))
    print()

    print("get_children(5):")
    print(ts.get_children(5))
    print()

    print("get_all_parents(7):")
    print(ts.get_all_parents(7))
