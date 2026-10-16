import re

with open("build_estudios_adicionales.py", "r", encoding="utf-8") as f:
    code = f.read()

# Check for emojis in current file
emoji_pattern = re.compile(
    '[\U00010000-\U0010ffff]|'
    '[\u2600-\u26FF\u2700-\u27BF\u2B50\u200D\uFE0F]',
    flags=re.UNICODE
)
matches = emoji_pattern.findall(code)
print("Emojis in build_estudios_adicionales.py:", len(matches))
