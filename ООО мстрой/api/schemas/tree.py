"""Схемы запросов и ответов для эндпоинтов дерева."""

from typing import Any

from pydantic import BaseModel


class Item(BaseModel):
    """Элемент дерева с полями id, parent и опциональным type."""

    id: Any
    parent: Any
    type: Any = None


class ItemIdRequest(BaseModel):
    """Запрос с id элемента."""

    id: Any


class TreeStoreRequest(BaseModel):
    """Запрос с массивом элементов для инициализации дерева."""

    items: list[dict[str, Any]]


class TreeStoreResponse(BaseModel):
    """Ответ API: результат операции (массив, объект или None)."""

    result: list[dict[str, Any]] | dict[str, Any] | None
