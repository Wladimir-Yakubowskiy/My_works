from tkinter import *

root = Tk()
root.geometry('240x270+100+200') #параметры окна в пикселях
root['bg'] = 'gray'
root.title('Калькулятор')

def press_key(event):
    if event.char.isdigit():
        add_digital(event.char)
    elif event.char in '+-*/':
        add_operation(event.char)
    elif event.char == '\r':
        calculate()

root.bind('<Key>', press_key)

def add_digital(digit):
    value = calc.get()
    if value[0] == '0' and len(value) == 1:
        value = value[1:]
    calc['state'] = NORMAL
    calc.delete(0, END)
    calc.insert(0, value + digit)
    calc['state'] = DISABLED

def add_operation(operation):
    value = calc.get()
    if value[-1] in '+-/*':
        value = value[:-1]
    calc['state'] = NORMAL
    calc.delete(0, END)
    calc.insert(0, value + operation)
    calc['state'] = DISABLED

def calculate():
    value = calc.get()
    calc['state'] = NORMAL
    if value[-1] not in '/*+-':
        calc.delete(0, END)
        calc.insert(0, eval(value))
        calc['state'] = DISABLED

def delete_digital():
    calc['state'] = NORMAL
    calc.delete(0, END)
    calc.insert(0, '0')
    calc['state'] = DISABLED

def make_digit_button(digit):
    return Button(text=digit, bd=5, command = lambda:add_digital(digit))

def make_operation_button(operation):
    return Button(text=operation, bd=5, command = lambda:add_operation(operation))

def make_calc_button(operation):
    return Button(text=operation, bd=5, command = calculate)

def make_delete_button(operation):
    return Button(text=operation, bd=5, command = delete_digital)

calc = Entry(root, justify=RIGHT, font=('Arial', 15))
calc.insert(0, '0')
calc['state'] = DISABLED

calc.grid(row=0, column=0, columnspan=4, stick='we', padx=5)

make_digit_button('1').grid(row=1, column=0, stick='wens', padx=5, pady=5)
make_digit_button('2').grid(row=1, column=1, stick='wens', padx=5, pady=5)
make_digit_button('3').grid(row=1, column=2, stick='wens', padx=5, pady=5)
make_digit_button('4').grid(row=2, column=0, stick='wens', padx=5, pady=5)
make_digit_button('5').grid(row=2, column=1, stick='wens', padx=5, pady=5)
make_digit_button('6').grid(row=2, column=2, stick='wens', padx=5, pady=5)
make_digit_button('7').grid(row=3, column=0, stick='wens', padx=5, pady=5)
make_digit_button('8').grid(row=3, column=1, stick='wens', padx=5, pady=5)
make_digit_button('9').grid(row=3, column=2, stick='wens', padx=5, pady=5)
make_digit_button('0').grid(row=4, column=0, stick='wens', padx=5, pady=5)

make_operation_button('+').grid(row=1, column=3, stick='ewns', padx=5, pady=5)
make_operation_button('-').grid(row=2, column=3, stick='ewns', padx=5, pady=5)
make_operation_button('*').grid(row=3, column=3, stick='ewns', padx=5, pady=5)
make_operation_button('/').grid(row=4, column=3, stick='ewns', padx=5, pady=5)

make_calc_button('=').grid(row=4, column=2, stick='ewns', padx=5, pady=5)
make_delete_button('С').grid(row=4, column=1, stick='ewns', padx=5, pady=5)

root.grid_columnconfigure(0, minsize=60)
root.grid_columnconfigure(1, minsize=60)
root.grid_columnconfigure(2, minsize=60)
root.grid_columnconfigure(3, minsize=60)

root.grid_rowconfigure(1, minsize=60)
root.grid_rowconfigure(2, minsize=60)
root.grid_rowconfigure(3, minsize=60)
root.grid_rowconfigure(4, minsize=60)

root.mainloop()