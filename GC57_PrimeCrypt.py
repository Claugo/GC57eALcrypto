"""
***************************************************************************************
GC57_PrimeCrypt
***************************************************************************************
Autore: [Claugo]
Versione: 1.0
Ultima modifica: [Dicembre 2024]

***************************************************************************************
Descrizione:
GC57_PrimeCrypt è un programma avanzato di crittografia che utilizza numeri primi 
di dimensioni molto grandi per garantire la sicurezza dei dati. Combina algoritmi 
crittografici moderni e robusti con un'interfaccia grafica intuitiva per l'invio e 
la ricezione sicura di file e messaggi.

***************************************************************************************
Caratteristiche principali:
1. **Sistema di codifica**:
   - I dati vengono criptati utilizzando AES (Advanced Encryption Standard) in modalità 
     EAX, che garantisce sia la confidenzialità che l'integrità dei dati.
   - La chiave AES è derivata tramite PBKDF2 (Password-Based Key Derivation Function 2) 
     con un valore di sale (salt) casuale e 100.000 iterazioni, garantendo una protezione 
     contro attacchi di forza bruta.

2. **Numeri primi e semiprimo**:
   - Il programma genera un semiprimo (prodotto di due numeri primi) che funge da 
     base per la generazione della chiave crittografica.
   - La sicurezza del sistema si basa sulla difficoltà di fattorizzare il semiprimo.

3. **Hash SHA-3**:
   - Utilizza SHA-3 (Secure Hash Algorithm 3) per generare un'impronta sicura e univoca 
     dei dati crittografici.

4. **Gestione di testo e allegati**:
   - Cripta e decripta messaggi di testo con o senza allegati.
   - Supporta file binari e di grandi dimensioni.

5. **Sicurezza fisica**:
   - L'accesso alla chiave crittografica è vincolato alla presenza di una pendrive USB 
     con un'etichetta specifica.

***************************************************************************************
Requisiti:
- Python 3.10 o superiore
- Librerie richieste:
  - tkinter (per l'interfaccia grafica)
  - Crypto (per la crittografia AES e PBKDF2)
  - hashlib (per SHA-3)
  - os, json, e altre librerie standard

***************************************************************************************
Istruzioni per l'uso:
1. Configurare le cartelle iniziali e il file CFG alla prima esecuzione.
2. Utilizzare le finestre grafiche per inviare o ricevere messaggi.
3. Assicurarsi che la pendrive USB contenente la chiave sia inserita prima di iniziare.

***************************************************************************************
Avvertenze:
- Non condividere la pendrive USB con la chiave crittografica.
- Il programma è progettato per proteggere dati sensibili; tuttavia, la sicurezza 
  dipende anche da una gestione corretta delle chiavi e dei file crittografati.

***************************************************************************************
"""

import tkinter as tk
from tkinter import messagebox, filedialog, simpledialog
import os
from math import gcd
import time
from random import randint, seed
import json
import win32api
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
from Crypto.Random import get_random_bytes
from hashlib import sha3_256
from Crypto.Protocol.KDF import PBKDF2

# *******************************************************
# * controllo file CFG che serve per individuare le cartelle
# * dove prelevare i semiprimi e memorizzare il messaggio
# * e gli allegati. Nel caso non venisse trovato ne crea uno nuovo
# *******************************************************

filecfg = "GC57PCcfg"
if os.path.exists(filecfg):
    pass
