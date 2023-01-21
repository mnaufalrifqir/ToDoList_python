import tkinter as tk
from tkinter import ttk
from tkcalendar import Calendar
from tkinter.scrolledtext import ScrolledText
from time import strftime

todos= {}

def detailTodo(cb=None):
    win = tk.Toplevel()
    win.wm_title("Detail Kegiatan")
    selectedItem = treev.focus()
    selectedIndex = treev.item(selectedItem)['text']
    tanggal = str(cal.selection_get())
    selectedTodo = todos[tanggal][selectedIndex]
    judul = tk.StringVar(value=selectedTodo['judul'])
    tk.Label(win, text="Tanggal        :").grid(row=0, column=0)
    tk.Label(win, text="{} | {}".format(tanggal, selectedTodo['waktu'])).grid(row=0, column=1, sticky="W")
    tk.Label(win, text="Judul            :").grid(row=1, column=0)
    tk.Entry(win, state="disabled", textvariable=judul, width=16).grid(row=1, column=1, sticky ="W")
    tk.Label(win, text="Keterangan :").grid(row=2, column=0, sticky="N")
    keterangan = ScrolledText(win, width=12, height=5)
    keterangan.grid(row=2, column=1, columnspan=2, rowspan=5)
    keterangan.insert(tk.INSERT, selectedTodo['keterangan'])
    keterangan.configure(state='disabled')


def LoadTodos():
    global todos
    f = open('mytodo.dat','r')
    data = f.read()
    f.close()
    todos = eval(data)
    ListTodo()

def SaveTodos():
    f = open('mytodo.dat','w')
    f.write(str(todos))
    f.close()

def delTodo():
    tanggal = str(cal.selection_get())
    selectedItem = treev.focus()
    todos[tanggal].pop(treev.item(selectedItem)['text'])
    ListTodo()

def ListTodo(cb=None):
    for i in treev.get_children():
        treev.delete(i)
    tanggal = str(cal.selection_get())
    if tanggal in todos:
        for i in range(len(todos[tanggal])):
            treev.insert("","end", text=i, values=(todos[tanggal][i]['waktu'], todos[tanggal][i]['judul']))

def addTodo(win, key, jam, menit, judul, keterangan):
    newTodo = {
        'waktu':'{}:{}'.format(jam.get(), menit.get()),
        'judul': judul.get(),
        'keterangan': keterangan.get('1.0', tk.END)
    }
    if key in todos:
        todos[key].append(newTodo)
    else:
        todos[key] = [newTodo]
    win.destroy()
    ListTodo()

def AddForm():
    win = tk.Toplevel()
    win.wm_title("Tambah Kegiatan")
    jam = tk.IntVar(value=10)
    menit = tk.IntVar(value=30)
    judul = tk.StringVar(value="")
    tk.Label(win, text="Waktu         :").grid(row=0, column=0)
    tk.Spinbox(win, from_=0, to=23, textvariable = jam, width=3).grid(row=0, column=1, sticky="W")
    tk.Spinbox(win, from_=0, to=59, textvariable = menit, width=3).grid(row=0, column=1, sticky="N")
    tk.Label(win, text="Judul           :").grid(row=1, column=0)
    tk.Entry(win, textvariable=judul, width=16).grid(row=1, column=1, sticky ="W")
    tk.Label(win, text="Keterangan : ").grid(row=2, column=0)
    keterangan = ScrolledText(win, width=12, height=5)
    keterangan.grid(row=2, column=1, columnspan=2, rowspan=5)
    tanggal = str(cal.selection_get())
    tk.Button(win, text="Tambah", command=lambda: addTodo(win, tanggal, jam, menit, judul, keterangan)).grid(row=4, column=0)

def title():
    waktu = strftime('%H:%M')
    tanggal = str(cal.selection_get())
    root.title("| Kalender | " + tanggal + " | " + waktu + " | ")
    root.after(1000, title)
    
root = tk.Tk()
s = ttk.Style()
s.configure('Treeview', rowheight=17)
root.title("Kalender")

cal = Calendar(root, font="Lucida 14 bold", background="dark green", foreground="snow", bordercolor="dark sea green", headersbackground="dark sea green", headersforeground="snow", normalforeground="black", weekendforeground="red", selectbackground="dark green", showweeknumbers = False, selectmode="day", locale="id_ID", cursor='hand1')
cal.grid(row=0, column=0, sticky='S', rowspan=7)
cal.bind("<<CalendarSelected>>", ListTodo)
tanggal = str(cal.selection_get())
treev = ttk.Treeview(root)
treev.grid(row=0, column=1, sticky="WNE", rowspan=4, columnspan=5)
scrollBar = tk.Scrollbar(root, orient='vertical', command=treev.yview)
scrollBar.grid(row=0, column=6, sticky="ENS", rowspan=4)
treev.configure(yscrollcommand=scrollBar.set)
treev.bind("<Double-1>", detailTodo)
treev['columns'] = ("1","2")
treev['show'] = 'headings'
treev.column("1", width=1)
treev.heading("1", text="Jam")
treev.heading("2", text="Judul")

btnAdd = tk.Button(root, text="Tambah", width=18, background="green", foreground="snow", command=AddForm)
btnAdd.grid(row=6, column=1, sticky='WS')

btnDel = tk.Button(root, text="Hapus", width=18, background="dark green", foreground="snow", command=delTodo)
btnDel.grid(row=6, column=2, sticky='WS')

btnLoad = tk.Button(root, text="Load", width=18, background="green", foreground="snow", command=LoadTodos)
btnLoad.grid(row=6, column=4, sticky='WS')

btnSave = tk.Button(root, text="Save", width=18, background="dark green", foreground="snow", command=SaveTodos)
btnSave.grid(row=6, column=3, sticky="WS")
title()
root.mainloop()
