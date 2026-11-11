import re


def _octal(match):
    return f"\\{ord(match.group(0)):03o}"


def c_string(text):
    value = str(text)
    value = value.replace("\\", "\\\\").replace('"', '\\"')
    value = value.replace("\n", "\\n").replace("\r", "\\r").replace("\t", "\\t")
    value = re.sub(r"[\x00-\x08\x0b\x0c\x0e-\x1f\x7f]", _octal, value)
    value = value.replace("??", "?\\?")
    return f'"{value}"'


def python_string(text):
    value = str(text)
    value = value.replace("\\", "\\\\").replace('"', '\\"')
    value = value.replace("\n", "\\n").replace("\r", "\\r").replace("\t", "\\t")
    value = re.sub(r"[\x00-\x08\x0b\x0c\x0e-\x1f\x7f]", lambda m: f"\\x{ord(m.group(0)):02x}", value)
    return f'"{value}"'


def comment_text(text):
    value = "" if text is None else str(text)
    value = re.sub(r"[\r\n]+", " ", value).replace("*/", "* /").replace('"""', '"\u200b""')
    return value.strip()


def c_comment_lines(text, prefix="// "):
    text = "" if text is None else str(text).replace("/*", "/ *")
    lines = []
    for line in str(text).splitlines() or [""]:
        if line.endswith("\\"):
            line += " "
        lines.append(prefix + line)
    return "\n".join(lines)


def indent_text(text, spaces):
    pad = " " * spaces
    value = re.sub(r"\r\n?", "\n", str(text))
    return "\n".join(line.rstrip() if index == 0 or not line.strip() else pad + line for index, line in enumerate(value.split("\n")))
