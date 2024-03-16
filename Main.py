import tkinter as tk
from tkinter import ttk
import pandas as pd
import tkinter as tk

VALID_USERNAME = "admin"
VALID_PASSWORD = "password"

dmu_divisions = {
    "DMU 1": {
        "Division 1A": ["Village 1A1", "Village 1A2", "Village 1A3"],
        "Division 1B": ["Village 1B1", "Village 1B2", "Village 1B3"],
        "Division 1C": ["Village 1C1", "Village 1C2", "Village 1C3"]
    },
    "DMU 2": {
        "Division 2A": ["Village 2A1", "Village 2A2", "Village 2A3"],
        "Division 2B": ["Village 2B1", "Village 2B2", "Village 2B3"],
        "Division 2C": ["Village 2C1", "Village 2C2", "Village 2C3"]
    },
    "DMU 3": {
        "Division 3A": ["Village 3A1", "Village 3A2", "Village 3A3"],
        "Division 3B": ["Village 3B1", "Village 3B2", "Village 3B3"],
        "Division 3C": ["Village 3C1", "Village 3C2", "Village 3C3"]
    },
}

def login():
    if username_entry.get() == VALID_USERNAME and password_entry.get() == VALID_PASSWORD:
        show_dmu_page()
    else:
        status_label.config(text="Invalid username or password")

def show_dmu_page():
    login_frame.pack_forget()
    dmu_frame.pack()

def on_select(col_1):
    selected_value = col_1.widget.get()
    print("Selected:", selected_value)
    
def select_dmu():
    selected_dmu = dmu_combobox.get()
    selected_division = division_combobox.get()
    selected_village = village_combobox.get()
    print("Selected DMU:", selected_dmu)
    print("Selected Division:", selected_division)
    print("Selected Village:", selected_village)
    open_data_entry_window(selected_dmu, selected_division, selected_village)

def open_data_entry_window(selected_dmu, selected_division, selected_village):
    data_entry_window = tk.Toplevel(root)
    data_entry_window.title("Data Entry")

    frame = tk.Frame(data_entry_window)
    frame.pack(fill="both", expand=True)

    canvas = tk.Canvas(frame)
    scrollbar = ttk.Scrollbar(frame, orient="vertical", command=canvas.yview)
    scrollbar.pack(side="right", fill="y")
    canvas.pack(side="left", fill="both", expand=True)
    canvas.configure(yscrollcommand=scrollbar.set)

    inner_frame = tk.Frame(canvas)
    canvas.create_window((0, 0), window=inner_frame, anchor="nw")

    labels = ["Illiterate Female", "Illiterate Male", "Literate Female", "Literate Male",
              "Senior Secondary Female", "Senior Secondary Male", "Graduate Female", "Graduate Male",
              "PG Female", "PG Male", "Above PG Female", "Above PG Male","Major Crops to be Grown",
              "Average Area Under Crops (In Ha.)","Area Unit","Average Production per Ha. (In Quintal)","Production Unit",
              "Species Name","Expected Demand (Nos.)","Place of Plantation","No. of Persons willing to Purchase","Profit expected from Species (Rs.)","Remarks",
              "Bank Name","Branch No. & Name","Account No.","Account Type","Account Opening Date","SC No. of Families","SC Female","SC Male","SC Child Female",
              "SC Child Male","ST No. of Families","ST Female","ST Male","ST Child Female","ST Child Male","OBC No. of Families","OBC Female",
              "OBC Male","OBC Child Female","OBC Child Male","Others No. of Families","Others Female","Others Male","Others Child Female",
              "Others Child Male","NoFamilies Below Poverty Line","Female Below Poverty Line","Male Below Poverty Line","Child Below Poverty Line",
              "NoFamilies Above Poverty Line","Female Above Poverty Line","Male Above Poverty Line","Child Above Poverty Line","Name of Forest Produce",
              "Estimated No. of Days for Collection","Estimated No. of Families Involved in Collection","Unit","Estimated Collection Quantity per Year",
              "Total Female Member","Total Male Member","BPL Female","BPL Male","APL Female","APL Male","Landless Female",
              "Landless Male","Marginal Farmer Female","Marginal Farmer Male","Small Farmer Female","Small Farmer Male","Medium Farmer Female","Medium Farmer Male",
              "Big Farmer Female","Big Farmer Male","(Daily Wages) Complete Dependent Female","(Daily Wages) Complete Dependent Male","(Daily Wages) Partial Dependent Female",
              "(Daily Wages) Partial Dependent Male","(Daily Wages) Non Dependent Female","(Daily Wages) Non Dependent Male"]
    entry_fields = []
    for i, label_text in enumerate(labels):
        label = tk.Label(inner_frame, text=label_text)
        label.grid(row=i, column=0, padx=5, pady=2, sticky="w")

        entry = tk.Entry(inner_frame)
        entry.grid(row=i, column=1, padx=5, pady=2, sticky="ew")
        entry_fields.append(entry)

    def save_data():
        data = {
            "DMU": selected_dmu,
            "Division": selected_division,
            "Village": selected_village,
        }

        for i, label_text in enumerate(labels):
            data[label_text] = entry_fields[i].get()

        print("Data to be saved:", data)

        try:
            existing_data = pd.read_excel("data.xlsx")
        except FileNotFoundError:
            existing_data = pd.DataFrame()

        new_data = pd.DataFrame(data, index=[0])
        updated_data = pd.concat([existing_data, new_data], ignore_index=True)
        updated_data.to_excel("data.xlsx", index=False)
        print("Data saved successfully")

        data_entry_window.destroy()

    save_button = tk.Button(inner_frame, text="Save", command=save_data)
    save_button.grid(row=len(labels) + 1, columnspan=2, pady=10)

    inner_frame.update_idletasks()
    canvas.config(scrollregion=canvas.bbox("all"))