else:

    def chiudi_programma():
        risposta = messagebox.askquestion("Attenzione:", "uscire dal programma?")
        if risposta == "yes":
            rootcfg.destroy()
            quit()
        else:
            return

    def salva_esci():
        controllo1 = e2_cfg.get()
        if controllo1 == "":
            messagebox.showerror("Attenzione:", "Tutti i campi devono essere compilati")
            return
        elif os.path.exists(f"{controllo1}"):
            pass
        else:
            messagebox.showerror("Attenzione:", "La cartella INVIO non esiste")
            return

        controllo2 = e3_cfg.get()
        if controllo2 == "":
            messagebox.showerror("Attenzione:", "Tutti i campi devono essere compilati")
            return
        elif os.path.exists(f"{controllo2}"):
            pass
        else:
            messagebox.showerror("Attenzione:", "La cartella RICEVE non esiste")
            return

        controllo3 = e4_cfg.get()
        if controllo3 == "":
            messagebox.showerror("Attenzione:", "Tutti i campi devono essere compilati")
            return
        elif os.path.exists(f"{controllo3}"):
            pass
        else:
            messagebox.showerror("Attenzione:", "La cartella ALLEGATI non esiste")
            return

        controllo4 = e5_cfg.get()
        if controllo4 == "":
            messagebox.showerror("Attenzione:", "Tutti i campi devono essere compilati")
            return
        elif os.path.exists(f"{controllo4}"):
            pass
        else:
            messagebox.showerror("Attenzione:", "La cartella SEMIPRIMI non esiste")
            return

        controllo5 = e6_cfg.get()
        if controllo5 == "":
            messagebox.showerror("Attenzione:", "Manca il nome PenDrive")
            return
        else:
            controllo5 = controllo5.strip().upper()

        scrivi = open("GC57PCcfg", "w")
        scrivi.write(controllo1 + "\n")
        scrivi.write(controllo2 + "\n")
        scrivi.write(controllo3 + "\n")
        scrivi.write(controllo4 + "\n")
        scrivi.write(controllo5 + "\n")
        scrivi.close()
        messagebox.showinfo("Salvataggi CFG:", "Configurazione Salvata")
        rootcfg.destroy()

    rootcfg = tk.Tk()

    # Imposta le dimensioni della finestra
    window_width = 415
    window_height = 460

    # Ottieni le dimensioni dello schermo
    screen_width = rootcfg.winfo_screenwidth()
    screen_height = rootcfg.winfo_screenheight()

    # Calcola la posizione x e y per centrare la finestra
    x = (screen_width - window_width) // 2
    y = (screen_height - window_height) // 2

    # Imposta la posizione e le dimensioni della finestra
    rootcfg.geometry(f"{window_width}x{window_height}+{x}+{y}")
    rootcfg.title("Configurazione Cartelle GC57")
    rootcfg.configure(bg="#458B74")
    colore_testo_entry = "#104E8B"
    testo = (
        "Se appare questa finestra è perchè il programma viene eseguito per la prima volta in questa posizione, \
oppure il file 'GC57PCcfg' è stato cancellato\n\
Copiare e incollare con CTR-V la posizione delle cartelle:",
    )

    l1_cfg = tk.Label(
        rootcfg, text=testo, justify=tk.LEFT, font="arial 12 bold", wraplength=400
    )
    l1_cfg.place(x=10, y=20)

    px = 10
    py = 150
    l2_cfg = tk.Label(
        rootcfg,
        text="Incollare Indirizzo Cartella INVIO",
        bg="#458B74",
        font="arial 12 bold",
    )
    l2_cfg.place(x=px, y=py)
    py = py + 20
    e2_cfg = tk.Entry(rootcfg, width=40, fg=colore_testo_entry, font="arial 12")
    e2_cfg.place(x=px, y=py)

    py = py + 30
    l3_cfg = tk.Label(
        rootcfg,
        text="Incollare Indirizzo Cartella RICEVE",
        bg="#458B74",
        font="arial 12 bold",
    )
    l3_cfg.place(x=px, y=py)
    py = py + 20
    e3_cfg = tk.Entry(rootcfg, width=40, fg=colore_testo_entry, font="arial 12")
    e3_cfg.place(x=px, y=py)

    py = py + 30
    l4_cfg = tk.Label(
        rootcfg,
        text="Incollare Indirizzo Cartella ALLEGATI",
        bg="#458B74",
        font="arial 12 bold",
    )
    l4_cfg.place(x=px, y=py)
    py = py + 20
    e4_cfg = tk.Entry(rootcfg, width=40, fg=colore_testo_entry, font="arial 12")
    e4_cfg.place(x=px, y=py)

    py = py + 30
    l5_cfg = tk.Label(
        rootcfg,
        text="Incollare Indirizzo Cartella SEMIPRIMI",
        bg="#458B74",
        font="arial 12 bold",
    )
    l5_cfg.place(x=px, y=py)
    py = py + 20
    e5_cfg = tk.Entry(rootcfg, width=40, fg=colore_testo_entry, font="arial 12")
    e5_cfg.place(x=px, y=py)

    py = py + 30
    l6_cfg = tk.Label(
        rootcfg,
        text="Inserire il nome della PenDrive (Chiavi)",
        bg="#458B74",
        font="arial 12 bold",
    )
    l6_cfg.place(x=px, y=py)
    py = py + 20
    e6_cfg = tk.Entry(rootcfg, width=40, fg=colore_testo_entry, font="arial 12")
    e6_cfg.place(x=px, y=py)

    px = px + 150
    py = py + 50
    b1 = tk.Button(
        rootcfg,
        text="Salva ed Esci",
        font="arial 12 bold",
        cursor="hand1",
        bg="green",
        command=salva_esci,
    )
    b1.place(x=px, y=py)
    rootcfg.protocol("WM_DELETE_WINDOW", chiudi_programma)

    rootcfg.mainloop()

