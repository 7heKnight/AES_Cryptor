import time
import os
print('[*] Checking and updating pip')
os.system('python.exe -m pip install --upgrade pip')
lib = ['PyCryptodome']
for i in lib:
    print(f'\n[*] Installing {i}...')
    os.system(f'pip install {i}')
print('[*] Creating "AES_Cryptor" Folder')
os.system(f'mkdir AES_Cryptor')
print('[*] Downloading "AES_Encrypt.py"...')
os.system('cd AES_Cryptor')
os.system(f'curl https://raw.githubusercontent.com/7heKnight/AES_Cryptor/main/AES_Decrypt.py > AES_Cryptor/AES_Encrypt.py')
print('[*] Downloading "AES_Encrypt.py"...')
os.system(f'curl https://raw.githubusercontent.com/7heKnight/AES_Cryptor/main/AES_Decrypt.py > AES_Cryptor/AES_Decrypt.py')
