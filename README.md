**Under Construction Warning:** This tool is currently under construction, and various bugs are present. The security aspects have not been thoroughly tested and are not proven. It is not recommended for use in security-critical scenarios at this time.

# PCrypt256 - File Encryption Tool
PCrypt256 is a command-line tool for file encryption and decryption using AES-256 in CTR mode. It provides a secure way to protect sensitive information in files. The tool is designed to be simple to use, offering encryption and decryption of individual files or entire directories (including subdirectories).


## Comming Soon
- Strong encryption using AES-256 in GCM mode
- Possibility to sign files
- Upgrade the security architecture 
- Implementing HSM as secret safe

## Features
- Strong encryption using AES-256 in CTR mode
- Command-line interface for easy integration into scripts or manual use
- Encryption of individual files or entire directories (including subdirectories)
- Password-based key generation for secure encryption (SHA256)
- Verification of file integrity after decryption

## Usage

### Encrypting a Single File
```bash
$ python Pcrypt_CLI.py -eF path/to/your/file.txt
```

This command encrypts a single file. Replace `path/to/your/file.txt` with the path to the file you want to encrypt.

### Decrypting a Single File
```bash
$ python Pcrypt_CLI.py -dF path/to/your/encrypted_file.pcrypt
```

This command decrypts a single file. Replace `path/to/your/encrypted_file.pcrypt` with the path to the encrypted file you want to decrypt.

### Encrypting an Entire Directory
```bash
$ python Pcrypt_CLI.py -eD path/to/your/directory
```

This command encrypts all files in a directory and its subdirectories. Replace `path/to/your/directory` with the path to the directory you want to encrypt.

### Decrypting an Entire Directory
```bash
$ python Pcrypt_CLI.py -dD path/to/your/encrypted_directory
```

This command decrypts all files in an encrypted directory and its subdirectories. Replace `path/to/your/encrypted_directory` with the path to the directory containing encrypted files.

## Requirements
- Python 3.x
- [cryptography](https://pypi.org/project/cryptography/) library (`pip install cryptography`)
- [tqdm](https://pypi.org/project/tqdm/) library (`pip install tqdm`)
- [termcolor](https://pypi.org/project/termcolor/) library (`pip install termcolor`)

## Installation
1. Install the required libraries:
   ```bash
   $ pip install -r requirements.txt
   ```

2. Run the tool:
   ```bash
   $ python Pcrypt_CLI.py
   ```

## Contributing
If you'd like to contribute to PCrypt256, please fork the repository and create a pull request. Feel free to open an issue for any bugs or feature requests.

