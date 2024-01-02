from enum import Enum


class InputType(Enum):
    BUTTON = 'button'
    CHECKBOX = 'checkbox'
    COLOR = 'color'
    DATE = 'date'
    DATETIME_LOCAL = 'datetime-local'
    EMAIL = 'email'
    FILE = 'file'
    HIDDEN = 'hidden'
    IMAGE = 'image'
    MONTH = 'month'
    NUMBER = 'number'
    PASSWORD = 'password'
    RADIO = 'radio'
    RANGE = 'range'
    RESET = 'reset'
    SEARCH = 'search'
    SUBMIT = 'submit'
    TEL = 'tel'
    TEXT = 'text'
    TIME = 'time'
    URL = 'url'
    WEEK = 'week'


class ValueEditor(Enum):
    # type ValueEditorType = 'text' | 'select' | 'checkbox' | 'radio' | 'textarea' | 'switch' | 'multiselect' | null;
    TEXT = 'text'
    SELECT = 'select'
    CHECKBOX = 'checkbox'
    RADIO = 'radio'
    TEXTAREA = 'textarea'
    SWITCH = 'switch'
    MULTISELECT = 'multiselect'


