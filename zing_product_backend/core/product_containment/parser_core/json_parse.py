from typing import TYPE_CHECKING, Dict, Set
from zing_product_backend.core.product_containment.containment_constants import *
from zing_product_backend.core.product_containment.parser_core.result_structure import *
if TYPE_CHECKING:
    from zing_product_backend.core.product_containment.parser_core.containment_structure import *
    from zing_product_backend.core.product_containment.parser_core.containment_structure import *


def extract_field_names_set(d, key='field', nested_key='rules') -> Set[str]:
    stack = [d]
    field_names = []
    while stack:
        current_item = stack.pop()
        if key in current_item:
            field_names.append(current_item[key])
        if nested_key in current_item:
            stack.extend(current_item[nested_key])

    return set(field_names)


def combine_results(results: List[ContainmentResult], combinator):
    if not results:
        return ContainmentResult(result_status=ContainmentStatus.PASS, dealt_base_rule_data_list=[])

    combined_data_record_list = []
    result_statuses = [r.result_status for r in results]
    error_exists = ContainmentStatus.UNKNOWN in result_statuses

    if error_exists:
        final_status = ContainmentStatus.UNKNOWN
    elif combinator == 'or':
        final_status = ContainmentStatus.CATCH if ContainmentStatus.CATCH in result_statuses else ContainmentStatus.PASS
    elif combinator == 'and':
        final_status = ContainmentStatus.PASS if ContainmentStatus.PASS in result_statuses else ContainmentStatus.CATCH
    else:
        raise ValueError("combinator must be 'or' or 'and'")
    for result in results:
        combined_data_record_list.extend(result.dealt_base_rule_data_list)

    return ContainmentResult(result_status=final_status, dealt_base_rule_data_list=combined_data_record_list)


def parse_rule(rule_dict: dict) -> 'ContainmentRule':
    """
    {
  "id": "f0c1b47d-61ea-4d26-a222-9e927af6712b",
  "combinator": "and",
  "not": false,
  "rules": [
    {
      "id": "004168d2-3984-4e3f-9973-9c1f2db766d5",
      "combinator": "or",
      "rules": [
        {
          "id": "be381380-0912-45d3-90c8-8d7971553f97",
          "field": "isMusician",
          "operator": "=",
          "value": true
        },
        {
          "id": "c2261783-8dde-4fde-845e-287728d558f2",
          "field": "instrument",
          "operator": "=",
          "value": "Guitar"
        }
      ]
    },
    {
      "id": "aa795446-3092-44d1-912b-01234742e900",
      "field": "groupedField1",
      "operator": "=",
      "value": "groupedField4",
      "valueSource": "field"
    },
    {
      "id": "5d5dbeac-21bd-4664-abb5-37d103a11264",
      "field": "birthdate",
      "operator": "between",
      "value": "1954-10-03,1960-06-06"
    }
  ]
}
    """
    if 'combinator' in rule_dict and 'value' in rule_dict:
        raise ValueError("Invalid rule: cannot contain both 'combinator' and 'value' keys.")

    not_flag = rule_dict.get('not', False)
    assert isinstance(not_flag, bool), "'not' flag must be boolean"

    combinator = rule_dict.get('combinator')
    if combinator:
        results = [parse_rule(sub_rule) for sub_rule in rule_dict['rules']]
        combined_result = combine_results(results, combinator)
    else:
        result = True
        combined_result = ContainmentResult(result, {rule_dict['rule_name']: rule_dict})

    return combined_result.invert() if not_flag else combined_result


