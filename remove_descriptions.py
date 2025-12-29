import re

with open('base/management/commands/populate_spells.py', 'r') as f:
    content = f.read()

# Replace all description strings with empty strings
# Match pattern: ' [text with 10+ characters]', followed by comma
content = re.sub(r"' [^']{10,}',", "' ',", content)

with open('base/management/commands/populate_spells.py', 'w') as f:
    f.write(content)

print('Successfully removed all description notes from spells')
