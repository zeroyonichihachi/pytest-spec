# -*- coding: utf-8 -*-
import string


_formatter = string.Formatter()


class FormatPlaceholder:
    def __init__(self, key):
        self.key = key

    def __format__(self, spec):
        result = self.key
        if spec:
            result += ":" + spec
        return "{" + result + "}"


class FormatDict(dict):
    def __missing__(self, key):
        return FormatPlaceholder(key)


def format_in_safe(format_string, **kwargs):
    """
    Format given string with remining arguments.

    Unlike the default 'format' function, this arises no exceptions even if a string
    to format includes a placeholder whose name is not specified in arguments.

    i.e.)
        '{arg}'.format(val=10)          #=> 'KeyError' arises
        format_in_safe('{arg}', val=10) #=> '{arg}' is returned without any exceptions
    """
    return _formatter.vformat(format_string, [], FormatDict(**kwargs))


__all__ = [format_in_safe]

