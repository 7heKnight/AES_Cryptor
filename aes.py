#!/usr/bin/env python3
"""AES-CBC encryption/decryption tool using only Python standard library."""

import os
import sys
import glob
import platform
from hashlib import md5
from base64 import b64encode, b64decode

try:
    import readline
    _HAS_READLINE = True
except ImportError:
    _HAS_READLINE = False

# ─── AES-128 Constants ───────────────────────────────────────────────────────

BLOCK_SIZE = 16

_SBOX = (
    0x63, 0x7C, 0x77, 0x7B, 0xF2, 0x6B, 0x6F, 0xC5, 0x30, 0x01, 0x67, 0x2B, 0xFE, 0xD7, 0xAB, 0x76,
    0xCA, 0x82, 0xC9, 0x7D, 0xFA, 0x59, 0x47, 0xF0, 0xAD, 0xD4, 0xA2, 0xAF, 0x9C, 0xA4, 0x72, 0xC0,
    0xB7, 0xFD, 0x93, 0x26, 0x36, 0x3F, 0xF7, 0xCC, 0x34, 0xA5, 0xE5, 0xF1, 0x71, 0xD8, 0x31, 0x15,
    0x04, 0xC7, 0x23, 0xC3, 0x18, 0x96, 0x05, 0x9A, 0x07, 0x12, 0x80, 0xE2, 0xEB, 0x27, 0xB2, 0x75,
    0x09, 0x83, 0x2C, 0x1A, 0x1B, 0x6E, 0x5A, 0xA0, 0x52, 0x3B, 0xD6, 0xB3, 0x29, 0xE3, 0x2F, 0x84,
    0x53, 0xD1, 0x00, 0xED, 0x20, 0xFC, 0xB1, 0x5B, 0x6A, 0xCB, 0xBE, 0x39, 0x4A, 0x4C, 0x58, 0xCF,
    0xD0, 0xEF, 0xAA, 0xFB, 0x43, 0x4D, 0x33, 0x85, 0x45, 0xF9, 0x02, 0x7F, 0x50, 0x3C, 0x9F, 0xA8,
    0x51, 0xA3, 0x40, 0x8F, 0x92, 0x9D, 0x38, 0xF5, 0xBC, 0xB6, 0xDA, 0x21, 0x10, 0xFF, 0xF3, 0xD2,
    0xCD, 0x0C, 0x13, 0xEC, 0x5F, 0x97, 0x44, 0x17, 0xC4, 0xA7, 0x7E, 0x3D, 0x64, 0x5D, 0x19, 0x73,
    0x60, 0x81, 0x4F, 0xDC, 0x22, 0x2A, 0x90, 0x88, 0x46, 0xEE, 0xB8, 0x14, 0xDE, 0x5E, 0x0B, 0xDB,
    0xE0, 0x32, 0x3A, 0x0A, 0x49, 0x06, 0x24, 0x5C, 0xC2, 0xD3, 0xAC, 0x62, 0x91, 0x95, 0xE4, 0x79,
    0xE7, 0xC8, 0x37, 0x6D, 0x8D, 0xD5, 0x4E, 0xA9, 0x6C, 0x56, 0xF4, 0xEA, 0x65, 0x7A, 0xAE, 0x08,
    0xBA, 0x78, 0x25, 0x2E, 0x1C, 0xA6, 0xB4, 0xC6, 0xE8, 0xDD, 0x74, 0x1F, 0x4B, 0xBD, 0x8B, 0x8A,
    0x70, 0x3E, 0xB5, 0x66, 0x48, 0x03, 0xF6, 0x0E, 0x61, 0x35, 0x57, 0xB9, 0x86, 0xC1, 0x1D, 0x9E,
    0xE1, 0xF8, 0x98, 0x11, 0x69, 0xD9, 0x8E, 0x94, 0x9B, 0x1E, 0x87, 0xE9, 0xCE, 0x55, 0x28, 0xDF,
    0x8C, 0xA1, 0x89, 0x0D, 0xBF, 0xE6, 0x42, 0x68, 0x41, 0x99, 0x2D, 0x0F, 0xB0, 0x54, 0xBB, 0x16,
)

_inv = [0] * 256
for _i, _v in enumerate(_SBOX):
    _inv[_v] = _i
_INV_SBOX = tuple(_inv)
del _i, _v, _inv

