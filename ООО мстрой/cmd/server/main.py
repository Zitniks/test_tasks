"""Эндпоинты FastAPI для TreeStore: загрузка данных из JSON, роуты дерева и health."""

import json
from pathlib import Path
from typing import Any

from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel

from api.schemas.tree import TreeStoreRequest, TreeStoreResponse
from configs.settings import settings
from internal.treestore.tree_store import ItemNotFoundError, TreeStore

app = FastAPI(title="TreeStore API", version="1.0.0")


def load_items_from_json(path: Path) -> list[dict[str, Any]]:
    """Загружает массив элементов из JSON-файла."""
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def get_tree_store() -> TreeStore:
    """Возвращает текущий экземпляр TreeStore, инициализированный из data_file."""
    items = load_items_from_json(settings.data_file)
    return TreeStore(items)


tree_store = get_tree_store()


class ItemIdRequest(BaseModel):
    """Запрос с id элемента."""

    id: Any


@app.post("/api/v1/tree/init", response_model=TreeStoreResponse)
def init_tree(request: TreeStoreRequest) -> TreeStoreResponse:
    """Инициализирует дерево переданным массивом элементов."""
    global tree_store
    tree_store = TreeStore(request.items)
    return TreeStoreResponse(
        result={"status": "initialized", "items_count": len(request.items)}
    )


@app.get("/api/v1/tree/getAll", response_model=TreeStoreResponse)
def get_all() -> TreeStoreResponse:
    """Возвращает все элементы дерева."""
    result = tree_store.get_all()
    return TreeStoreResponse(result=result)


@app.post("/api/v1/tree/getItem", response_model=TreeStoreResponse)
def get_item(request: ItemIdRequest) -> TreeStoreResponse:
    """Возвращает элемент по id. 404, если элемент не найден."""
    try:
        result = tree_store.get_item(request.id)
        return TreeStoreResponse(result=result)
    except ItemNotFoundError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e),
        ) from e


@app.post("/api/v1/tree/getChildren", response_model=TreeStoreResponse)
def get_children(request: ItemIdRequest) -> TreeStoreResponse:
    """Возвращает дочерние элементы для указанного id."""
    result = tree_store.get_children(request.id)
    return TreeStoreResponse(result=result)


@app.post("/api/v1/tree/getAllParents", response_model=TreeStoreResponse)
def get_all_parents(request: ItemIdRequest) -> TreeStoreResponse:
    """Возвращает цепочку родителей от элемента до корня."""
    result = tree_store.get_all_parents(request.id)
    return TreeStoreResponse(result=result)


@app.get("/api/v1/health")
def health() -> dict[str, str]:
    """Проверка работоспособности API."""
    return {"status": "ok"}
