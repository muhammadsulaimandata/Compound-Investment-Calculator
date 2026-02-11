import tkinter as tk
from tkinter import *
from tkinter import ttk
from tkinter import font

# -------------------- Calculation Logic ------------------------

def adjusted_contribution(monthly_contri, frequency):
    if frequency == 12:
        return monthly_contri
    elif frequency == 4:
        return monthly_contri * 3
    elif frequency == 1:
        return monthly_contri * 12
    return monthly_contri

def compound_interest_calculator(ini, rat, dur, contri, freq):
    rat = rat / 100
    total = ini * (1 + rat / freq) ** (freq * dur)
    total += contri * (((1 + rat / freq) ** (freq * dur) - 1) / (rat / freq))
    return total

def calculate_table(initial, rate, duration, monthly_contribution, frequency):
    rate = rate / 100
    contribution_per_period = adjusted_contribution(monthly_contribution, frequency)
    yearly_data = []

    total = initial
    for year in range(1, int(duration) + 1):
        total = total * (1 + rate / frequency) ** frequency
        total += contribution_per_period * (((1 + rate / frequency) ** frequency - 1) / (rate / frequency))
        total_contributions = initial + (monthly_contribution * 12 * year)
        interest_earned = total - total_contributions
        yearly_data.append((year, round(total_contributions, 2), round(interest_earned, 2), round(total, 2)))

    return yearly_data

def calculate_simple_table(principal, rate, time, monthly_contribution):
    yearly_data = []
    for year in range(1, int(time) + 1):
        total_contri = principal + (monthly_contribution * 12 * year)

        # Interest on principal (invested for full years)
        principal_interest = (principal * rate * year) / 100

        # Interest on monthly contributions (average duration ~ (year + 1)/2)
        contrib_interest = (monthly_contribution * 12 * rate * (year + 1)) / (2 * 100)

        total_interest = principal_interest + contrib_interest
        total_amount = total_contri + total_interest

        yearly_data.append((year, round(total_contri, 2), round(total_interest, 2), round(total_amount, 2)))

    return yearly_data

def select(event):
    selected_item = combo_box.get()

def clear_table():
    for row in table.get_children():
        table.delete(row)
    # for clearing entry fields
    entry_initial.delete(0, tk.END)
    entry_rate.delete(0, tk.END)
    entry_duration.delete(0, tk.END)
    entry_monthly.delete(0, tk.END)

    # to reset combox to default
    combo_box.set("Monthly")

    # clearing result labels
    label_total.config(text="")
    label_interest.config(text="")
    label_contri.config(text="")

def simple_interest_calculator(principal, rate, time):
    return (principal * rate * time) / 100


def calculate():
    for row in table.get_children():
        table.delete(row)

    try:
        ini = float(entry_initial.get())
        rate = float(entry_rate.get())
        dur = float(entry_duration.get())
        monthly = float(entry_monthly.get())
        freq_choice = combo_box.get()

        freq_dict = {"Monthly": 12, "Quarterly": 4, "Yearly": 1}
        freq = freq_dict.get(freq_choice, 12)
        interest_type = type_combo.get()


        if interest_type == "Simple Interest":
            rows = calculate_simple_table(ini, rate, dur, monthly)

            last_year = rows[-1]
            total_contri, interest, total_amt = last_year[1], last_year[2], last_year[3]

            label_total.config(text=f"Total Amount: Rs {total_amt}")
            label_interest.config(text=f"Simple Interest: Rs {interest}")
            label_contri.config(text=f"Total Contributions: Rs {total_contri}")

        else:
            contribution_per_period = adjusted_contribution(monthly, freq)
            final_amount = round(compound_interest_calculator(ini, rate, dur, contribution_per_period, freq), 2)
            total_contri = round(ini + monthly * 12 * dur, 2)
            interest = round(final_amount - total_contri, 2)

            label_total.config(text=f"Total Amount: {final_amount}")
            label_interest.config(text=f"Compound Interest: {interest}")
            label_contri.config(text=f"Total Contributions: {total_contri}")

        if interest_type == "Simple Interest":
            rows = calculate_simple_table(ini, rate, dur, monthly)
        else:
            rows = calculate_table(ini, rate, dur, monthly, freq)

        for row in rows:
            table.insert('', 'end', values=row)

    except ValueError:
        label_total.config(text="Invalid input. Please enter numeric values.")

# -------------------- GUI Setup ------------------------

root = tk.Tk()
root.title("Compound Interest Calculator")
root.geometry("750x650")
root.configure(bg="#f0f4f7")