_RCON = (0x01, 0x02, 0x04, 0x08, 0x10, 0x20, 0x40, 0x80, 0x1B, 0x36)

# ─── AES Primitives ──────────────────────────────────────────────────────────


def _xtime(a):
    """Multiply by 2 in GF(2^8)."""
    return ((a << 1) ^ 0x11B) & 0xFF if a & 0x80 else (a << 1) & 0xFF


def _gmul(a, b):
    """Multiply two numbers in GF(2^8)."""
    result = 0
    for _ in range(8):
        if b & 1:
            result ^= a
        a = _xtime(a)
        b >>= 1
    return result


def _sub_bytes(state):
    return [_SBOX[b] for b in state]


def _inv_sub_bytes(state):
    return [_INV_SBOX[b] for b in state]


def _shift_rows(state):
    """Shift rows of the 4x4 state matrix (column-major storage)."""
    s = state[:]
    s[1], s[5], s[9], s[13] = s[5], s[9], s[13], s[1]
    s[2], s[6], s[10], s[14] = s[10], s[14], s[2], s[6]
    s[3], s[7], s[11], s[15] = s[15], s[3], s[7], s[11]
    return s


def _inv_shift_rows(state):
    """Inverse shift rows of the 4x4 state matrix."""
    s = state[:]
    s[1], s[5], s[9], s[13] = s[13], s[1], s[5], s[9]
    s[2], s[6], s[10], s[14] = s[10], s[14], s[2], s[6]
    s[3], s[7], s[11], s[15] = s[7], s[11], s[15], s[3]
    return s


def _mix_columns(state):
    """MixColumns transformation on each column."""
    s = state[:]
    for c in range(4):
        i = c * 4
        a = s[i:i + 4]
        s[i]     = _gmul(a[0], 2) ^ _gmul(a[1], 3) ^ a[2] ^ a[3]
        s[i + 1] = a[0] ^ _gmul(a[1], 2) ^ _gmul(a[2], 3) ^ a[3]
        s[i + 2] = a[0] ^ a[1] ^ _gmul(a[2], 2) ^ _gmul(a[3], 3)
        s[i + 3] = _gmul(a[0], 3) ^ a[1] ^ a[2] ^ _gmul(a[3], 2)
    return s


def _inv_mix_columns(state):
    """Inverse MixColumns transformation."""
    s = state[:]
    for c in range(4):
        i = c * 4
        a = s[i:i + 4]
        s[i]     = _gmul(a[0], 14) ^ _gmul(a[1], 11) ^ _gmul(a[2], 13) ^ _gmul(a[3], 9)
        s[i + 1] = _gmul(a[0], 9)  ^ _gmul(a[1], 14) ^ _gmul(a[2], 11) ^ _gmul(a[3], 13)
        s[i + 2] = _gmul(a[0], 13) ^ _gmul(a[1], 9)  ^ _gmul(a[2], 14) ^ _gmul(a[3], 11)
        s[i + 3] = _gmul(a[0], 11) ^ _gmul(a[1], 13) ^ _gmul(a[2], 9)  ^ _gmul(a[3], 14)
    return s


def _add_round_key(state, round_key):
    return [s ^ k for s, k in zip(state, round_key)]


