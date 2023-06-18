import tkinter as tk

root = tk.Tk()
root.geometry('400x400')

# Define the table data
table_data = [
    ['Header 1', 'Header 2', 'Header 3'],
    ['Data 1', 'Data 2', 'Data 3'],
    ['Data 4', 'Data 5', 'Data 6']
]

# Create labels for table headers
for column, header in enumerate(table_data[0]):
    label = tk.Label(root, text=header, relief=tk.RIDGE, width=12)
    label.grid(row=0, column=column)

# Create labels for table data
for row, data_row in enumerate(table_data[1:], start=1):
    for column, data in enumerate(data_row):
        label = tk.Label(root, text=data, relief=tk.GROOVE, width=12)
        label.grid(row=row, column=column)
        label.place(x=20+column*100, y=row*100)

root.mainloop()