import pytest
import main

@pytest.fixture(autouse=True)
def reset_globals():
    """Сбрасываем глобальные переменные для изоляции тестов."""
    main.constants.clear()
    main.value_to_constant.clear()
    main.constant_counter = 0


### Тесты для get_or_create_constant ###
def test_get_or_create_constant_new_value():
    assert main.get_or_create_constant("test_value") == "^CONST_0"
    assert main.constants == {"CONST_0": "test_value"}

def test_get_or_create_constant_existing_value():
    main.get_or_create_constant("duplicate_value")
    assert main.get_or_create_constant("duplicate_value") == "^CONST_0"

def test_get_or_create_constant_multiple_values():
    main.get_or_create_constant("value_1")
    main.get_or_create_constant("value_2")
    assert main.get_or_create_constant("value_3") == "^CONST_2"


### Тесты для resolve_constant_reference ###
def test_resolve_constant_reference_existing():
    main.declare_constant("CONST_1", "resolved_value")
    assert main.resolve_constant_reference("^CONST_1") == "resolved_value"

def test_resolve_constant_reference_nonexistent():
    assert main.resolve_constant_reference("^UNKNOWN_CONST") == "^UNKNOWN_CONST"

def test_resolve_constant_reference_not_a_reference():
    assert main.resolve_constant_reference("plain_value") == "plain_value"


### Тесты для to_custom_lang ###
def test_to_custom_lang_with_dict():
    input_data = {"key": "value"}
    expected_output = '$[\n  KEY : "value",\n]'
    assert main.to_custom_lang(input_data) == expected_output

def test_to_custom_lang_with_constant():
    main.declare_constant("CONST_A", "constant_value")
    assert main.to_custom_lang("^CONST_A") == "\"constant_value\""

def test_to_custom_lang_invalid_type():
    with pytest.raises(ValueError):
        main.to_custom_lang(set([1, 2, 3]))


### Тесты для declare_constant ###
def test_declare_constant():
    main.declare_constant("CONST_X", "value_x")
    assert main.constants["CONST_X"] == "value_x"

def test_declare_constant_overwrite():
    main.declare_constant("CONST_Y", "value_y1")
    main.declare_constant("CONST_Y", "value_y2")
    assert main.constants["CONST_Y"] == "value_y2"

def test_declare_constant_case_insensitive():
    main.declare_constant("const_z", "value_z")
    assert "CONST_Z" in main.constants


### Тесты для parse_constants ###
def test_parse_constants_with_constants():
    data = {"CONSTANTS": {"MY_CONST": "my_value"}, "key": "value"}
    assert main.parse_constants(data) == {"key": "value"}
    assert main.constants == {"MY_CONST": "my_value"}

def test_parse_constants_without_constants():
    data = {"key": "value"}
    assert main.parse_constants(data) == data

def test_parse_constants_duplicate_values():
    data = {"CONSTANTS": {"CONST_A": "val", "CONST_B": "val"}}
    main.parse_constants(data)
    assert main.constants["CONST_A"] == "val"
    assert main.constants["CONST_B"] == "val"
