"""Схемы запросов и ответов для эндпоинтов дерева."""

from typing import Any, Dict, List

from pydantic import BaseModel


class Item(BaseModel):
    """Элемент дерева с полями id, parent и опциональным type."""

    id: Any
    parent: Any
    type: Any = None


class TreeStoreRequest(BaseModel):
    """Запрос с массивом элементов для инициализации дерева."""

    items: List[Dict[str, Any]]


class TreeStoreResponse(BaseModel):
    """Ответ API: результат операции (массив, объект или None)."""

    result: List[Dict[str, Any]] | Dict[str, Any] | None
