from typing import TYPE_CHECKING, Dict, Set
import pytest
from zing_product_backend.core.product_containment.parser_core import json_parse

if TYPE_CHECKING:
    from zing_product_backend.core.product_containment.parser_core.containment_structure import *


def test_extract_field_names_set():
    pass


to_test_rule = [
    {"id": "ae857898-ec11-4c03-9e78-2ebb35809505", "rules": [
        {"id": "b0d072a4-b2f3-45a3-b88a-663b1ba282d7", "field": "puller_name", "value": "N01,N02,N03", "operator": "in",
         "valueSource": "value"},
        {"id": "c09b3336-a612-4249-84d6-2b1f421417d5", "not": False, "rules": [], "combinator": "and"}],
     "combinator": "and"}
]


def test_parse_rule():
    pass


def test_zero_division():
    with pytest.raises(ZeroDivisionError):
        1 / 0