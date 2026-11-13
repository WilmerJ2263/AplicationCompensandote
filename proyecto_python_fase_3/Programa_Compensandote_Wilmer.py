# PROGRAM: COMPENSANDOTE FAMILY COMPENSATION FUND
# Data Structures Project - Phase 3
# This program uses a stack, a queue, and a list to store affiliates
# Data stays in memory while the program is open

import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
from collections import deque
from datetime import datetime


# This class stores the information of an affiliate.
class AffiliateData:
    def __init__(self, document_type, document_number, name,
                 income, employment_type, service, fee, date):
        self.document_type = document_type
        self.document_number = document_number
        self.name = name
        self.income = income
        self.employment_type = employment_type
        self.service = service
        self.fee = fee
        self.date = date


# This class calculates the fee each affiliate must pay.
class FeeCalculator:
    def calculate_fee(self, income, employment_type, service):
        fee = 0

        # First, the fee is calculated according to the employment type.
        if employment_type == "Employee":
            if income <= 2000000:
                fee = 45000
            elif income <= 3000000:
                fee = 60000
            elif income <= 4000000:
                fee = 75000
            elif income <= 5000000:
                fee = 90000
            else:
                fee = 150000
        else:
            if income <= 2000000:
                fee = 10000
            elif income <= 3000000:
                fee = 20000
            elif income <= 4000000:
                fee = 30000
            elif income <= 5000000:
                fee = 40000
            else:
                fee = 80000

        # Then, the cost of the selected service is added.
        if service == "Park entry":
            fee = fee + 2500
        elif service == "Training course":
            fee = fee + 7500
        elif service == "Travel package":
            fee = fee + 10000
        elif service == "Preventive medicine":
            fee = fee + (income * 0.10)

        return fee


# This is the window where the user enters the password.
class LoginWindow:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("Login - Compensandote")
        self.window.geometry("420x350")
        self.window.resizable(False, False)

        tk.Label(self.window, text="Compensandote",
                 font=("Arial", 20, "bold")).pack(pady=18)
        tk.Label(self.window, text="Family Compensation Fund").pack(pady=4)
        tk.Label(self.window, text="Password:").pack(pady=(20, 5))

        self.password_field = tk.Entry(self.window, show="*")
        self.password_field.pack(padx=45, fill="x")
        self.password_field.focus()

        tk.Button(self.window, text="About",
                  command=self.show_about).pack(pady=10)
        tk.Button(self.window, text="Log in",
                  command=self.check_password).pack(pady=4)
        tk.Button(self.window, text="Exit",
                  command=self.window.destroy).pack(pady=4)

        self.window.mainloop()

    # Shows the student's information.
    def show_about(self):
        message = (
            "Course: Data Structures - 301305\n\n"
            "Student: Wilmer José Gómez Ospino\n\n"
            "Collaborative group: 301305_47\n\n"
            "Institution: UNAD - ECBTI"
        )
        messagebox.showinfo("About", message)

    # Checks whether the password is correct.
    def check_password(self):
        password = self.password_field.get()

        if password == "Caja":
            self.window.destroy()
            AffiliatesWindow()
        else:
            messagebox.showerror("Error", "The password is incorrect.")
            self.password_field.delete(0, tk.END)


