from typing import Any, List, Optional
from pydantic import BaseModel


class SpcOOSBaseRule(BaseModel):
    field: Optional[str]
    value: Any
    operator: Optional[str]
    combinator: Optional[str]
    rules: Optional[List['SpcOOSBaseRule']]


class ContainmentRule(BaseModel):
    field: Optional[str]
    value: Any
    operator: Optional[str]
    combinator: Optional[str]
    rules: Optional[List['ContainmentRule']]