# Labels and Entries
heading_label = Label(root, text = "Compound Interest Calculator")
heading_label.configure(font = ("Ariel", 30, "bold"))
heading_label.grid(row = 0, column = 1, columnspan = 10, pady = (10, 30), padx = (5, 0), sticky = "")

initial_label = Label(root, text="Initial Investment", bg="#f0f4f7")
initial_label.config(font = ("Ariel", 15, "bold"))
initial_label.grid(row=1, column=0, sticky="w", padx=(25, 0), pady=(5,5))
entry_initial = Entry(root)
entry_initial.grid(row=1, column=1, ipady = 5, ipadx = 20, pady=(5,5))

interest_label = Label(root, text="Annual Interest Rate (%)", bg="#f0f4f7", font=("Arial", 12))
interest_label.config(font = ("Ariel", 15, "bold"))
interest_label.grid(row=2, column=0, sticky="w", padx=20, pady=5)
entry_rate = tk.Entry(root)
entry_rate.grid(row=2, column=1, padx=20, pady=5, ipady = 5, ipadx = 20)

duration_label = Label(root, text="Investment Duration (Years)", bg="#f0f4f7", )
duration_label.config(font=("Arial", 15, "bold"))
duration_label.grid(row=3, column=0, sticky="w", padx=20, pady=5)
entry_duration = tk.Entry(root)
entry_duration.grid(row=3, column=1, padx=20, pady=5, ipady = 5, ipadx = 20)

contribution_label = Label(root, text="Monthly Contribution", bg="#f0f4f7")
contribution_label.config(font=("Arial", 15, "bold"))
contribution_label.grid(row=4, column=0, sticky="w", padx=20, pady=5)
entry_monthly = tk.Entry(root)
entry_monthly.grid(row=4, column=1, padx=20, pady=5, ipady = 5, ipadx = 20)

frequency_label = Label(root, text="Compounding Frequency", bg="#f0f4f7")
frequency_label.config(font=("Arial", 15, "bold"))
frequency_label.grid(row=5, column=0, sticky="w", padx=20, pady=5)

combo_box = ttk.Combobox(root, values=["Monthly", "Quarterly", "Yearly"])
combo_box.grid(row=5, column=1, padx=20, pady=5, ipady = 4, ipadx = 10)
combo_box.config(font = ("Arial", 15))
combo_box.set("Monthly")
combo_box.bind("<<ComboboxSelected>>", select)

type_label = Label(root, text="Select Interest Type:", bg="#f0f4f7")
type_label.config(font=("Arial", 15, "bold"))
type_label.grid(row=1, column=2, sticky="w", padx=20, pady=5)

type_combo = ttk.Combobox(root, values=["Compound Interest", "Simple Interest"])
type_combo.grid(row=1, column=3, padx=20, pady=5, ipady=4, ipadx=10)
type_combo.config(font=("Arial", 15))
type_combo.set("Compound Interest") 

# Calculate Button
calculate_button = Button(root, text="Calculate", command=calculate, bg="#4CAF50", fg="white")
calculate_button.config(font=("Arial", 15, "bold"))
calculate_button.grid(row=6, column=0, columnspan=1, pady=10, padx = (15, 5))

# Clear Button
clear_button = Button(root, text="Clear", command=clear_table, bg="#f44336", fg="white")
clear_button.config(font=("Arial", 14, "bold"))
clear_button.grid(row=6, column=1,pady=15, padx=(0, 20), ipadx = 20, ipady = 2)

# Result Labels
label_total = Label(root, text="", bg="#f0f4f7")
label_total.config( font=("Arial", 15, "bold"))
label_total.grid(row=7, column=0, columnspan=2, pady=5, padx = (0, 20))

label_interest = tk.Label(root, text="", bg="#f0f4f7" )
label_interest.config(font=("Arial", 15, "bold"))
label_interest.grid(row=8, column=0, columnspan=2, pady=5, padx = (0, 20))

label_contri = Label(root, text="", bg="#f0f4f7")
label_contri.config(font=("Arial", 15, "bold"))
label_contri.grid(row=9, column=0, columnspan=2, pady=5, padx = (0, 20))

# Table
table = ttk.Treeview(root, columns=("Year", "Contributions", "Interest", "Total Amount"), show='headings')
table.heading("Year", text="Year")
table.heading("Contributions", text="Total Contributions")
table.heading("Interest", text="Interest Earned")
table.heading("Total Amount", text="Total Amount")
table.grid(row=10, column=1, columnspan=9, padx=20, pady=10, sticky="")

# Optional: Add scrollbars for the table if needed
scrollbar = ttk.Scrollbar(root, orient="vertical", command=table.yview)
table.configure(yscrollcommand=scrollbar.set)
scrollbar.grid(row=10, column=10, sticky='ns')

root.mainloop()