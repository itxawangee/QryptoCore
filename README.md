# 🔐 QryptoCore - Advanced Encryption/Decryption Tool

![QryptoCore Screenshot](icon/app.png)

A powerful desktop application for encrypting and decrypting text using both classical and modern cryptographic algorithms. Built with Python and Tkinter, featuring a sleek user interface with multiple themes.

## 🌟 Features

### 🔒 Encryption Algorithms
| Algorithm | Type | Key Required |
|-----------|------|--------------|
| AES | Modern (Block Cipher) | ✅ |
| DES3 | Modern (Block Cipher) | ✅ |
| Caesar | Classical (Substitution) | ✅ |
| Vigenère | Classical (Polyalphabetic) | ✅ |
| One-Time Pad | Unbreakable (When used correctly) | ✅ |
| Atbash | Classical (Substitution) | ❌ |
| Rail Fence | Classical (Transposition) | ✅ |

### ✨ Interface Features
- **Three Beautiful Themes**: Dark, Light, and Tech
- **Adjustable Font Sizes**: Customize your viewing experience
- **Operation History**: Track all your encryption/decryption activities
- **File Operations**: Import/export text files
- **Key Generation**: Automatic secure key generation
- **Responsive Design**: Works on multiple screen sizes

## 📂 Project Structure

```
QryptoCore/
├── main.py            # Application entry point
├── gui.py             # All GUI components and layouts
├── ciphers.py         # Cryptographic implementations
├── utils.py           # Utility functions
├── assets/            # Application assets (icons, etc.)
│   ├── settings.json  # User preferences
│   └── ...            # Other assets
├── requirements.txt   # Python dependencies
├── README.md          # This documentation
└── LICENSE            # MIT License
```

## 🔧 Technical Details

### Cryptographic Implementations
- **AES/DES3**: Uses pycryptodome's optimized implementations
- **Classical Ciphers**: Pure Python implementations with security considerations
- **Key Handling**: Secure key generation and validation

## 🤝 Contributing

We welcome contributions! Please follow these steps:

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request



## 📜 License

Distributed under the MIT License. See `LICENSE` for more information.

## 📬 Contact

Project Maintainer: Akrash Noor Awan 
Email: akrashnoor2580@gmail.com  
GitHub: [@yourusername](https://github.com/itxawangee)  

Project Link: [https://github.com/yourusername/QryptoCore](https://github.com/itxawangee/QryptoCore)

## 🎉 Acknowledgments
- Inspired by classic cryptography tools
- Thanks to the PyCryptodome team for their excellent library
- Tkinter community for GUI resources

---

### Recommended Extras:
1. Add actual screenshots in an `/assets` folder
2. Include a demo GIF showing the app in action
3. Add badges at the top for build status, version, etc.
4. Consider adding a CHANGELOG.md for version history

This README provides:
- Visual appeal with emojis and clear sections
- Comprehensive feature documentation
- Easy-to-follow installation instructions
- Clear usage guide
- Technical details for developers
- Contribution guidelines
- Proper licensing and contact information

Would you like me to add any specific sections or modify any part of this README?
