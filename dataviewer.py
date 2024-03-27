# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
import tkinter as tk
import matplotlib.pyplot as plt
from tkinter import messagebox
import os

# def createCheckboxGroup():


root = tk.Tk()
root.geometry("400x500")
root.title("Data Viewer")

availableDataSize = ['3k', '6k', '9k', '12k', '15k']
availablePeriod = ['10ms', '20ms', '30ms', '40ms', '50ms', '60ms', '70ms', '80ms', '90ms', '100ms']


# radio button
def handle_radio_selection():
    initialize_gui()


radio_var = tk.StringVar()  # Use StringVar for text-based values
radio_var.set("ConstSize")
radio1 = tk.Radiobutton(root, text="Compare different period with const data size", variable=radio_var,
                        value="ConstSize", command=handle_radio_selection)
radio2 = tk.Radiobutton(root, text="Compare different data size with const period", variable=radio_var,
                        value="ConstPeriod", command=handle_radio_selection)

radio1.place(x=10, y=10)
radio2.place(x=10, y=40)

# dropbox option
label1 = tk.Label(root, text='The size is set as :')
selected_option = tk.StringVar(root)
selected_option.set(availableDataSize[0])
option_menu = tk.OptionMenu(root, selected_option, *availableDataSize)
label1.place(x=10, y=70)
option_menu.place(x=200, y=70)

# checkboxes
label2 = tk.Label(root, text='Please check period from below values :')
label2.place(x=10, y=100)


# button
def button_click():
    view_plot()


button = tk.Button(root, text="View Plot")
button.config(command=button_click)
button.place(x=300, y=450)

checkboxes_size = []
checkvalues_size = []
checkboxes_period = []
checkvalues_period = []

i = 0
for item in availableDataSize:
    checkvalues_size.append(tk.IntVar())
    checkboxes_size.append(tk.Checkbutton(root, text=item, variable=checkvalues_size[i]))
    i += 1

i = 0
for item in availablePeriod:
    checkvalues_period.append(tk.IntVar())
    checkboxes_period.append(tk.Checkbutton(root, text=item, variable=checkvalues_period[i]))
    i += 1


def initialize_gui():
    for titem in checkvalues_period:
        titem.set(0)
    for titem in checkvalues_size:
        titem.set(0)
    for titem in checkboxes_period:
        titem.place_forget()
    for titem in checkboxes_size:
        titem.place_forget()
    if radio_var.get() == 'ConstSize':
        option_menu = tk.OptionMenu(root, selected_option, *availableDataSize)
        label1 = tk.Label(root, text='The data size is set as:                    ')
        label2 = tk.Label(root, text='Please check period from below values :   ')
        selected_option.set(availableDataSize[0])
        i = 100
        for titem in checkboxes_period:
            titem.place(x=20, y=(i + 30))
            i += 30
    else:
        option_menu = tk.OptionMenu(root, selected_option, *availablePeriod)
        label1 = tk.Label(root, text='The period is set as :')
        label2 = tk.Label(root, text='Please check data size from below values :   ')
        selected_option.set(availablePeriod[0])
        i = 100
        for titem in checkboxes_size:
            titem.place(x=20, y=(i + 30))
            i += 30

    label1.place(x=10, y=70)
    option_menu.place(x=200, y=70)
    label2.place(x=10, y=100)


initialize_gui()


def view_plot():
    rootPath = os.path.join(os.getcwd(),'datapack')
    platforms = ['u', 'udocker', 'ava', 'xen']
    platform_color = ['red', 'blue', 'green', 'yellow']
    datasize = []
    periods = []
    alldata = []
    colors = []
    labels = []
    bConstSize = True
    if radio_var.get() == 'ConstSize':
        bConstSize = True
        datasize.append(selected_option.get())
        i = 0
        for titem in checkvalues_period:
            if titem.get():
                periods.append(availablePeriod[i])
            i += 1
        if not len(periods):
            messagebox.showwarning(title="Invalid input", message="Please select at least one period.")
            return
    else:
        bConstSize = False
        periods.append(selected_option.get())
        i = 0
        for titem in checkvalues_size:
            if titem.get():
                datasize.append(availableDataSize[i])
            i += 1
        if not len(datasize):
            messagebox.showwarning(title="Invalid input", message="Please select at least one data size.")
            return

    paths = []
    for tPlatForm in platforms:
        for sizeItem in datasize:
            for periodItem in periods:
                paths.append(os.path.join(rootPath, tPlatForm, sizeItem + periodItem + ".txt"))
                colors.append(platform_color[platforms.index(tPlatForm)])
                if bConstSize:
                    labels.append(periodItem)
                else:
                    labels.append(sizeItem)

    for path in paths:
        with open(path, 'r') as f:
            lines = f.readlines()

        values = lines[0].split()
        values = list(map(float, values))
        values = [v * 1000 for v in values]
        alldata.append(values)

    # if bConstSize:
    plt.boxplot(alldata, labels=labels, patch_artist=True, showfliers=False)
    for box, color in zip(plt.boxplot(alldata, labels=labels, patch_artist=True)['boxes'], colors):
        box.set_facecolor(color)

    plt.xlabel('Period')
    plt.ylabel('Latency_(ms)')
    plt.title('Ubuntu-Ubuntu+docker-SOAFEE-XEN')
    # else:
    #     plt.boxplot(alldata, labels=labels, patch_artist=True, showfliers=False)
    #     plt.xlabel('Data_size')
    #     plt.ylabel('Latency_(ms)')
    #     plt.title('Ubuntu-Ubuntu+docker-SOAFEE-XEN')
    # 显示盒图
    plt.show()

# # Press the green button in the gutter to run the script.
if __name__ == '__main__':
    root.mainloop()

# # See PyCharm help at https://www.jetbrains.com/help/pycharm/
