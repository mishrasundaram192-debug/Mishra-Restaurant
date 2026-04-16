import customtkinter as ctk
from tkinter import messagebox
from datetime import datetime
import random
from reportlab.pdfgen import canvas
import os
import sys

# -------- UI THEME --------
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

# -------- MENU --------
menu = {
    "Fast Food": {
        "Pizza": 120,
        "Burger": 80,
        "Pasta": 100,
        "Samosa": 20
    },
    "Main Course": {
        "Roti": 10,
        "Butter Roti": 15,
        "Half Dal": 25,
        "Full Dal": 60,
        "Paneer Curry": 150
    },
    "Drinks": {
        "Tea": 10,
        "Coffee": 20,
        "Cold Coffee": 50,
        "Soda": 20,
        "Juice": 60
    }
}

order = []
order_no = random.randint(1000, 9999)

# -------- FUNCTIONS --------
def add_item(item, price):
    qty = qty_entry.get()
    if not qty:
        messagebox.showerror("Error", "Enter quantity!")
        return
    
    qty = int(qty)
    total_price = qty * price
    order.append((item, qty, total_price))
    
    bill_box.insert("end", f"{item} x {qty} = Rs {total_price}\n")
    qty_entry.delete(0, "end")


def generate_bill():
    if not order:
        return
    
    customer_name = customer_entry.get().strip()
    if not customer_name:
        customer_name = "Guest"
    
    subtotal = sum(i[2] for i in order)
    gst = subtotal * 0.05
    discount = subtotal * 0.10
    total = subtotal + gst - discount
    
    bill_box.insert("end", "\n------------------\n")
    bill_box.insert("end", f"Customer: {customer_name}\n")
    bill_box.insert("end", f"Subtotal: Rs {subtotal}\n")
    bill_box.insert("end", f"GST (5%): Rs {gst:.2f}\n")
    bill_box.insert("end", f"Discount (10%): -Rs {discount:.2f}\n")
    bill_box.insert("end", f"Total: Rs {total:.2f}\n")


def clear_order():
    order.clear()
    bill_box.delete("1.0", "end")
    qty_entry.delete(0, "end")
    customer_entry.delete(0, "end")


def export_pdf():
    if not order:
        return
    
    customer_name = customer_entry.get().strip()
    if not customer_name:
        customer_name = "Guest"
    
    file = f"Bill_{order_no}.pdf"
    c = canvas.Canvas(file)
    
    y = 800
    c.drawString(200, y, "MISHRA RESTAURANT")
    y -= 20
    
    c.drawString(50, y, f"Order No: {order_no}")
    y -= 20
    
    c.drawString(50, y, f"Customer: {customer_name}")
    y -= 20
    
    c.drawString(50, y, datetime.now().strftime("%d-%m-%Y %H:%M"))
    y -= 30
    
    subtotal = 0
    
    for item, qty, price in order:
        c.drawString(50, y, f"{item} x {qty} = Rs {price}")
        subtotal += price
        y -= 20
    
    gst = subtotal * 0.05
    discount = subtotal * 0.10
    total = subtotal + gst - discount
    
    y -= 10
    c.drawString(50, y, f"Subtotal: Rs {subtotal}")
    y -= 20
    c.drawString(50, y, f"GST (5%): Rs {gst:.2f}")
    y -= 20
    c.drawString(50, y, f"Discount (10%): -Rs {discount:.2f}")
    y -= 20
    c.drawString(50, y, f"Total: Rs {total:.2f}")
    
    c.save()
    messagebox.showinfo("Saved", f"{file} saved!")

    # AUTO OPEN PDF
    try:
        if sys.platform == "win32":
            os.startfile(file)
        elif sys.platform == "darwin":
            os.system(f"open {file}")
        else:
            os.system(f"xdg-open {file}")
    except:
        pass


# -------- UI --------
app = ctk.CTk()
app.geometry("900x600")
app.title("Mishra Restaurant - Billing System")

# DARK BLUE BACKGROUND
app.configure(fg_color="#000000")

# LEFT PANEL
left_frame = ctk.CTkFrame(app)
left_frame.pack(side="left", fill="both", expand=True, padx=10, pady=10)

# RIGHT PANEL
right_frame = ctk.CTkFrame(app, width=300)
right_frame.pack(side="right", fill="y", padx=10, pady=10)

# HEADER
title = ctk.CTkLabel(left_frame, text=" _🍽_Mishra_Restaurant_", font=("Arial", 20, "bold"))
title.pack(pady=10)

info = ctk.CTkLabel(left_frame, text=f"Order #{order_no} | {datetime.now().strftime('%d-%m-%Y %H:%M')}")
info.pack()

# CUSTOMER NAME
customer_entry = ctk.CTkEntry(left_frame, placeholder_text="Enter Customer Name")
customer_entry.pack(pady=10)

# QUANTITY
qty_entry = ctk.CTkEntry(left_frame, placeholder_text="Enter Quantity")
qty_entry.pack(pady=10)

# MENU
for category, items in menu.items():
    ctk.CTkLabel(left_frame, text=category, font=("Arial", 16, "bold")).pack(pady=5)
    
    frame = ctk.CTkFrame(left_frame)
    frame.pack(pady=5)
    
    for item, price in items.items():
        btn = ctk.CTkButton(
            frame,
            text=f"{item}\nRs {price}",
            width=120,
            fg_color="#9706BB",
            hover_color="#e07b00",
            command=lambda i=item, p=price: add_item(i, p)
        )
        btn.pack(side="left", padx=5, pady=5)

# BILL AREA
ctk.CTkLabel(right_frame, text="🧾 Bill", font=("Arial", 16, "bold")).pack(pady=10)

bill_box = ctk.CTkTextbox(right_frame, width=280, height=350)
bill_box.pack(padx=10)

# BUTTONS (ALL ORANGE)
ctk.CTkButton(right_frame, text="Generate Bill", fg_color="#FF8C00", hover_color="#e07b00", command=generate_bill).pack(pady=5)
ctk.CTkButton(right_frame, text="Export PDF", fg_color="#FF8C00", hover_color="#e07b00", command=export_pdf).pack(pady=5)
ctk.CTkButton(right_frame, text="Clear", fg_color="#FF8C00", hover_color="#e07b00", command=clear_order).pack(pady=5)

app.mainloop()