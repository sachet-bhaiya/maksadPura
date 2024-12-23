import unicodedata

# ASCII code for '\x10'
char = chr(16)  # Equivalent to '\x10'
name = unicodedata.name(char, f"Non-printable ASCII {ord(char)}")
print(name)  # Output: 'DEVICE CONTROL TWO'
