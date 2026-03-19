import socket
import struct
import os
import threading
import customtkinter as ctk
from datetime import datetime
from cryptography.hazmat.primitives import hashes, hmac, serialization
from cryptography.hazmat.primitives.asymmetric import padding as asym_padding
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives.kdf.hkdf import HKDF
from cryptography import x509

# Configuration - Update to your Server VM IP
SERVER_IP = "10.0.2.10"
PORT = 8080

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

class SecureChatClient(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("ShieldChat v1.0 | E2EE Secure Messaging")
        self.geometry("950x650")
       
        # Grid Layout
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # ---- Sidebar for Security Logs ----
        self.sidebar = ctk.CTkFrame(self, width=250, corner_radius=0)
        self.sidebar.grid(row=0, column=0, sticky="nsew")
       
        self.logo = ctk.CTkLabel(self.sidebar, text="🔐 ShieldChat", font=ctk.CTkFont(size=22, weight="bold"))
        self.logo.pack(padx=20, pady=(30, 10))
       
        self.status_badge = ctk.CTkLabel(self.sidebar, text="STATUS: INITIALIZING", text_color="#FFCC00", font=ctk.CTkFont(weight="bold"))
        self.status_badge.pack(padx=20, pady=5)

        self.protocol_box = ctk.CTkTextbox(self.sidebar, width=220, height=350, font=("Consolas", 11), fg_color="#1a1a1a")
        self.protocol_box.pack(padx=15, pady=20)
        self.protocol_box.insert("0.0", "SYSTEM LOGS\n" + "-"*20 + "\n")
        self.protocol_box.configure(state="disabled")

        # ---- Chat Interface ----
        self.chat_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.chat_frame.grid(row=0, column=1, padx=20, pady=20, sticky="nsew")
        self.chat_frame.grid_rowconfigure(0, weight=1)
        self.chat_frame.grid_columnconfigure(0, weight=1)

        self.display = ctk.CTkTextbox(self.chat_frame, state="disabled", font=("Inter", 14), spacing3=8)
        self.display.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

        self.input_area = ctk.CTkFrame(self.chat_frame, fg_color="transparent")
        self.input_area.grid(row=1, column=0, padx=10, pady=(0, 10), sticky="ew")
       
        self.entry = ctk.CTkEntry(self.input_area, placeholder_text="Type your secure message...", height=45)
        self.entry.pack(side="left", fill="x", expand=True, padx=(0, 10))
        self.entry.bind("<Return>", self.send_action)

        self.send_btn = ctk.CTkButton(self.input_area, text="SEND", width=100, height=45, font=ctk.CTkFont(weight="bold"), command=self.send_action)
        self.send_btn.pack(side="right")

        # Security attributes
        self.sock = None
        self.aes_key = None
        self.hmac_key = None
       
        threading.Thread(target=self.run_handshake, daemon=True).start()

    def log(self, text):
        self.protocol_box.configure(state="normal")
        self.protocol_box.insert("end", f"▶ {text}\n")
        self.protocol_box.configure(state="disabled")
        self.protocol_box.see("end")

    def show_msg(self, user, text):
        self.display.configure(state="normal")
        tag = f"[{datetime.now().strftime('%H:%M')}] {user}: "
        self.display.insert("end", f"{tag}{text}\n")
        self.display.configure(state="disabled")
        self.display.see("end")

    def run_handshake(self):
        try:
            # 1. Load Credentials
            with open("certs/client.key", "rb") as f:
                c_priv = serialization.load_pem_private_key(f.read(), password=None)
            with open("certs/rootCA.crt", "rb") as f:
                root = x509.load_pem_x509_certificate(f.read())
           
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.sock.connect((SERVER_IP, PORT))
            self.log("Socket Connected")

            # 2. RSA Identity Exchange
            raw_len = self.sock.recv(4)
            s_cert_data = self.sock.recv(struct.unpack("I", raw_len)[0])
            s_cert = x509.load_pem_x509_certificate(s_cert_data)
            root.public_key().verify(s_cert.signature, s_cert.tbs_certificate_bytes, asym_padding.PKCS1v15(), s_cert.signature_hash_algorithm)
            self.log("Server Cert Verified")

            with open("certs/client.crt", "rb") as f:
                c_data = f.read()
            self.sock.sendall(struct.pack("I", len(c_data)) + c_data)

            # 3. Nonce & AES-CTR Key Transport
            s_nonce = self.sock.recv(16)
            c_nonce = os.urandom(16)
            self.sock.sendall(c_nonce)
            self.log("Nonces Exchanged")

            pms = os.urandom(32)
            enc_pms = s_cert.public_key().encrypt(pms, asym_padding.OAEP(mgf=asym_padding.MGF1(hashes.SHA256()), algorithm=hashes.SHA256(), label=None))
            sig = c_priv.sign(enc_pms, asym_padding.PKCS1v15(), hashes.SHA256())
            self.sock.sendall(struct.pack("I", len(enc_pms)) + enc_pms + struct.pack("I", len(sig)) + sig)
           
            # 4. HKDF Derivation
            hkdf = HKDF(algorithm=hashes.SHA256(), length=48, salt=c_nonce+s_nonce, info=b'chat keys')
            mat = hkdf.derive(pms)
            self.aes_key, self.hmac_key = mat[:16], mat[16:]
           
            self.status_badge.configure(text="STATUS: SECURE (AES-CTR)", text_color="#00FF7F")
            self.log("Encryption Keys Ready")
            threading.Thread(target=self.recv_thread, daemon=True).start()

        except Exception as e:
            self.status_badge.configure(text="STATUS: FAILED", text_color="red")
            self.log(f"Error: {e}")

    def send_action(self, event=None):
        msg = self.entry.get()
        if msg and self.aes_key:
            nonce = os.urandom(16)
            cipher = Cipher(algorithms.AES(self.aes_key), modes.CTR(nonce))
            encryptor = cipher.encryptor()
            ct = encryptor.update(msg.encode()) + encryptor.finalize()
            h = hmac.HMAC(self.hmac_key, hashes.SHA256())
            h.update(ct)
            mac = h.finalize()
            self.sock.sendall(nonce + struct.pack("I", len(ct)) + ct + mac)
            self.show_msg("You", msg)
            self.entry.delete(0, "end")

    def recv_thread(self):
        while True:
            try:
                nonce = self.sock.recv(16)
                ct_len = struct.unpack("I", self.sock.recv(4))[0]
                ct = self.sock.recv(ct_len)
                mac = self.sock.recv(32)
                h = hmac.HMAC(self.hmac_key, hashes.SHA256())
                h.update(ct)
                h.verify(mac)
                cipher = Cipher(algorithms.AES(self.aes_key), modes.CTR(nonce))
                pt = cipher.decryptor().update(ct) + cipher.decryptor().finalize()
                self.show_msg("Server", pt.decode())
            except: break

if __name__ == "__main__":
    SecureChatClient().mainloop()
