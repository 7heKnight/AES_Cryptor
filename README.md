# aes.py

A single-file AES-128-CBC encrypt/decrypt tool in pure Python. No pip install, no dependencies, no nonsense — just drop it in and go.

## Why?

I wanted a quick way to encrypt files and strings without pulling in `pycryptodome` or `cryptography` or anything that needs a `pip install`. Sometimes you're on a locked-down machine, sometimes you just don't want the overhead. This does AES-128-CBC from scratch using nothing but the standard library.

Is it as fast as a C-backed library? Nope. Is it handy when you need something that works out of the box on any machine with Python 3? Absolutely.

## What it does

- **Encrypts and decrypts** both files and strings, interactively from the command line
- **Pure Python AES-128** — the actual S-box, ShiftRows, MixColumns, key expansion, all of it
- **CBC mode** with a random IV every time, so encrypting the same thing twice gives different output
- **PKCS7 padding** with proper validation (catches corrupted data on decrypt)
- **Secure file deletion** — overwrites the original with random bytes before removing it, so it's not trivially recoverable
- **Tab-completion** for file paths on macOS and Linux (falls back to normal `input()` on Windows)
- Key derivation is MD5(passphrase) → 16-byte key. Simple, not meant for Fort Knox

## Getting started

```bash
python3 aes.py
```

That's it. Python 3.6+ required, nothing to install.

## Usage

The script walks you through it:

```
[*] Choose mode e/d (encrypt/decrypt): e
[*] Choose data type f/s (file/string): s
[*] Input the data: meet me at the usual place
[*] Enter security key: correcthorsebatterystaple
========== RESULT ==========
[+] Encrypted data: 7J3Fa8x...  (base64)
```

To decrypt, just pick `d` and paste the base64 blob back in with the same key.

**For files**, pick `f` instead of `s` — you can press **Tab** to autocomplete the file path. After encrypting, the original file gets securely wiped and you're left with `yourfile.aes`. Decrypting reverses it.

```
[*] Input file name: doc<TAB>
document.pdf    documents/
[*] Input file name: document.pdf
```

### As a library

You can also import it directly:

```python
from aes import AESCipher

c = AESCipher("my-key")
enc = c.encrypt("secret stuff")
print(c.decrypt(enc))  # b'secret stuff'
```

## How it works, briefly

```
passphrase  →  MD5  →  16-byte AES key
plaintext   →  PKCS7 pad  →  CBC encrypt (random IV)  →  base64(IV + ciphertext)
```

Decryption is the reverse. The IV is prepended to the ciphertext before base64 encoding, so everything you need to decrypt is in one string.

The AES implementation itself follows FIPS 197 — SubBytes, ShiftRows, MixColumns, AddRoundKey, 10 rounds for AES-128. It's been verified against the standard test vectors.

## Known quirks & limitations

- **Speed**: Pure Python is slow compared to OpenSSL-backed libraries. Fine for most files, don't try to encrypt a 2 GB video with it.
- **Key derivation**: MD5 is fast and unsalted — fine for casual use, not suitable if you're worried about serious adversaries. Swap in PBKDF2 if that matters to you.
- **Secure delete on SSDs**: The random overwrite works well on HDDs. SSDs with wear-leveling might keep old data in remapped sectors — that's a hardware limitation, not something any software can fully solve without full-disk encryption.
- **Windows tab-completion**: `readline` isn't available on Windows, so file path auto-complete won't work there. Everything else works fine.
