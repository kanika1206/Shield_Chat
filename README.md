\# 🛡️ ShieldChat



\*\*End-to-End Encrypted Socket-Based Messaging Protocol\*\*



ShieldChat is a secure peer-to-peer messaging system implementing a custom Zero-Trust cryptographic protocol from scratch. It eliminates reliance on high-level security abstractions by directly integrating RSA, AES-CTR, and HKDF to establish a fully secure communication channel over raw sockets.



\---



\## 🚀 Features



\- 🔐 \*\*End-to-End Encryption (E2EE)\*\* using AES-128-CTR  

\- 🔑 \*\*Custom RSA-OAEP Key Exchange\*\* for secure session initiation  

\- 🧾 \*\*Mutual Authentication\*\* via custom X.509 PKI  

\- 🛡️ \*\*Replay Attack Protection\*\* using cryptographic nonces  

\- ⚡ \*\*Zero-Trust Architecture\*\* (no reliance on TLS/third-party wrappers)  

\- 🔄 \*\*HKDF-based Key Derivation\*\* for secure session keys  

\- 🧵 \*\*Multi-threaded Architecture\*\* for non-blocking communication  

\- 🎨 \*\*Modern GUI\*\* built using CustomTkinter  



\---



\## 🛠️ Tech Stack



\- \*\*Language\*\*: Python  

\- \*\*UI\*\*: CustomTkinter  

\- \*\*Cryptography\*\*:

&#x20; - RSA (OAEP)

&#x20; - AES-128 (CTR Mode)

&#x20; - HMAC-SHA256

&#x20; - HKDF (SHA-256)

\- \*\*Networking\*\*: TCP Sockets  

\- \*\*Environment\*\*: Virtual Environment (venv)  

\- \*\*Platform Tested\*\*: Linux  



\---



\## 🔐 Protocol Overview



\### Secure Handshake



1\. Client initiates connection  

2\. Server sends X.509 certificate  

3\. Client sends X.509 certificate  

4\. Server sends nonce (Ns)  

5\. Client sends:

&#x20;  - Nc (client nonce)  

&#x20;  - Encrypted Pre-Master Secret (RSA)  

&#x20;  - Digital signature  



✔ Secure channel established



\---



\## 🔑 Key Derivation (HKDF)



\- Input: Pre-Master Secret + (Nc || Ns)  

\- Output:

&#x20; - AES-128 Key (16 bytes)  

&#x20; - HMAC-SHA256 Key (32 bytes)  



\---



\## 📡 Secure Messaging Pipeline



Plaintext → AES-CTR Encryption → Ciphertext → HMAC → Transmission  



\- AES-CTR ensures \*\*low latency \& no padding overhead\*\*  

\- HMAC guarantees \*\*integrity and authenticity\*\*



\---



\## 🧵 Architecture



\### Main Thread

\- Handles GUI (CustomTkinter)  

\- Captures user input  

\- Updates logs in real-time  



\### Background Threads

\- `handshake()` → RSA + key exchange  

\- `recv\_thread()` → receives \& verifies messages  



✔ Fully asynchronous, non-blocking system  



\---



\## 📦 Setup



\### 1. Clone Repository

```bash

git clone https://github.com/kanika1206/Shield\_Chat.git

cd Shield\_Chat

\### 🔹 2. Create Virtual Environment

```bash
python3 -m venv venv


\### 🔹 3. Activate Virtual Environment



&#x20;(Linux/Mac)

```bash
source venv/bin/activate


Windows: 

```bash
venv\\Scripts\\activate


\### 🔹 4. Install Dependencies

```bash
pip install customtkinter



\### 🔹 5. Running the Project

&#x20; ## Start Server

```bash

python3 server\_ui.py



&#x20; ## Start Client

```bash
python3 client\_ui.py


\### 🔒 Security Specifications

* AES-128-CTR 
* RSA
* HMAC-SHA256



\### 🤝 Contributing

Feel free to fork and submit pull requests.





\### 📜 License

MIT License

