from pynput.keyboard import Key

# Use the special key constant
key_code = Key.space

# Get the key name
key_name = str(key_code).replace("Key.", "")  # This will give 'space'
print(f"Key Name:"+chr(65))  # Output: "Key Name: space"
