"""Module to define a DBT manifest file representation."""

from __future__ import annotations

from enum import Enum
from typing import Any

import pydantic
from pydantic import BaseModel, ConfigDict


class _BaseSchema(BaseModel):
    if pydantic.__version__.startswith("1."):

        class Config:
            extra = "allow"
    else:
        model_config = ConfigDict(extra="allow")


class Column(_BaseSchema):
    """Incomplete representation of a column in a manifest."""

    description: str = ""


class ResourceType(str, Enum):
    """Resource type valid options."""

    seed = "seed"
    analysis = "analysis"
    test = "test"
    operation = "operation"
    model = "model"
    sql_operation = "sql_operation"


class Node(_BaseSchema):
    """Incomplete representation of a model in a manifest."""

    name: str
    description: str = ""
    resource_type: ResourceType
    columns: dict[str, Column] = {}


class Argument(_BaseSchema):
    """Incomplete representation of a macro argument in a manifest."""

    name: str
    description: str = ""


class Macro(_BaseSchema):
    """Incomplete representation of a macro in a manifest."""

    description: str = ""
    package_name: str
    arguments: list[Argument] = []


class Manifest(_BaseSchema):
    """Incomplete representation of a DBT manifest file."""

    nodes: dict[str, Node]
    macros: dict[str, Macro]


def parse_manifest(manifest: dict[str, Any]) -> Manifest:
    """Parse a DBT manifest file."""
    if pydantic.__version__.startswith("1."):
        return Manifest.parse_obj(manifest)
    else:
        return Manifest.model_validate(manifest)


__all__ = [
    "parse_manifest",
    "Manifest",
    "Macro",
    "Argument",
    "Node",
    "ResourceType",
    "Column",
]
