import tkinter as tk
from tkinter import ttk, messagebox

# =========================
# BOLT SIZES
# =========================

bolt_sizes = {
    "M4": 0.004,
    "M5": 0.005,
    "M6": 0.006,
    "M8": 0.008,
    "M10": 0.010,
    "M12": 0.012,
    "M14": 0.014,
    "M16": 0.016,
    "M18": 0.018,
    "M20": 0.020
}

# =========================
# MATERIALS
# =========================

materials = {
    "เหล็ก": {
        "4.6": 4000,
        "8.8": 8000,
        "10.9": 12000,
        "12.9": 15000
    },

    "สแตนเลส": {
        "304": 5200,
        "316": 5800
    },

    "อลูมิเนียม": {
        "6061": 3100,
        "7075": 5500
    },

    "ไทเทเนียม": {
        "Grade 2": 9000,
        "Grade 5": 14000
    },

    "ทองเหลือง": {
        "Standard": 2500
    }
}

# =========================
# UPDATE GRADE LIST
# =========================

def update_grades(event=None):

    material = material_var.get()

    grades = list(materials[material].keys())

    grade_combo["values"] = grades

    if grades:
        grade_combo.set(grades[0])

# =========================
# CALCULATE
# =========================

def calculate():

    size = bolt_var.get()
    material = material_var.get()
    grade = grade_var.get()
    length_text = entry_length.get()

    if not size or not material or not grade or not length_text:
        messagebox.showerror(
            "Error",
            "กรอกข้อมูลให้ครบ"
        )
        return

    try:

        length = float(length_text)

        d = bolt_sizes[size]

        F = materials[material][grade]

        K = float(
            k_var.get().split(" - ")[0]
        )

        # Torque
        T = K * F * d

        # lb-ft
        lbft = T * 0.73756

        # Clamp Force
        clamp_force = T / (K * d)

        result = f"""
SYSTEM READY

🧱 Material : {material}
🔩 Bolt Size : {size}
🛠 Grade     : {grade}
📏 Length    : {length} mm

⚙ K Factor   : {K}

========================

Torque
{T:.2f} N·m
{lbft:.2f} lb-ft

========================

Clamp Force
{clamp_force:.2f} N
"""

        result_label.config(text=result)

    except ValueError:

        messagebox.showerror(
            "Error",
            "ใส่ตัวเลขไม่ถูกต้อง"
        )

# =========================
# CLEAR
# =========================

def clear():

    entry_length.delete(0, tk.END)

    bolt_combo.set("M6")

    material_combo.set("เหล็ก")

    update_grades()

    k_combo.set(
        "0.20 - น็อตแห้งทั่วไป"
    )

    result_label.config(
        text="READY"
    )

# =========================
# WINDOW
# =========================

root = tk.Tk()

root.title(
    "BoltPro Engineering Suite"
)

root.geometry("460x720")

root.configure(bg="#181818")

# =========================
# STYLE
# =========================

style = ttk.Style()

style.theme_use("clam")

# Labels
style.configure(
    "TLabel",
    background="#202020",
    foreground="white",
    font=("Segoe UI", 10)
)

# Normal Button
style.configure(
    "TButton",
    background="#2d2d2d",
    foreground="white",
    font=("Segoe UI", 10),
    padding=8
)

style.map(
    "TButton",
    background=[
        ("active", "#3a3a3a")
    ]
)

# Accent Button
style.configure(
    "Accent.TButton",
    background="#0078D7",
    foreground="white",
    font=("Segoe UI", 10, "bold"),
    padding=10
)

style.map(
    "Accent.TButton",
    background=[
        ("active", "#2893FF")
    ]
)

# Combobox
style.configure(
    "TCombobox",
    fieldbackground="#2d2d2d",
    background="#2d2d2d",
    foreground="white"
)

# =========================
# HEADER BAR
# =========================

header = tk.Frame(
    root,
    bg="#0078D7",
    height=65
)

header.pack(fill="x")

header.pack_propagate(False)

