import requests
import tkinter as tk
from tkinter import ttk
from tkinter import scrolledtext

class CurrencyConverterGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Currency Converter")

        self.app_id = 'ca739fb19afc4344a7970d583f79d7a4'
        self.converter = CurrencyConverter(self.app_id)

        self.amount_label = ttk.Label(root, text="Введіть суму для конвертації:")
        self.amount_label.grid(row=0, column=0, padx=10, pady=10, sticky="W")

        self.amount_entry = ttk.Entry(root)
        self.amount_entry.grid(row=0, column=1, padx=10, pady=10)

        self.from_label = ttk.Label(root, text="Виберіть вихідну валюту:")
        self.from_label.grid(row=1, column=0, padx=10, pady=10, sticky="W")

        self.from_currency_combobox = ttk.Combobox(root, values=self.get_currency_list())
        self.from_currency_combobox.grid(row=1, column=1, padx=10, pady=10)
        self.from_currency_combobox.set("USD")

        self.to_label = ttk.Label(root, text="Виберіть цільову валюту:")
        self.to_label.grid(row=2, column=0, padx=10, pady=10, sticky="W")

        self.to_currency_combobox = ttk.Combobox(root, values=self.get_currency_list())
        self.to_currency_combobox.grid(row=2, column=1, padx=10, pady=10)
        self.to_currency_combobox.set("EUR")

        self.convert_button = ttk.Button(root, text="Конвертувати", command=self.convert_currency)
        self.convert_button.grid(row=3, column=0, columnspan=2, pady=10)

        self.result_label = ttk.Label(root, text="")
        self.result_label.grid(row=4, column=0, columnspan=2, pady=10)

        self.history_button = ttk.Button(root, text="Історія", command=self.show_history)
        self.history_button.grid(row=5, column=0, columnspan=2, pady=10)

        self.history_text = scrolledtext.ScrolledText(root, width=40, height=10, wrap=tk.WORD)
        self.history_text.grid(row=6, column=0, columnspan=2, padx=10, pady=10, sticky="W")

    def get_currency_list(self):
        rates = self.converter.get_exchange_rates()
        return list(rates.keys()) if rates else []

    def convert_currency(self):
        try:
            amount = float(self.amount_entry.get())
            from_currency = self.from_currency_combobox.get().upper()
            to_currency = self.to_currency_combobox.get().upper()

            converted_amount = self.converter.convert_currency(amount, from_currency, to_currency)
            if converted_amount is not None:
                result_text = f"{amount} {from_currency} = {converted_amount} {to_currency}"
                self.result_label.config(text=result_text)

                # Збереження історії конвертацій (просто для прикладу)
                history_entry = result_text
                with open('conversion_history.txt', 'a') as history_file:
                    history_file.write(history_entry + '\n')
            else:
                self.result_label.config(text="Помилка конвертації.")
        except ValueError:
            self.result_label.config(text="Будь ласка, введіть коректну суму.")
        except Exception as e:
            self.result_label.config(text=f"Помилка: {e}")

    def show_history(self):
        try:
            with open('conversion_history.txt', 'r') as history_file:
                history_text = history_file.read()
                self.history_text.delete(1.0, tk.END)
                self.history_text.insert(tk.END, history_text)
        except FileNotFoundError:
            self.history_text.delete(1.0, tk.END)
            self.history_text.insert(tk.END, "Історія порожня.")

class CurrencyConverter:
    def __init__(self, app_id):
        self.app_id = app_id
        self.base_url = 'https://openexchangerates.org/api/latest.json'

    def get_exchange_rates(self):
        try:
            response = requests.get(f"{self.base_url}?app_id={self.app_id}")
            response.raise_for_status()
            data = response.json()
            return data.get('rates')
        except requests.exceptions.RequestException as e:
            print(f"Error fetching exchange rates: {e}")
            return None

    def convert_currency(self, amount, from_currency, to_currency):
        rates = self.get_exchange_rates()
        if not rates:
            return None

        if from_currency == to_currency:
            return amount

        if from_currency != 'USD':
            amount_in_usd = amount / rates.get(from_currency, 1)
        else:
            amount_in_usd = amount

        converted_amount = amount_in_usd * rates.get(to_currency, 1)
        return converted_amount

if __name__ == "__main__":
    root = tk.Tk()
    app = CurrencyConverterGUI(root)
    root.mainloop()