def search_data():
    search_window = tk.Toplevel(root)
    search_window.title("Search Data")

    def save_data():
        selected_column = column_combobox.get()

        if selected_column:
            try:
                df = pd.read_excel("data.xlsx")
                selected_data = df[selected_column].tolist()
            except FileNotFoundError:
                selected_data = []

            new_data = pd.DataFrame({selected_column: selected_data})
            new_data.to_excel("selected_data.xlsx", index=False)
            print("Data saved successfully")

            search_window.destroy()
        else:
            print("Please select a column")

    search_frame = tk.Frame(search_window)
    search_frame.pack(padx=20, pady=20)

    column_label = tk.Label(search_frame, text="Select Column:")
    column_label.grid(row=0, column=0, padx=5, pady=5)

    try:
        df = pd.read_excel("data.xlsx")
        column_names = df.columns.tolist()
    except FileNotFoundError:
        column_names = []

    column_combobox = ttk.Combobox(search_frame, values=column_names)
    column_combobox.grid(row=0, column=1, padx=5, pady=5)

    save_button = tk.Button(search_frame, text="Save Data", command=save_data)
    save_button.grid(row=1, columnspan=2, pady=10)

root = tk.Tk()
root.title("Forest Department App")

login_frame = tk.Frame(root)
login_frame.pack(padx=20, pady=20)

username_label = tk.Label(login_frame, text="Username:")
username_label.grid(row=0, column=0, sticky="w")
username_entry = tk.Entry(login_frame)
username_entry.grid(row=0, column=1)

password_label = tk.Label(login_frame, text="Password:")
password_label.grid(row=1, column=0, sticky="w")
password_entry = tk.Entry(login_frame, show="*")
password_entry.grid(row=1, column=1)

login_button = tk.Button(login_frame, text="Login", command=login)
login_button.grid(row=2, columnspan=2)

status_label = tk.Label(login_frame, text="")
status_label.grid(row=3, columnspan=2)

dmu_frame = tk.Frame(root)

dmu_label = tk.Label(dmu_frame, text="Select DMU:")
dmu_label.grid(row=0, column=0, padx=5, pady=5)

dmu_combobox = ttk.Combobox(dmu_frame, values=list(dmu_divisions.keys()))
dmu_combobox.grid(row=0, column=1, padx=5, pady=5)

division_label = tk.Label(dmu_frame, text="Select Division:")
division_label.grid(row=1, column=0, padx=5, pady=5)

division_combobox = ttk.Combobox(dmu_frame)
division_combobox.grid(row=1, column=1, padx=5, pady=5)

village_label = tk.Label(dmu_frame, text="Select Village:")
village_label.grid(row=2, column=0, padx=5, pady=5)

village_combobox = ttk.Combobox(dmu_frame)
village_combobox.grid(row=2, column=1, padx=5, pady=5)

def update_divisions(event):
    selected_dmu = dmu_combobox.get()
    division_list = list(dmu_divisions[selected_dmu].keys())
    division_combobox.config(values=division_list)
    division_combobox.set(division_list[0])
    update_villages(None)

def update_villages(event):
    selected_dmu = dmu_combobox.get()
    selected_division = division_combobox.get()
    village_list = dmu_divisions[selected_dmu][selected_division]
    village_combobox.config(values=village_list)
    village_combobox.set(village_list[0])

dmu_combobox.bind("<<ComboboxSelected>>", update_divisions)
division_combobox.bind("<<ComboboxSelected>>", update_villages)

select_button = tk.Button(dmu_frame, text="Select", command=select_dmu)
select_button.grid(row=3, column=0, pady=10)

search_button = tk.Button(dmu_frame, text="Search Data", command=search_data)
search_button.grid(row=3, column=1, pady=10)

dmu_frame.pack_forget()

root.mainloop()
