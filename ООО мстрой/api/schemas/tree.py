from typing import Any, Dict, List
from pydantic import BaseModel


class Item(BaseModel):
    id: Any
    parent: Any
    type: Any = None


class TreeStoreRequest(BaseModel):
    items: List[Dict[str, Any]]


class TreeStoreResponse(BaseModel):
    result: List[Dict[str, Any]] | Dict[str, Any] | None