# *******************************************************
# * Carica CFG
# *******************************************************
filename = ""
apricfg = open("GC57PCcfg", "r")
programma_invia_a = apricfg.readline().strip()
programma_riceve_a = apricfg.readline().strip()
programma_allegati = apricfg.readline().strip()
programma_semiprimi = apricfg.readline().strip()
volume_label = apricfg.readline().strip()
apricfg.close()

# *******************************************************
# * Controlla la porta USB che sia inserita una pendrive
# * con il nome specificato. Questo facilita l'inserimento
# * della pennetta USB su qualsiasi computer
# *******************************************************
messagebox.showinfo("USB", "Inserisci la pen drive CODICE_S")


def get_drive_letter_by_label(label):
    try:
        # Ottenere l'elenco delle unità logiche
        drives = win32api.GetLogicalDriveStrings().split("\x00")[:-1]
        for drive in drives:
            try:
                # Controlla l'etichetta del volume per ogni unità
                volume_label = win32api.GetVolumeInformation(drive)[0]
                if volume_label == label:
                    return drive  # Restituisce la lettera dell'unità
            except Exception:
                # Ignora unità non accessibili
                continue
        return None  # Se non trova l'etichetta
    except Exception as e:
        return f"Error: {e}"


# Test
drive_letter = get_drive_letter_by_label(volume_label)
if drive_letter:
    apri_dati = drive_letter
else:
    messagebox.showerror("Attenzione", "Pennetta non trovata")
    quit()


# *************************************************
# * FINESTRA Principale: In questa finestra vengono proposti due comandi
# * uno per inviare e l'altroper ricevere i messaggi
# * Segue una piccola descrizione della codifica che viene usata per la crittografia
# *************************************************


class Finestra1(tk.Tk):
    def __init__(self):
        super().__init__()

        # ******************************************************
        # dimensione e colori
        # ******************************************************
        colorefw = "#00688B"
        colorei1 = "#FFD700"
        colorei2 = "#CDAD00"
        colorei3 = "#282828"
        coloreft = "#54FF9F"
        colorest = "#1E1E1E"

        dimensionex = 600
        dimensioney = 400
        self.title("Programma di criptazione GC57_PrimeCrypt")
        self.geometry(f"{dimensionex}x{dimensioney}")

        # Crea un canvas per disegnare
        canvas = tk.Canvas(self, width=dimensionex, height=dimensioney, bg=colorefw)
        canvas.pack()
        px = dimensionex // 2
        py = dimensioney - 320
        # Inserisci del testo
        canvas.create_text(
            px, py, text="GC57_PrimeCrypt", font=("Arial 18 bold"), fill=colorei1
        )
        py = dimensioney - 290
        canvas.create_text(
            px, py, text="Numeri Primi al servizio della Crittografia", font=("Arial 18 bold"), fill=colorei2
        )

        # Aggiungi un widget Text per il testo lungo
        text_lungo = tk.Text(self, wrap=tk.WORD, width=60, height=6, bg=colorefw, fg="black", font=("Arial", 12))
        text_lungo.place(x=28, y=dimensioney - 150)
        testo = (
            "Il programma utilizza una combinazione di SHA-3 e PBKDF2 per generare chiavi crittografiche sicure a partire da un semiprimo, "
            "creato moltiplicando due grandi numeri primi. I dati (testo e/o allegati) vengono crittografati con una chiave derivata, e il file risultante, "
            "in formato JSON, include il semiprimo per la decrittazione. La sicurezza è garantita dalla difficoltà di fattorizzare il semiprimo."
        )
        text_lungo.insert(tk.END, testo)
        text_lungo.config(state=tk.DISABLED)  # Rendi il testo non modificabile

        # Disegna una linea
        px = 0
        py = dimensioney - 250
        canvas.create_line(px, py, dimensionex, py, fill="red", width=7)
        py = dimensioney - 170
        canvas.create_line(px, py, dimensionex, py, fill="red", width=7)

        # Crea un pulsante e posizionalo all'interno del trapezio
        px = dimensionex - 430
        py = dimensioney - 210
        button1 = tk.Button(
            self,
            width=5,
            text="Invia",
            fg=colorest,
            bg=coloreft,
            font="arial 16 bold",
            command=self.apri_finestra2,
        )
        canvas.create_window(px, py, window=button1)
        px = dimensionex - 180

        button2 = tk.Button(
            self,
            width=5,
            text="Ricevi",
            fg=colorest,
            bg=coloreft,
            font="arial 16 bold",
            command=self.apri_finestra3,
        )
        canvas.create_window(px, py, window=button2)

    def apri_finestra2(self):
        finestra2 = Finestra2(self)
        finestra2.grab_set()

    def apri_finestra3(self):
        finestra3 = Finestra3(self)
        finestra3.grab_set()


