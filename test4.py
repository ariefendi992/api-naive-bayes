import string

nama = 'Ari efendi'
nama_user = nama.translate({ord(c): None for c in string.whitespace})
# print(nama.translate({ord(c): None for c in string.whitespace}))

print(nama.replace(" ", "_").lower())