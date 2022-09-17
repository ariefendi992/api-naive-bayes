# import string

# nama = 'Ari efendi'
# nama_user = nama.translate({ord(c): None for c in string.whitespace})
# # print(nama.translate({ord(c): None for c in string.whitespace}))

# print(nama.replace(" ", "_").lower())

import os 

download_folder = '/app/static'
folder = os.path.join(download_folder, 'saya punya')
print(folder) 