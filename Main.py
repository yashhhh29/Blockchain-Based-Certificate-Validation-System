from tkinter import messagebox, Tk, Label, Button, Entry, Text as TkText, Scrollbar, END
from tkinter.filedialog import askopenfilename
from Block import *
from Blockchain import *
from hashlib import sha256
import os
import pickle
import shutil

# Initialize the Tkinter window
main = Tk()
main.title("Blockchain Based Certificate Validation")
main.geometry("1300x1200")

# Initialize blockchain
blockchain = Blockchain()

# Load the blockchain if it exists
if os.path.exists('blockchain_contract.txt'):
    with open('blockchain_contract.txt', 'rb') as fileinput:
        blockchain = pickle.load(fileinput)
else:
    blockchain = Blockchain()  # Create a new blockchain if none exists

# Create text widget to display messages
Text = TkText(main, height=15, width=120)
scroll = Scrollbar(Text)
Text.configure(yscrollcommand=scroll.set)
Text.place(x=10, y=350)
Text.config(font=('times', 13, 'bold'))

# Define global filename variable
filename = ""
selected_file_label = Label(main, text="No file selected", font=('times', 12, 'italic'))
selected_file_label.place(x=50, y=300)


def uploadCertificate():
    global filename
    filename = askopenfilename(initialdir="certificate_templates")
    if filename:
        selected_file_label.config(text=f"Selected: {os.path.basename(filename)}")
    else:
        selected_file_label.config(text="No file selected")


def saveCertificate():
    global filename
    Text.delete('1.0', END)

    if not filename:
        Text.insert(END, "Please upload a certificate file first!\n")
        return

    save_directory = "saved_certificates"
    if not os.path.exists(save_directory):
        os.makedirs(save_directory)

    file_name = os.path.basename(filename)
    saved_file_path = os.path.join(save_directory, file_name)
    shutil.copy(filename, saved_file_path)

    with open(filename, "rb") as f:
        file_bytes = f.read()

    roll_no = tf1.get()
    name = tf2.get()
    contact = tf3.get()
    issuer = tf4.get()

    if len(roll_no) > 0 and len(name) > 0 and len(contact) > 0 and len(issuer) > 0:
        digital_signature = sha256(file_bytes).hexdigest()

        transaction_data = {
            'roll_no': roll_no,
            'name': name,
            'contact': contact,
            'issuer': issuer,
            'digital_signature': digital_signature,
            'file_path': saved_file_path
        }

        blockchain.add_new_transaction(transaction_data)
        block_index = blockchain.mine()
        block = blockchain.chain[-1]

        Text.insert(END, f"Blockchain Previous Hash: {block.previous_hash}\n")
        Text.insert(END, f"Block No: {block.index}\n")
        Text.insert(END, f"Current Hash: {block.hash}\n")
        Text.insert(END, f"Certificate Digital Signature: {digital_signature}\n")
        Text.insert(END, f"Certificate saved at: {saved_file_path}\n\n")

        blockchain.save_object(blockchain, 'blockchain_contract.txt')
    else:
        Text.insert(END, "Please enter all required fields: Roll No, Name, Contact, and Issuer\n")


def verifyCertificate():
    Text.delete('1.0', END)
    filename = askopenfilename(initialdir="certificate_templates")

    if not filename:
        Text.insert(END, "No certificate selected for verification.\n")
        return

    with open(filename, "rb") as f:
        file_bytes = f.read()

    digital_signature = sha256(file_bytes).hexdigest()
    found = False

    for block in blockchain.chain:
        for transaction in block.transactions:
            if isinstance(transaction, dict) and transaction.get("digital_signature") == digital_signature:
                Text.insert(END, "\u2705 Certificate Validation Successful\n")
                Text.insert(END, f"\u2192 Roll No: {transaction.get('roll_no')}\n")
                Text.insert(END, f"\u2192 Student Name: {transaction.get('name')}\n")
                Text.insert(END, f"\u2192 Contact No: {transaction.get('contact')}\n")
                Text.insert(END, f"\u2192 Issuer: {transaction.get('issuer')}\n")
                Text.insert(END, f"\u2192 Certificate Hash: {transaction.get('digital_signature')}\n")
                found = True
                break
        if found:
            break

    if not found:
        Text.insert(END, "\u274C Verification failed or certificate has been tampered.\n")


# Create UI elements
font1 = ('times', 13, 'bold')
font = ('times', 15, 'bold')

title = Label(main, text='Blockchain Based Certificate Validation')
title.config(bg='bisque', fg='purple1', font=font, height=3, width=120)
title.place(x=0, y=5)

l1 = Label(main, text='Roll No :', font=font1)
l1.place(x=50, y=100)
tf1 = Entry(main, width=20, font=font1)
tf1.place(x=180, y=100)

l2 = Label(main, text='Student Name :', font=font1)
l2.place(x=50, y=150)
tf2 = Entry(main, width=20, font=font1)
tf2.place(x=180, y=150)

l3 = Label(main, text='Contact No :', font=font1)
l3.place(x=50, y=200)
tf3 = Entry(main, width=20, font=font1)
tf3.place(x=180, y=200)

l4 = Label(main, text='Issuer :', font=font1)
l4.place(x=450, y=100)
tf4 = Entry(main, width=20, font=font1)
tf4.place(x=580, y=100)

uploadButton = Button(main, text="Upload Certificate", command=uploadCertificate, font=font1)
uploadButton.place(x=50, y=250)

saveButton = Button(main, text="Save Certificate with Digital Signature", command=saveCertificate, font=font1)
saveButton.place(x=220, y=250)

verifyButton = Button(main, text="Verify Certificate", command=verifyCertificate, font=font1)
verifyButton.place(x=420, y=250)

main.config(bg='cornflower blue')
main.mainloop()