header_title = tk.Label(
    header,
    text="🔩 BoltPro Engineering Suite",
    bg="#0078D7",
    fg="white",
    font=("Segoe UI", 18, "bold")
)

header_title.pack(pady=14)

# =========================
# INPUT FRAME
# =========================

input_frame = tk.LabelFrame(
    root,
    text="  Bolt Configuration  ",
    bg="#202020",
    fg="white",
    font=("Segoe UI", 10, "bold"),
    bd=2
)

input_frame.pack(
    padx=20,
    pady=20,
    fill="both"
)

# =========================
# BOLT SIZE
# =========================

ttk.Label(
    input_frame,
    text="🔩 ขนาดน็อต"
).pack(
    pady=(15, 5)
)

bolt_var = tk.StringVar()

bolt_combo = ttk.Combobox(
    input_frame,
    textvariable=bolt_var,
    values=list(bolt_sizes.keys()),
    state="readonly"
)

bolt_combo.pack(
    pady=5,
    padx=20,
    ipady=3
)

bolt_combo.set("M6")

# =========================
# MATERIAL
# =========================

ttk.Label(
    input_frame,
    text="🧱 วัสดุ"
).pack(
    pady=(15, 5)
)

material_var = tk.StringVar()

material_combo = ttk.Combobox(
    input_frame,
    textvariable=material_var,
    values=list(materials.keys()),
    state="readonly"
)

material_combo.pack(
    pady=5,
    padx=20,
    ipady=3
)

material_combo.set("เหล็ก")

material_combo.bind(
    "<<ComboboxSelected>>",
    update_grades
)

# =========================
# GRADE
# =========================

ttk.Label(
    input_frame,
    text="🛠 เกรดวัสดุ"
).pack(
    pady=(15, 5)
)

grade_var = tk.StringVar()

grade_combo = ttk.Combobox(
    input_frame,
    textvariable=grade_var,
    values=[],
    state="readonly"
)

grade_combo.pack(
    pady=5,
    padx=20,
    ipady=3
)

update_grades()

# =========================
# K VALUE
# =========================

ttk.Label(
    input_frame,
    text="⚙ ค่า K"
).pack(
    pady=(15, 5)
)

k_var = tk.StringVar()

k_combo = ttk.Combobox(
    input_frame,
    textvariable=k_var,
    values=[
        "0.10 - จาระบีเยอะ",
        "0.15 - มีน้ำมัน",
        "0.20 - น็อตแห้งทั่วไป",
        "0.25 - เกลียวฝืด/สนิม"
    ],
    state="readonly"
)

k_combo.pack(
    pady=5,
    padx=20,
    ipady=3
)

k_combo.set(
    "0.20 - น็อตแห้งทั่วไป"
)

# =========================
# LENGTH
# =========================

ttk.Label(
    input_frame,
    text="📏 ความยาวเกลียว (mm)"
).pack(
    pady=(15, 5)
)

entry_length = tk.Entry(
    input_frame,
    bg="#2d2d2d",
    fg="white",
    insertbackground="white",
    relief="flat",
    font=("Segoe UI", 10)
)

entry_length.pack(
    pady=(5, 20),
    ipadx=40,
    ipady=8
)

# =========================
# BUTTONS
# =========================

ttk.Button(
    root,
    text="CALCULATE",
    style="Accent.TButton",
    command=calculate
).pack(
    pady=(10, 8),
    ipadx=25
)

ttk.Button(
    root,
    text="CLEAR",
    command=clear
).pack(
    pady=5,
    ipadx=15
)

# =========================
# RESULT CONSOLE
# =========================

result_label = tk.Label(
    root,
    text="READY",
    bg="#111111",
    fg="#00FF7F",
    justify="left",
    anchor="nw",
    font=("Consolas", 11),
    padx=20,
    pady=20
)

result_label.pack(
    padx=20,
    pady=20,
    fill="both"
)

# =========================
# EXIT BUTTON
# =========================

ttk.Button(
    root,
    text="EXIT",
    command=root.quit
).pack(
    pady=(0, 20),
    ipadx=15
)

# =========================
# START
# =========================

root.mainloop()