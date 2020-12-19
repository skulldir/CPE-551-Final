import requests
from tkinter import *
import tkinter as tk
from tkinter import ttk

class CurrencyConverter():

    def __init__(self,url):
        self.data = requests.get(url).json()
        self.currencies = self.data['rates']

    def convert(self, from_currency, to_currency, amount):
        initial_amount = amount

        if (from_currency != 'USD') :
            amount = amount / self.currencies[from_currency]

        converted_amount = round(amount * self.currencies[to_currency],2)
        return converted_amount
class CurrencyConverterUI(tk.Tk):
    def __init__(self,converter):
        tk.Tk.__init__(self)
        self.title = 'Currency Converter'
        self.currency_converter = converter
        self.geometry('550x200')

        self.intro_label = Label(self, text = 'Currency Converter', fg = 'green', relief = tk.RAISED, width = 17, borderwidth = 3)
        self.intro_label.config(font = ('Helvetica', 20, 'bold'))
        
        self.intro_label.place(x = 120, y = 5)
        valid = (self.register(self.restrictNumberOnly), '%d', '%P')
        self.amount_field = Entry(self,bd = 3, relief = tk.RIDGE, justify = tk.CENTER,validate='key', validatecommand=valid, width = 15)
        self.converted_amount_field_label = Label(self, text = '', fg = 'black', bg = 'white', relief = tk.RIDGE, justify = tk.CENTER, width = 15, borderwidth = 3)
         

        self.from_currency_variable = StringVar(self)
        self.from_currency_variable.set("INR")
        self.to_currency_variable = StringVar(self)
        self.to_currency_variable.set("USD")
        font = ("Helvetica", 12, "bold")
        self.option_add('*TCombobox*Listbox.font', font)
        self.from_currency_dropdown = ttk.Combobox(self, textvariable=self.from_currency_variable,values=list(self.currency_converter.currencies.keys()), font = font, state = 'readonly', width = 12, justify = tk.CENTER)
        self.to_currency_dropdown = ttk.Combobox(self, textvariable=self.to_currency_variable,values=list(self.currency_converter.currencies.keys()), font = font, state = 'readonly', width = 12, justify = tk.CENTER)
         

        self.from_currency_dropdown.place(x = 23, y= 124)
        self.amount_field.place(x = 20, y = 150)
        self.to_currency_dropdown.place(x = 331, y= 124)
        self.converted_amount_field_label.place(x = 330, y = 150)

        self.convert_button = Button(self, text = "Convert", fg = "black", command = self.perform) 
        self.convert_button.config(font=('Helvetica', 10, 'bold'))
        self.convert_button.place(x = 225, y = 75)

        
    def perform(self,):
        amount = float(self.amount_field.get())
        from_curr = self.from_currency_variable.get()
        to_curr = self.to_currency_variable.get()
 
        converted_amount= self.currency_converter.convert(from_curr,to_curr,amount)
        converted_amount = round(converted_amount, 2)
     
        self.converted_amount_field_label.config(text = str(converted_amount))
    def restrictNumberOnly(self, action, string):
        regex = re.compile(r"[0-9,]*?(\.)?[0-9,]*$")
        result = regex.match(string)
        return (string == "" or (string.count('.') <= 1 and result is not None))
    


if __name__ == '__main__':
    url = 'https://api.exchangerate-api.com/v4/latest/USD'
    converter = CurrencyConverter(url)
    CurrencyConverterUI(converter)
    mainloop()
