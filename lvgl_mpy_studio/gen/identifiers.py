import keyword
import re
import unicodedata

C_KEYWORDS = set("auto bool break case char const continue default do double else enum extern false float for goto if inline int long register restrict return short signed sizeof static struct switch true typedef union unsigned void volatile while null main _Alignas _Alignof _Atomic _Bool _Complex _Generic _Imaginary _Noreturn _Static_assert _Thread_local".split())
TEMPLATE_NAMES = set("lv lvgl e code obj parent screen screens current_screen objects page_index i display_driver ui app_events time main".split())
PYTHON_BUILTINS = set("abs all any bool bytearray bytes callable chr dict dir divmod enumerate eval exec filter float format getattr globals hasattr hash help hex id input int isinstance iter len list locals map max memoryview min next object oct open ord pow print property range repr reversed round set setattr slice sorted str sum super tuple vars zip const micropython machine time sys gc binascii".split())
RESERVED_NAMES = C_KEYWORDS | set(keyword.kwlist) | PYTHON_BUILTINS | TEMPLATE_NAMES
RESERVED_NAMES.update(name.lower() for name in ("None", "True", "False"))
MAX_IDENTIFIER_LENGTH = 48


def sanitize_identifier(text, fallback="obj"):
    value = "" if text is None else str(text)
    name = unicodedata.normalize("NFKD", value)
    name = "".join(char for char in name if not unicodedata.combining(char)).lower()
    name = re.sub(r"[^a-z0-9_]+", "_", name)
    name = re.sub(r"_+", "_", name).strip("_")[:MAX_IDENTIFIER_LENGTH].rstrip("_")
    if not name:
        name = fallback
    if name[0].isdigit() or re.match(r"^lv(_|$)", name):
        name = f"{fallback}_{name}"
    if name in RESERVED_NAMES:
        name = f"{name}_{fallback}"
    return name


class IdentifierAllocator:
    def __init__(self, reserved=()):
        self.used = RESERVED_NAMES | set(reserved)

    def reserve(self, *names):
        self.used.update(names)

    def allocate(self, text, fallback="obj", also_reserve=None):
        also_reserve = also_reserve or (lambda _name: [])
        base = sanitize_identifier(text, fallback)
        candidate = base
        number = 2
        while candidate in self.used or any(extra in self.used for extra in also_reserve(candidate)):
            candidate = f"{base}_{number}"
            number += 1
        self.reserve(candidate, *also_reserve(candidate))
        return candidate