# *************************************************
# * FINESTRA Invia: In questa finestra troviamo un piccolo editor di testo
# * e 3 pulsanti 'Carica allegato, Carica codifica, Invia file'
# * il pulsante Carica allegato permette di caricare un file da inviare assieme al testo
# * questo file può assumere qualsiasi estensione: pdf, txt, jpg, ecc...
# *
# * Il pulsante Carica Codifica permette di selezionare un file con dentro molti semiprimi
# * questi file riportano come grandezza i bit del semiprimo, per esempio S8249b,S10200b,S11622b
# * e dentro questi file verrà caricato un semiprimo a caso da cui verranno estratti i due numeri primi
# * che serviranno a creare una chiave crittografica
# *
# * Il pulsante invia file memorizzerà nella cartella impostata il file criptato
# *************************************************
class Finestra2(tk.Toplevel):
    def __init__(self, master):
        super().__init__(master)

        def codifica():
            if filename == "":
                messagebox.showerror(
                    "Attenzione", "Non è stata selezionata nessuna codifica"
                )
                return
            testo = tw1_invia.get("1.0", tk.END)
            if testo == "" or len(testo) < 12:
                messagebox.showerror("Attenzione", "Messaggio mancante o Troppo corto")
                return

            T = int(time.time())
            seed(T)

            with open(filename, "r") as file:
                righe = file.readlines()
                codice_random = randint(0, len(righe) - 1)  # Genera un indice casuale
                nn = righe[codice_random]
                semiprimo = int(nn.strip())
                a = semiprimo % chiave
                b = semiprimo - a
                for i in range(10):
                    r = gcd(a, b)
                    if r != 1:
                        p = r
                        q = semiprimo // p
                        break
                    a = a + chiave
                    b = b - chiave
                if r == 1:
                    messagebox.showerror("Attenzione", "Codifica non Superata")
                    return
            congiunzione = f"{p}{q}"
            congiunzione=int(congiunzione)
            congiunzione_bytes = congiunzione.to_bytes(
                (congiunzione.bit_length() + 7) // 8, byteorder="big"
            )
            # Genera hash con SHA-3

            sha3_hash = sha3_256(congiunzione_bytes).digest()

            # Deriva la chiave crittografica con PBKDF2
            salt = get_random_bytes(16)  # Genera un sale casuale
            aes_key = PBKDF2(
                sha3_hash, salt, dkLen=32, count=100000
            )  # Chiave AES a 256 bit

            # Cripta il testo con AES
            cipher = AES.new(aes_key, AES.MODE_EAX)
            ciphertext, tag = cipher.encrypt_and_digest(testo.encode("utf-8"))

            allegato_invia = e1_invia.get()

            # Iniziamo con la condizione per verificare se c'è un allegato
            if not allegato_invia or len(allegato_invia) < 6:
                # Nessun allegato, salva solo il testo
                json_data = {
                    "semiprimo": semiprimo,
                    "salt": salt.hex(),
                    "nonce": cipher.nonce.hex(),
                    "ciphertext": ciphertext.hex(),
                    "tag": tag.hex(),
                    "allegato": False
                }

                with open(
                    f"{programma_invia_a}/GC57_PrimeCrypt_mess_{codice_selezionato}.json", "w"
                ) as output_file:
                    json.dump(json_data, output_file)

                messagebox.showinfo(
                    "Successo", "Codifica completata e salvata in dati_criptati.json"
                )
            else:
                # C'è un allegato, leggilo e cripta
                with open(filename_allegato, "rb") as file_allegato:
                    allegato_bytes = file_allegato.read()

                # Cripta l'allegato
                cipher_allegato = AES.new(aes_key, AES.MODE_EAX)
                allegato_ciphertext, allegato_tag = cipher_allegato.encrypt_and_digest(allegato_bytes)

                # Salva testo e allegato
                json_data = {
                    "semiprimo": semiprimo,
                    "salt": salt.hex(),
                    "nonce": cipher.nonce.hex(),
                    "ciphertext": ciphertext.hex(),
                    "tag": tag.hex(),
                    "allegato": True,
                    "allegato_nonce": cipher_allegato.nonce.hex(),
                    "allegato_ciphertext": allegato_ciphertext.hex(),
                    "allegato_tag": allegato_tag.hex(),
                    "allegato_nome":allegato_invia
                }

                with open(
                    f"{programma_invia_a}/GC57_PrimeCrypt_mess_{codice_selezionato}.json",
                    "w",
                ) as output_file:
                    json.dump(json_data, output_file)

                messagebox.showinfo(
                    "Successo", "Codifica completata con allegato salvata in dati_criptati.json"
                )

        def apri_allegato():
            global filename_allegato
            if e2_invia.get() == "":
                messagebox.showerror("Attenzione", "Selezionare prima tipo di codifica")
                return
            filename_allegato = filedialog.askopenfilename(
                title="Apri file",
                # initialdir="C:\\Users/Claugo/OneDrive/Documenti",
                initialdir="f:\\DCP",
                filetypes=(
                    ("Tutti i File", "*.*"),
                    ("File di testo", "*.txt"),
                    ("File PDF", "*.pdf"),
                ),
            )
            if filename_allegato == "":
                return
            else:
                cartella, allegato = os.path.split(filename_allegato)
                e1_invia.delete(0, tk.END)
                e1_invia.insert(0, allegato)

        def apri_codifica():
            global codice_selezionato, chiave, filename
            filename = filedialog.askopenfilename(
                title="Apri file",
                initialdir=f"{programma_semiprimi}",  # Cartella iniziale predefinita
                filetypes=[("File S.*", "s*.*"), ("Tutti i file", "*.*")],
            )

            if filename == "":
                messagebox.showwarning(
                    "Attenzione", "Nessuna codifica selezionata" + apri_dati
                )
                return
            semipsel = filename.split("/")
            codice_selezionato = semipsel[2]
            chiave_usb = apri_dati + "chiave_" + codice_selezionato
            if os.path.exists(chiave_usb):
                with open(chiave_usb, "r") as leggif:
                    chiave = int(leggif.readline())

            else:
                messagebox.showerror("Errore", "Dati su USB non trovati")
                return

            e2_invia.delete(0, tk.END)
            e2_invia.insert(0, codice_selezionato)

        fondo_finestra = "#2F4F4F"
        colore_testo = "#E6E6FA"
        fondo_text = "#00688B"
        self.title("Programma di Criptazione Dati - INVIA")
        self.geometry("700x600")
        self.config(bg=fondo_finestra)
        l1_invia = tk.Label(
            self,
            text="Invia GC57_PrimeCrypto",
            bg=fondo_finestra,
            font="arial 18 bold",
            fg=colore_testo,
        )
        l1_invia.place(x=190, y=20)

        tw1_invia = tk.Text(
            self,
            width=75,
            height=20,
            bg=fondo_text,
            font="helvetica, 12",
            cursor="left_ptr",
            wrap=tk.WORD,
        )
        tw1_invia.place(x=10, y=70)
        b1_invia = tk.Button(
            self,
            text="Invia File",
            fg="#006400",
            width=15,
            font="arial 12 bold",
            cursor="hand2",
            command=codifica,
        )
        b1_invia.place(x=500, y=450)

        b2_invia = tk.Button(
            self,
            text="Carica Allegato",
            fg="#006400",
            width=15,
            font="arial 12 bold",
            cursor="hand2",
            command=apri_allegato,
        )
        b2_invia.place(x=10, y=490)

        b3_invia = tk.Button(
            self,
            text="Seleziona Codifica",
            fg="#006400",
            width=15,
            font="arial 12 bold",
            cursor="hand2",
            command=apri_codifica,
        )
        b3_invia.place(x=10, y=530)

        e1_invia = tk.Entry(
            self,
            width=25,
            font="arial 12 bold",
            bg=fondo_finestra,
            borderwidth=2,
            relief=tk.SUNKEN,
        )
        e1_invia.place(x=180, y=495)

        e2_invia = tk.Entry(
            self,
            width=25,
            font="arial 12 bold",
            bg=fondo_finestra,
            borderwidth=2,
            relief=tk.SUNKEN,
        )
        e2_invia.place(x=180, y=535)