# This class contains the form and the three data structures.
class AffiliatesWindow:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("Compensandote Fund - Affiliate Management")
        self.window.geometry("1200x700")
        self.window.minsize(1000, 620)

        # The stack is stored in a list.
        self.stack = []

        # The queue is stored using deque.
        self.queue = deque()

        # The affiliate list is stored in another list.
        self.records_list = []

        self.calculator = FeeCalculator()

        self.create_interface()
        self.window.mainloop()

    # Creates the elements of the window.
    def create_interface(self):
        title = tk.Label(
            self.window,
            text="Compensandote - Affiliate Management",
            font=("Arial", 16, "bold")
        )
        title.pack(pady=10)

        main_frame = tk.Frame(self.window)
        main_frame.pack(fill="both", expand=True, padx=10, pady=5)

        # Left panel: form.
        form = tk.LabelFrame(
            main_frame, text="Affiliate information", padx=10, pady=8
        )
        form.pack(side="left", fill="y", padx=5)

        tk.Label(form, text="Data structure:").pack(anchor="w")
        self.structure_selection = ttk.Combobox(
            form, values=["Stack", "Queue", "List"], state="readonly"
        )
        self.structure_selection.current(0)
        self.structure_selection.pack(fill="x", pady=3)
        self.structure_selection.bind(
            "<<ComboboxSelected>>", self.change_structure
        )

        tk.Label(form, text="Document type:").pack(anchor="w")
        self.document_type_selection = ttk.Combobox(
            form, values=["CC", "CE", "NUIP", "PAS"], state="readonly"
        )
        self.document_type_selection.current(0)
        self.document_type_selection.pack(fill="x", pady=3)

        tk.Label(form, text="Document number:").pack(anchor="w")
        self.document_field = tk.Entry(form)
        self.document_field.pack(fill="x", pady=3)

        tk.Label(form, text="Full name:").pack(anchor="w")
        self.name_field = tk.Entry(form)
        self.name_field.pack(fill="x", pady=3)

        tk.Label(form, text="Current income:").pack(anchor="w")
        self.income_field = tk.Entry(form)
        self.income_field.pack(fill="x", pady=3)
        self.income_field.bind("<KeyRelease>", self.update_fee)

        tk.Label(form, text="Employment type:").pack(anchor="w")
        self.employment_type = tk.StringVar(value="Employee")
        tk.Radiobutton(
            form, text="Employee", variable=self.employment_type,
            value="Employee", command=self.update_fee
        ).pack(anchor="w")
        tk.Radiobutton(
            form, text="Self-employed", variable=self.employment_type,
            value="Self-employed", command=self.update_fee
        ).pack(anchor="w")

        tk.Label(form, text="Selected service:").pack(anchor="w")
        self.service_selection = ttk.Combobox(
            form,
            values=[
                "Unemployment subsidy",
                "Park entry",
                "Training course",
                "Travel package",
                "Preventive medicine"
            ],
            state="readonly"
        )
        self.service_selection.current(0)
        self.service_selection.pack(fill="x", pady=3)
        self.service_selection.bind(
            "<<ComboboxSelected>>", self.update_fee
        )

        tk.Label(form, text="Membership fee:").pack(anchor="w")
        self.fee_field = tk.Entry(form, state="readonly")
        self.fee_field.pack(fill="x", pady=3)

        tk.Label(form, text="Membership date:").pack(anchor="w")
        date_frame = tk.Frame(form)
        date_frame.pack(fill="x", pady=3)

        current_date = datetime.now()
        self.day = tk.Spinbox(date_frame, from_=1, to=31, width=4)
        self.day.pack(side="left")
        self.day.delete(0, tk.END)
        self.day.insert(0, current_date.day)

        self.month = tk.Spinbox(date_frame, from_=1, to=12, width=4)
        self.month.pack(side="left", padx=3)
        self.month.delete(0, tk.END)
        self.month.insert(0, current_date.month)

        self.year = tk.Spinbox(date_frame, from_=2000, to=2100, width=6)
        self.year.pack(side="left")
        self.year.delete(0, tk.END)
        self.year.insert(0, current_date.year)

        tk.Label(form, text="Report:").pack(anchor="w", pady=(8, 0))
        self.report_field = tk.Entry(form, state="readonly", width=35)
        self.report_field.pack(fill="x", pady=3)

        # Right panel: records table.
        table_panel = tk.Frame(main_frame)
        table_panel.pack(side="right", fill="both", expand=True, padx=5)

        self.table_title = tk.Label(
            table_panel, text="Registered affiliates - Stack",
            font=("Arial", 12, "bold")
        )
        self.table_title.pack(anchor="w", pady=5)

        columns = (
            "type", "document", "name", "income",
            "employment", "service", "fee", "date"
        )
        self.table = ttk.Treeview(
            table_panel, columns=columns, show="headings"
        )

        column_names = [
            ("type", "Type"),
            ("document", "Document"),
            ("name", "Name"),
            ("income", "Income"),
            ("employment", "Employment"),
            ("service", "Service"),
            ("fee", "Fee"),
            ("date", "Date")
        ]

        for identifier, column_name in column_names:
            self.table.heading(identifier, text=column_name)
            self.table.column(identifier, width=100, anchor="center")

        self.table.column("name", width=150)
        self.table.column("service", width=140)

        scrollbar = ttk.Scrollbar(
            table_panel, orient="vertical", command=self.table.yview
        )
        self.table.configure(yscrollcommand=scrollbar.set)
        self.table.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        # Buttons required by the guide.
        buttons_frame = tk.Frame(self.window)
        buttons_frame.pack(fill="x", padx=10, pady=10)

        tk.Button(
            buttons_frame, text="Register",
            command=self.register_affiliate
        ).pack(side="left", expand=True, fill="x", padx=4)
        tk.Button(
            buttons_frame, text="Clear",
            command=self.clear_form
        ).pack(side="left", expand=True, fill="x", padx=4)
        tk.Button(
            buttons_frame, text="Report",
            command=self.generate_report
        ).pack(side="left", expand=True, fill="x", padx=4)
        tk.Button(
            buttons_frame, text="Delete",
            command=self.delete_record
        ).pack(side="left", expand=True, fill="x", padx=4)
        tk.Button(
            buttons_frame, text="Exit",
            command=self.window.destroy
        ).pack(side="left", expand=True, fill="x", padx=4)

    # Returns the selected data structure.
    def get_selected_data(self):
        structure = self.structure_selection.get()

        if structure == "Stack":
            return self.stack
        elif structure == "Queue":
            return self.queue
        else:
            return self.records_list

    # Updates the title and table when the structure changes.
    def change_structure(self, event=None):
        structure = self.structure_selection.get()
        self.table_title.config(
            text="Registered affiliates - " + structure
        )
        self.show_records()
        self.show_report("")

    # Calculates and displays the fee without allowing the user to edit it.
    def update_fee(self, event=None):
        try:
            income_text = self.income_field.get().strip()

            if income_text == "":
                self.show_fee("")
                return

            income = float(income_text)
            fee = self.calculator.calculate_fee(
                income, self.employment_type.get(),
                self.service_selection.get()
            )
            self.show_fee("$" + format(fee, ",.2f"))
        except ValueError:
            self.show_fee("")

    # Writes the value in the fee field.
    def show_fee(self, value):
        self.fee_field.config(state="normal")
        self.fee_field.delete(0, tk.END)
        self.fee_field.insert(0, value)
        self.fee_field.config(state="readonly")

    # Writes the report in the corresponding field.
    def show_report(self, value):
        self.report_field.config(state="normal")
        self.report_field.delete(0, tk.END)
        self.report_field.insert(0, value)
        self.report_field.config(state="readonly")

    # Checks whether the form information is correct.
    def validate_data(self):
        document = self.document_field.get().strip()
        name = self.name_field.get().strip()
        income_text = self.income_field.get().strip()

        if document == "" or name == "" or income_text == "":
            messagebox.showwarning(
                "Incomplete information", "Please complete all the fields."
            )
            return False

        if not document.isdigit():
            messagebox.showwarning(
                "Incorrect information",
                "The document number must contain numbers only."
            )
            return False

        if not name.replace(" ", "").isalpha():
            messagebox.showwarning(
                "Incorrect information",
                "The name must contain letters and spaces only."
            )
            return False

        try:
            income_value = float(income_text)
            if income_value <= 0:
                raise ValueError
        except ValueError:
            messagebox.showwarning(
                "Incorrect information",
                "Income must be a number greater than zero."
            )
            return False

        try:
            datetime(
                int(self.year.get()),
                int(self.month.get()),
                int(self.day.get())
            )
        except ValueError:
            messagebox.showwarning(
                "Incorrect date", "Please check the day, month, and year."
            )
            return False

        return True

    # Saves an affiliate in the selected data structure.
    def register_affiliate(self):
        if not self.validate_data():
            return

        document_type = self.document_type_selection.get()
        document = self.document_field.get().strip()
        name = self.name_field.get().strip()
        income = float(self.income_field.get())
        employment = self.employment_type.get()
        service = self.service_selection.get()

        fee = self.calculator.calculate_fee(income, employment, service)

        date = (
            str(self.day.get()).zfill(2) + "/" +
            str(self.month.get()).zfill(2) + "/" +
            str(self.year.get())
        )

        affiliate = AffiliateData(
            document_type, document, name, income,
            employment, service, fee, date
        )

        structure = self.structure_selection.get()

        if structure == "Stack":
            self.stack.append(affiliate)
        elif structure == "Queue":
            self.queue.append(affiliate)
        else:
            self.records_list.append(affiliate)

        self.show_records()
        self.show_report("")
        messagebox.showinfo(
            "Registration completed",
            "The affiliate was added to the " + structure + "."
        )
        self.clear_form()

    # Displays the affiliates in the selected structure.
    def show_records(self):
        for item in self.table.get_children():
            self.table.delete(item)

        structure = self.structure_selection.get()
        data = self.get_selected_data()

        if structure == "Stack":
            data = reversed(data)

        for affiliate in data:
            self.table.insert("", tk.END, values=(
                affiliate.document_type,
                affiliate.document_number,
                affiliate.name,
                "$" + format(affiliate.income, ",.2f"),
                affiliate.employment_type,
                affiliate.service,
                "$" + format(affiliate.fee, ",.2f"),
                affiliate.date
            ))

    # Clears the form fields but keeps the saved records.
    def clear_form(self):
        self.document_field.delete(0, tk.END)
        self.name_field.delete(0, tk.END)
        self.income_field.delete(0, tk.END)
        self.show_fee("")
        self.show_report("")
        self.document_field.focus()

    # Creates the report required by the guide for each structure.
    def generate_report(self):
        structure = self.structure_selection.get()
        data = self.get_selected_data()

        if structure == "Stack":
            total = 0
            for affiliate in data:
                total = total + affiliate.fee
            report_text = "Sum of fees: $" + format(total, ",.2f")

        elif structure == "Queue":
            report_text = "Number of records: " + str(len(data))

        else:
            if len(data) == 0:
                report_text = "There are no records to calculate the average."
            else:
                total = 0
                for affiliate in data:
                    total = total + affiliate.income
                average = total / len(data)
                report_text = "Average income: $" + format(average, ",.2f")

        self.show_report(report_text)

    # Deletes a record according to the behavior of each structure.
    def delete_record(self):
        structure = self.structure_selection.get()
        data = self.get_selected_data()

        if len(data) == 0:
            messagebox.showwarning(
                "No records", "There are no affiliates to delete."
            )
            return

        if structure == "List":
            document = simpledialog.askstring(
                "Delete affiliate",
                "Enter the affiliate's document number:"
            )

            if document is None:
                return

            found_affiliate = None

            for affiliate in data:
                if affiliate.document_number == document.strip():
                    found_affiliate = affiliate
                    break

            if found_affiliate is None:
                messagebox.showwarning(
                    "Not found", "There is no affiliate with that document number."
                )
                return

            confirm = messagebox.askyesno(
                "Confirm deletion",
                "Do you want to delete " + found_affiliate.name + "?"
            )

            if confirm:
                data.remove(found_affiliate)

        else:
            if structure == "Stack":
                affiliate = data[-1]
                action = "remove the last item from the stack"
            else:
                affiliate = data[0]
                action = "remove the first item from the queue"

            confirm = messagebox.askyesno(
                "Confirm deletion",
                "The record for " + affiliate.name + " will be removed. "
                "Do you want to continue?"
            )

            if confirm:
                if structure == "Stack":
                    data.pop()
                else:
                    data.popleft()

        self.show_records()
        self.show_report("")


# This instruction starts the program.
if __name__ == "__main__":
    LoginWindow()