MDV2_CHARACTERS_TO_ESCAPE = ('_', '*', '[', ']', '(', ')', '~', '`', '>', '#', '+', '-', '=', '|', '{', '}', '.', '!')

MDV2_ESCAPE_SYMBOL = '\\'
MDV2_BOLD_SYMBOL = '*'
_E = MDV2_ESCAPE_SYMBOL
_B = MDV2_BOLD_SYMBOL


def mdv2_escape(text: str) -> str:
    result = text
    for c in MDV2_CHARACTERS_TO_ESCAPE:
        result = result.replace(c, ''.join((MDV2_ESCAPE_SYMBOL, c)))
    return result


def mdv2_bold(text: str) -> str:
    return ''.join((MDV2_BOLD_SYMBOL, text, MDV2_BOLD_SYMBOL))