# *************************************************
# * FINESTRA Ricevi: in questa finestra troveremo un editor di testo e un pulsante 'carica file
# * e una casella vuota con scritto 'Allegato'
# *
# * La finestra editor permetterà di vedere in chiaro il messaggio testo ricevuto
# * Nel caso il file contenga un allegato, comparirà il nome con l'estensione dell'allegato
# * e questo verrà salvato nell'apposita cartella Allegati
# *************************************************


class Finestra3(tk.Toplevel):
    def __init__(self, master):
        super().__init__(master)

        def apri_filer():
            global codice_selezionato, chiave, filename
            filename = filedialog.askopenfilename(
                title="Apri file",
                initialdir=f"{programma_riceve_a}",  # Cartella iniziale predefinita
            # filetypes=(("Tutti i File", "*.*"),("File di testo", "*.txt")),
            )

            if filename == "":
                messagebox.showerror("Attenzione", "File non selezionato")
                return

            if "\\" in filename:
                # Se il percorso utilizza '\', usa split('\\')
                semipsel = filename.split("\\")
            else:
                # Altrimenti, usa split('/')
                semipsel = filename.split("/")

            files = semipsel[-1].split("_")
            codice_selezionato = files[3].replace(".json", "")
            chiave_usb = os.path.join(apri_dati, "chiave_" + codice_selezionato)
            if os.path.exists(chiave_usb):
                with open(chiave_usb, "r") as leggif:
                    chiave = int(leggif.readline())
                    # l2.config(text=files[0] + "/" + codice_selezionato)

            else:
                messagebox.showerror("Errore", "Dati su USB non trovati")
                return

            with open(filename, "r") as file:
                dati_criptati = json.load(file)

            # Estrarre i dati principali
            semiprimo = dati_criptati.get("semiprimo")
            salt = bytes.fromhex(dati_criptati.get("salt", ""))
            nonce = bytes.fromhex(dati_criptati.get("nonce", ""))
            ciphertext = bytes.fromhex(dati_criptati.get("ciphertext", ""))
            tag = bytes.fromhex(dati_criptati.get("tag", ""))
            allegato_presente = dati_criptati.get("allegato", False)

            if not all([semiprimo, salt, nonce, ciphertext, tag]):
                messagebox.showerror(
                    "Errore",
                    "Il file non contiene tutti i dati necessari per la decriptazione",
                )
                return
            n = int(semiprimo)
            a = n % chiave
            b = n - a
            for i in range(10):
                r = gcd(a, b)
                if r != 1:
                    p = r
                    q = n // p
                    break
                a = a + chiave
                b = b - chiave
            if r == 1:
                messagebox.showerror("Attenzione", "Codifica non Superata")
                return
            congiunzione = f"{p}{q}"
            congiunzione = int(congiunzione)
            if allegato_presente==False:
                congiunzione_bytes = congiunzione.to_bytes(
                    (congiunzione.bit_length() + 7) // 8, byteorder="big"
                )
                sha3_hash = sha3_256(congiunzione_bytes).digest()
                aes_key = PBKDF2(sha3_hash, salt, dkLen=32, count=100000)
                try:
                    cipher = AES.new(aes_key, AES.MODE_EAX, nonce=nonce)
                    testo_decriptato = cipher.decrypt_and_verify(ciphertext, tag).decode("utf-8")
                    tw1_riceve.delete("1.0",tk.END)
                    tw1_riceve.insert("1.0",testo_decriptato)

                except ValueError as e:
                    messagebox.showerror("Errore", f"Errore durante la decriptazione del testo: {e}")
                    return
            else:
                # Recupera i dati dal file JSON
                congiunzione_bytes = congiunzione.to_bytes(
                    (congiunzione.bit_length() + 7) // 8, byteorder="big"
                )
                sha3_hash = sha3_256(congiunzione_bytes).digest()
                aes_key = PBKDF2(sha3_hash, salt, dkLen=32, count=100000)
                try:
                    cipher = AES.new(aes_key, AES.MODE_EAX, nonce=nonce)
                    testo_decriptato = cipher.decrypt_and_verify(ciphertext, tag).decode("utf-8")
                    tw1_riceve.delete("1.0",tk.END)
                    tw1_riceve.insert("1.0",testo_decriptato)
                except ValueError as e:
                    messagebox.showerror("Errore", f"Errore durante la decriptazione del testo: {e}")
                    return

                allegato = bytes.fromhex(dati_criptati.get("allegato_ciphertext", ""))
                allegato_tag = bytes.fromhex(dati_criptati.get("allegato_tag", ""))
                allegato_nonce = bytes.fromhex(dati_criptati.get("allegato_nonce", ""))
                allegato_nome = dati_criptati.get("allegato_nome", "allegato_sconosciuto")
                e1_riceve.delete(0, tk.END)
                e1_riceve.insert(0, allegato_nome)


                # Genera la chiave AES
                congiunzione_bytes = congiunzione.to_bytes(
                    (congiunzione.bit_length() + 7) // 8, byteorder="big"
                )
                sha3_hash = sha3_256(congiunzione_bytes).digest()
                aes_key = PBKDF2(sha3_hash, salt, dkLen=32, count=100000)

                try:
                    # Decripta l'allegato usando il nonce specifico
                    cipher_allegato = AES.new(aes_key, AES.MODE_EAX, nonce=allegato_nonce)
                    allegato_decriptato = cipher_allegato.decrypt_and_verify(allegato, allegato_tag)

                    # Salva l'allegato su file
                    with open(f"{programma_allegati}/{allegato_nome}", "wb") as decoded_file:
                        decoded_file.write(allegato_decriptato)

                    messagebox.showinfo("Successo", f"Allegato salvato come {allegato_nome}")

                except ValueError as e:
                    messagebox.showerror("Errore", f"Errore durante la decriptazione dell'allegato: {e}")
                    return



        fondo_finestra = "#292421"
        colore_testo = "#E6E6FA"
        fondo_text = "#00688B"

        self.title("Programma di Criptazione Dati - RICEVE")
        self.geometry("700x550")
        self.config(bg=fondo_finestra)
        l1_riceve = tk.Label(
            self,
            text="Ricevi: GC57_PrimeCrypto",
            bg=fondo_finestra,
            font="arial 18 bold",
            fg=colore_testo,
        )
        l1_riceve.place(x=190, y=20)

        tw1_riceve = tk.Text(
            self,
            width=75,
            height=20,
            bg=fondo_text,
            cursor="left_ptr",
            font="helvetica, 12",
            wrap=tk.WORD,
        )
        tw1_riceve.place(x=10, y=70)

        b1_riceve = tk.Button(
            self,
            text="Carica File",
            fg="#228B22",
            width=15,
            font="arial 12 bold",
            cursor="hand2",
            command=apri_filer,
        )
        b1_riceve.place(x=10, y=450)

        px = 450
        py = 475
        l1_riceve = tk.Label(
            self,
            text="Allegato",
            bg=fondo_finestra,
            font="arial 12 bold",
            fg=colore_testo,
        )
        l1_riceve.place(x=px, y=py)
        py = py + 30
        e1_riceve = tk.Entry(
            self,
            width=23,
            font="arial 12 bold",
            fg="#66CD00",
            justify="center",
            bg=fondo_finestra,
            borderwidth=2,
            relief=tk.SUNKEN,
        )
        e1_riceve.place(x=px, y=py)


if __name__ == "__main__":
    finestra_principale = Finestra1()
    finestra_principale.mainloop()
