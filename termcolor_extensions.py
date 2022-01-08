from typing import Tuple, Optional

import termcolor

INVERSE_COLORS = {value: key for key, value in termcolor.COLORS.items()}


def get_color(text: str) -> Tuple[str, Optional[str]]:
    if not (text.startswith('\033[') and text[4] == 'm' and text.endswith(termcolor.RESET)):
        return text, None
    color_chars = int(text[2:4])
    text = text[5:]
    text = text.rstrip(termcolor.RESET)
    return text, INVERSE_COLORS.get(color_chars, None)
