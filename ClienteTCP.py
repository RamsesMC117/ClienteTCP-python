import socket
import threading
import tkinter as tk
from tkinter import scrolledtext

class ClienteTCP:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Cliente TCP")
        
        # Configuración de la interfaz
        self.text_area = scrolledtext.ScrolledText(self.root, wrap=tk.WORD, state='disabled')
        self.text_area.pack(pady=10, padx=10)

        self.message_entry = tk.Entry(self.root, width=50)
        self.message_entry.pack(pady=10, padx=10)

        self.send_button = tk.Button(self.root, text="Enviar", command=self.send_message)
        self.send_button.pack(pady=10)

        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_address = ('localhost', 8080)  # Cambia la dirección IP y el puerto si es necesario

        # Intentar conectar al servidor
        try:
            self.client_socket.connect(self.server_address)
            self.text_area.config(state='normal')
            self.text_area.insert(tk.END, "Conectado al servidor en: {}\n".format(self.server_address))
            self.text_area.config(state='disabled')

            # Iniciar un hilo para recibir mensajes del servidor
            threading.Thread(target=self.receive_messages, daemon=True).start()
        except Exception as e:
            self.text_area.config(state='normal')
            self.text_area.insert(tk.END, "Error al conectar: {}\n".format(e))
            self.text_area.config(state='disabled')

        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.root.mainloop()

    def send_message(self):
        message = self.message_entry.get()
        if message:
            self.client_socket.sendall(message.encode('utf-8'))
            self.message_entry.delete(0, tk.END)  # Limpiar el campo de entrada

    def receive_messages(self):
        while True:
            try:
                response = self.client_socket.recv(1024).decode('utf-8')
                self.text_area.config(state='normal')
                self.text_area.insert(tk.END, "{}\n".format(response))
                self.text_area.config(state='disabled')
            except Exception as e:
                self.text_area.config(state='normal')
                self.text_area.insert(tk.END, "Error al recibir mensaje: {}\n".format(e))
                self.text_area.config(state='disabled')
                break

    def on_closing(self):
        self.client_socket.close()
        self.root.destroy()

if __name__ == "__main__":
    ClienteTCP()