def _key_expansion(key):
    """Expand a 16-byte AES-128 key into 11 round keys."""
    nk, nr = 4, 10
    w = [list(key[4 * i:4 * i + 4]) for i in range(nk)]

    for i in range(nk, 4 * (nr + 1)):
        temp = w[i - 1][:]
        if i % nk == 0:
            temp = [_SBOX[b] for b in temp[1:] + temp[:1]]
            temp[0] ^= _RCON[i // nk - 1]
        w.append([a ^ b for a, b in zip(w[i - nk], temp)])

    return [sum((w[r * 4 + c] for c in range(4)), []) for r in range(nr + 1)]


def _aes_encrypt_block(block, round_keys):
    """Encrypt a single 16-byte block with AES-128."""
    state = _add_round_key(list(block), round_keys[0])
    for r in range(1, 10):
        state = _sub_bytes(state)
        state = _shift_rows(state)
        state = _mix_columns(state)
        state = _add_round_key(state, round_keys[r])
    state = _sub_bytes(state)
    state = _shift_rows(state)
    state = _add_round_key(state, round_keys[10])
    return bytes(state)


def _aes_decrypt_block(block, round_keys):
    """Decrypt a single 16-byte block with AES-128."""
    state = _add_round_key(list(block), round_keys[10])
    for r in range(9, 0, -1):
        state = _inv_shift_rows(state)
        state = _inv_sub_bytes(state)
        state = _add_round_key(state, round_keys[r])
        state = _inv_mix_columns(state)
    state = _inv_shift_rows(state)
    state = _inv_sub_bytes(state)
    state = _add_round_key(state, round_keys[0])
    return bytes(state)


# ─── Padding ─────────────────────────────────────────────────────────────────


def pkcs7_pad(data, block_size=BLOCK_SIZE):
    """Apply PKCS7 padding to data."""
    pad_len = block_size - (len(data) % block_size)
    return data + bytes([pad_len] * pad_len)


def pkcs7_unpad(data, block_size=BLOCK_SIZE):
    """Remove and validate PKCS7 padding."""
    if not data:
        raise ValueError("Cannot unpad empty data")
    pad_len = data[-1]
    if pad_len < 1 or pad_len > block_size:
        raise ValueError(f"Invalid padding length: {pad_len}")
    if data[-pad_len:] != bytes([pad_len] * pad_len):
        raise ValueError("Invalid PKCS7 padding")
    return data[:-pad_len]


# ─── AESCipher ───────────────────────────────────────────────────────────────


class AESCipher:
    """AES-128-CBC cipher with MD5 key derivation. Format: base64(IV + ciphertext)."""

    def __init__(self, key):
        """Derive AES-128 key from passphrase via MD5."""
        if not key:
            raise ValueError("Key must not be empty")
        if isinstance(key, str):
            key = key.encode('utf-8')
        self.key = md5(key).digest()
        self._round_keys = _key_expansion(self.key)

    def encrypt(self, data):
        """Encrypt data, returning base64-encoded IV + ciphertext."""
        if isinstance(data, str):
            data = data.encode('utf-8')
        if not isinstance(data, (bytes, bytearray)):
            raise TypeError("Data must be str, bytes, or bytearray")

        iv = os.urandom(BLOCK_SIZE)
        padded = pkcs7_pad(data)

        ciphertext = bytearray()
        prev = iv
        for i in range(0, len(padded), BLOCK_SIZE):
            block = padded[i:i + BLOCK_SIZE]
            xored = bytes(a ^ b for a, b in zip(block, prev))
            encrypted = _aes_encrypt_block(xored, self._round_keys)
            ciphertext.extend(encrypted)
            prev = encrypted

        return b64encode(iv + bytes(ciphertext))

    def decrypt(self, data):
        """Decrypt base64-encoded IV + ciphertext, returning plaintext bytes."""
        if isinstance(data, str):
            data = data.encode('utf-8')
        if not isinstance(data, (bytes, bytearray)):
            raise TypeError("Data must be str, bytes, or bytearray")

        raw = b64decode(data)
        if len(raw) < BLOCK_SIZE * 2:
            raise ValueError("Ciphertext too short (must contain IV + at least one block)")
        if len(raw) % BLOCK_SIZE != 0:
            raise ValueError("Ciphertext length is not a multiple of block size")

        iv = raw[:BLOCK_SIZE]
        ciphertext = raw[BLOCK_SIZE:]

        plaintext = bytearray()
        prev = iv
        for i in range(0, len(ciphertext), BLOCK_SIZE):
            block = ciphertext[i:i + BLOCK_SIZE]
            decrypted = _aes_decrypt_block(block, self._round_keys)
            plaintext.extend(bytes(a ^ b for a, b in zip(decrypted, prev)))
            prev = block

        return pkcs7_unpad(bytes(plaintext))


# ─── Tab-Completion ──────────────────────────────────────────────────────────


class _FileCompleter:
    """Tab-completion for file/directory paths using readline."""

    def __init__(self):
        self._matches = []

    def complete(self, text, state):
        if state == 0:
            pattern = os.path.expanduser(text) + '*'
            self._matches = glob.glob(pattern)
            self._matches = [
                m + os.sep if os.path.isdir(m) else m
                for m in self._matches
            ]
        return self._matches[state] if state < len(self._matches) else None


def _input_with_file_completion(prompt_text):
    """Prompt for input with tab-completion for file paths (falls back to plain input on Windows)."""
    if not _HAS_READLINE:
        return input(prompt_text).strip()

    completer = _FileCompleter()
    old_completer = readline.get_completer()
    old_delims = readline.get_completer_delims()
    try:
        readline.set_completer(completer.complete)
        readline.set_completer_delims(' \t\n;')
        # macOS ships libedit instead of GNU readline — different bind syntax
        if getattr(readline, '__doc__', '') and 'libedit' in readline.__doc__:
            readline.parse_and_bind('bind ^I rl_complete')
        else:
            readline.parse_and_bind('tab: complete')
        return input(prompt_text).strip()
    finally:
        readline.set_completer(old_completer)
        readline.set_completer_delims(old_delims)


# ─── CLI ─────────────────────────────────────────────────────────────────────


def _secure_delete(file_path):
    """Overwrite file contents with random data before unlinking to hinder recovery."""
    try:
        length = os.path.getsize(file_path)
        with open(file_path, 'r+b') as f:
            f.write(os.urandom(length))
            f.flush()
            os.fsync(f.fileno())
        os.remove(file_path)
    except OSError:
        # Fallback: plain delete if overwrite fails (e.g., read-only FS)
        os.remove(file_path)


def _get_separator():
    """Return OS-appropriate path separator."""
    return '\\' if platform.system() == 'Windows' else '/'


def _run_encrypt(cipher, data, file_name, type_of_data):
    """Handle encryption output for file or string mode."""
    encrypted = cipher.encrypt(data)
    print('========== RESULT ==========')
    if type_of_data == 'f':
        out_name = file_name + '.aes'
        with open(out_name, 'wb') as f:
            f.write(encrypted)
        _secure_delete(file_name)
        sep = _get_separator()
        print(f'[+] Encrypted data saved to {os.getcwd()}{sep}{out_name}')
        print(f'[+] Original file securely deleted: {file_name}')
    else:
        print(f'[+] Encrypted data: {encrypted.decode("utf-8")}')


def _run_decrypt(cipher, data, file_name, type_of_data):
    """Handle decryption output for file or string mode."""
    plaintext = cipher.decrypt(data)
    print('========== RESULT ==========')
    if type_of_data == 'f':
        out_name = file_name.replace('.aes', '') if file_name.endswith('.aes') else file_name + '.dec'
        with open(out_name, 'wb') as f:
            f.write(plaintext)
        _secure_delete(file_name)
        sep = _get_separator()
        print(f'[+] Decrypted data saved to {os.getcwd()}{sep}{out_name}')
    else:
        print(f'[+] Decrypted data: {plaintext.decode("utf-8")}')


def user_input():
    """Gather operation parameters from the user interactively."""
    mode = input('[*] Choose mode e/d (encrypt/decrypt): ').strip().lower()
    if mode not in ('e', 'd'):
        sys.exit('[-] Invalid mode. Use "e" for encrypt or "d" for decrypt.')

    type_of_data = input('[*] Choose data type f/s (file/string): ').strip().lower()
    file_name = ''

    if type_of_data == 'f':
        file_name = _input_with_file_completion('[*] Input file name: ')
        if not file_name:
            sys.exit('[-] File name cannot be empty.')
        if not os.path.isfile(file_name):
            sys.exit(f'[-] Cannot find file: {file_name}')
        with open(file_name, 'rb') as f:
            data = f.read()
    elif type_of_data == 's':
        data = input('[*] Input the data: ').encode('utf-8')
        if not data:
            sys.exit('[-] Data cannot be empty.')
    else:
        sys.exit('[-] Invalid type. Use "f" for file or "s" for string.')

    aes_key = input('[*] Enter security key: ')
    if not aes_key:
        sys.exit('[-] Security key cannot be empty.')

    return mode, data, aes_key, file_name, type_of_data


if __name__ == '__main__':
    try:
        mode, data, aes_key, file_name, type_of_data = user_input()
        cipher = AESCipher(aes_key)
        if mode == 'e':
            _run_encrypt(cipher, data, file_name, type_of_data)
        else:
            _run_decrypt(cipher, data, file_name, type_of_data)
    except KeyboardInterrupt:
        print('\n[!] Interrupted by user.')
        sys.exit(130)
    except (ValueError, TypeError) as e:
        sys.exit(f'[-] Operation failed: {e}')
    except Exception:
        sys.exit('[-] Wrong key or corrupted data. Operation failed.')