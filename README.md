<div align="center">

# 🛡️ ShieldChat

### *End-to-End Encrypted · Zero-Trust · Socket-Based Messaging*

<br/>

[![Python](https://img.shields.io/badge/Python-3.10+-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://python.org)
[![License: MIT](https://img.shields.io/badge/License-MIT-22c55e?style=for-the-badge)](LICENSE)
[![Platform](https://img.shields.io/badge/Platform-Linux-FCC624?style=for-the-badge&logo=linux&logoColor=black)](https://linux.org)
[![Cryptography](https://img.shields.io/badge/Crypto-RSA%20%7C%20AES%20%7C%20HKDF-ef4444?style=for-the-badge&logo=gnuprivacyguard&logoColor=white)]()

<br/>

> **ShieldChat** is a secure peer-to-peer messaging system that implements a custom  
> **Zero-Trust cryptographic protocol from scratch** — no TLS, no high-level wrappers.  
> Just raw sockets, real cryptography, and a paranoid amount of care.

</div>

---

<br/>

## ✦ What Makes ShieldChat Different

Most "secure" chat apps offload trust to TLS and third-party libraries. ShieldChat doesn't.  
Every byte is accounted for. Every key is derived intentionally. Every message is authenticated.
```
Client ──── RSA-OAEP ──── Pre-Master Secret ──── HKDF ──── AES-128-CTR + HMAC ──── Server
              ↑                                                       ↑
         X.509 PKI                                           Replay Protection
      Mutual Auth                                             via Nonces
```

<br/>

## ⚡ Features

| Feature | Description |
|---|---|
| 🔐 **End-to-End Encryption** | AES-128-CTR ensures low-latency, no-padding-overhead message encryption |
| 🔑 **RSA-OAEP Key Exchange** | Asymmetric encryption for secure session bootstrapping |
| 🧾 **Mutual Authentication** | Custom X.509 PKI — both parties prove who they are |
| 🛡️ **Replay Attack Protection** | Cryptographic nonces (`Nc`, `Ns`) eliminate replay vectors |
| 🔄 **HKDF Key Derivation** | Session keys derived fresh from pre-master secret + nonces |
| ⚡ **Zero-Trust Architecture** | No reliance on TLS or any third-party security wrappers |
| 🧵 **Multi-threaded Design** | Non-blocking async architecture for smooth real-time chat |
| 🎨 **Modern GUI** | Clean, intuitive interface built with CustomTkinter |

<br/>

## 🔐 Cryptographic Protocol

### Handshake Flow
```
┌──────────────────────────────────────────────────────────────────┐
│                    SHIELDCHAT SECURE HANDSHAKE                   │
├──────────────────────────────────────────────────────────────────┤
│                                                                  │
│   CLIENT                                          SERVER         │
│     │                                               │            │
│     │ ──── TCP Connect ────────────────────────────▶│            │
│     │                                               │            │
│     │ ◀─── X.509 Certificate (Server) ─────────────│            │
│     │                                               │            │
│     │ ──── X.509 Certificate (Client) ─────────────▶│            │
│     │                                               │            │
│     │ ◀─── Nonce Ns ────────────────────────────────│            │
│     │                                               │            │
│     │ ──── Nc + Encrypted PMS (RSA) + Signature ───▶│            │
│     │                                               │            │
│     │        ✔ Secure Channel Established           │            │
│                                                                  │
└──────────────────────────────────────────────────────────────────┘
```

### Key Derivation (HKDF-SHA256)
```
Pre-Master Secret  ──┐
                     ├──▶  HKDF(SHA-256)  ──▶  AES-128 Key   (16 bytes)
Nonce: Nc ║ Ns    ──┘                     └──▶  HMAC Key      (32 bytes)
```

### Messaging Pipeline
```
  Plaintext
     │
     ▼
 AES-128-CTR  ──▶  Ciphertext
                       │
                       ▼
                   HMAC-SHA256  ──▶  Authenticated Ciphertext  ──▶  Transmitted
```

> **AES-CTR** = no padding overhead, stream-cipher speed  
> **HMAC** = integrity + authenticity on every message

<br/>

## 🛠️ Tech Stack
```yaml
Language:     Python 3.10+
UI:           CustomTkinter
Networking:   Raw TCP Sockets
Cryptography:
  - RSA-OAEP         # Asymmetric key exchange
  - AES-128-CTR      # Symmetric message encryption
  - HMAC-SHA256      # Message integrity & authenticity
  - HKDF-SHA256      # Session key derivation
  - X.509 PKI        # Mutual certificate-based authentication
Platform:     Linux (tested)
Environment:  Python venv
```

<br/>

## 🧵 Architecture
```
┌─────────────────────────────────────────┐
│              MAIN THREAD                │
│  • Runs CustomTkinter GUI               │
│  • Captures user input                  │
│  • Updates message log in real-time     │
└──────────────────┬──────────────────────┘
                   │ spawns
       ┌───────────┴───────────┐
       ▼                       ▼
┌─────────────┐       ┌─────────────────┐
│ handshake() │       │  recv_thread()  │
│             │       │                 │
│ RSA key ex. │       │ Receive msgs    │
│ HKDF derive │       │ Verify HMAC     │
│ Auth certs  │       │ Decrypt AES-CTR │
└─────────────┘       └─────────────────┘
```

<br/>

## 📦 Installation & Setup

### 1. Clone the Repository
```bash
git clone https://github.com/kanika1206/Shield_Chat.git
cd Shield_Chat
```

### 2. Create a Virtual Environment
```bash
python3 -m venv venv
```

### 3. Activate the Environment
```bash
# Linux / macOS
source venv/bin/activate

# Windows
venv\Scripts\activate
```

### 4. Install Dependencies
```bash
pip install customtkinter
```

<br/>

## 🚀 Running ShieldChat

Open **two terminals** in the project directory with venv active in both.

**Terminal 1 — Start the Server:**
```bash
python3 server_ui.py
```

**Terminal 2 — Start the Client:**
```bash
python3 client_ui.py
```

> The handshake happens automatically. Once the secure channel is established, you can start chatting.

<br/>

## 🔒 Security Specifications

| Primitive | Specification |
|---|---|
| Symmetric Encryption | AES-128-CTR |
| Asymmetric Encryption | RSA-OAEP |
| Message Authentication | HMAC-SHA256 |
| Key Derivation | HKDF-SHA256 |
| Certificate Format | X.509 |
| Replay Protection | Dual nonce scheme (Nc, Ns) |

<br/>

## 🤝 Contributing

Contributions are welcome. Fork the repo, make your changes, and open a pull request.  
Please ensure any cryptographic changes are well-documented and justified.

<br/>

## 📜 License

This project is licensed under the **MIT License** — see the [LICENSE](LICENSE) file for details.

---

<div align="center">

*Built from scratch. No shortcuts. No trust.*

**ShieldChat** — *because security shouldn't be a black box.*

</div>
