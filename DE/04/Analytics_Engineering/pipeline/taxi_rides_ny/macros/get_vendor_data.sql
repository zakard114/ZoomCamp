{#
    매크로 이름: get_vendor_names
    설명: vendor_id를 사람이 읽기 쉬운 업체명으로 변환합니다.
    작성 방식: Jinja 딕셔너리를 활용한 동적 CASE 문 생성
#}

{% macro get_vendor_names(vendor_id_column) %}

{%- set vendors = {
    1: 'Creative Mobile Technologies',
    2: 'VeriFone Inc.',
    4: 'Unknown/Other'
} -%}

case {{ vendor_id_column }}
    {% for id, name in vendors.items() -%}
    when {{ id }} then '{{ name }}'
    {% endfor -%}
    else 'Unknown'
end

{% endmacro %}