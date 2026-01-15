#!/usr/bin/env python
"""
Simple script to compile .po files to .mo files without requiring gettext tools.
"""
import os
import struct
import array
import re

def generate_mo(po_file, mo_file):
    """
    Compile a .po file to .mo file format.
    This is a simplified implementation that handles basic po files.
    """
    messages = {}
    current_msgid = []
    current_msgstr = []
    in_msgid = False
    in_msgstr = False

    with open(po_file, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.rstrip('\n')

            # Skip comments and blank lines
            if line.startswith('#') or not line.strip():
                continue

            if line.startswith('msgid '):
                # Save previous message
                if in_msgstr:
                    msgid_text = ''.join(current_msgid)
                    msgstr_text = ''.join(current_msgstr)
                    messages[msgid_text] = msgstr_text

                # Start new msgid
                current_msgid = [line[7:-1]]  # Remove 'msgid "' and '"'
                current_msgstr = []
                in_msgid = True
                in_msgstr = False

            elif line.startswith('msgstr '):
                current_msgstr = [line[8:-1]]  # Remove 'msgstr "' and '"'
                in_msgid = False
                in_msgstr = True

            elif line.startswith('"') and (in_msgid or in_msgstr):
                # Continuation line
                text = line[1:-1]  # Remove quotes
                if in_msgid:
                    current_msgid.append(text)
                elif in_msgstr:
                    current_msgstr.append(text)

    # Don't forget the last message
    if in_msgstr:
        msgid_text = ''.join(current_msgid)
        msgstr_text = ''.join(current_msgstr)
        messages[msgid_text] = msgstr_text

    # Convert \\n to actual newlines in the header
    if '' in messages:
        messages[''] = messages[''].replace('\\n', '\n')

    # Generate .mo file
    keys = sorted(messages.keys())
    offsets = []
    ids = b''
    strs = b''

    for key in keys:
        msg = messages[key]
        key_bytes = key.encode('utf-8')
        msg_bytes = msg.encode('utf-8')
        offsets.append((len(ids), len(key_bytes), len(strs), len(msg_bytes)))
        ids += key_bytes + b'\x00'
        strs += msg_bytes + b'\x00'

    # The header is 7 32-bit unsigned integers
    keystart = 7 * 4 + 16 * len(keys)
    valuestart = keystart + len(ids)
    koffsets = []
    voffsets = []

    for o1, l1, o2, l2 in offsets:
        koffsets += [l1, o1 + keystart]
        voffsets += [l2, o2 + valuestart]

    offsets = koffsets + voffsets

    output = struct.pack(
        'Iiiiiii',
        0x950412de,        # Magic number
        0,                 # Version
        len(keys),         # Number of entries
        7 * 4,             # Start of key index
        7 * 4 + len(keys) * 8,  # Start of value index
        0, 0               # Size and offset of hash table
    )

    output += array.array('i', offsets).tobytes()
    output += ids
    output += strs

    with open(mo_file, 'wb') as f:
        f.write(output)

    print(f"Compiled {po_file} -> {mo_file} ({len(messages)-1} messages + header)")

if __name__ == '__main__':
    # Compile Vietnamese translation
    po_file = 'locale/vi/LC_MESSAGES/django.po'
    mo_file = 'locale/vi/LC_MESSAGES/django.mo'

    if os.path.exists(po_file):
        generate_mo(po_file, mo_file)
        print("Vietnamese translation compiled successfully!")
    else:
        print(f"Error: {po_file} not found")
