from tkinter import *
from tkinter import ttk

clicked = 0

def makeStyle():
    style = ttk.Style()
    style.theme_use('clam')
    
    # Frame styl
    style.configure('TFrame', background='#333333')
    
    # Label styl
    style.configure('TLabel', background='#333333', foreground='white', font=('Arial', 12))
    
    # Button styl
    style.configure('TButton', foreground='white', font=('Arial', 12), padding=10)
    style.map('TButton',
              background=[('!active', '#555555'),  # normální stav
                          ('active', '#777777'),  # při najetí myší
                          ('pressed', '#999999')], # při stisku
              foreground=[('pressed', 'yellow'), ('active', 'white')])
    
    return style

def tlacitko_pushed():
    global clicked
    clicked += 1
    print(clicked)
    counter.config(text=f"Numbers clicked: {clicked}")

def main():
    global counter
    style = makeStyle()
    
    root = Tk()
    root.title("Protocol UI Test")
    root.geometry("600x400")
    
    frm = ttk.Frame(root, padding=10)
    frm.grid()
    
    ttk.Label(frm, text="Hello, Protocol UI!").grid(column=0, row=0)
    
    ttk.Button(frm, text="Quit", command=root.destroy, style="TButton").grid(column=1, row=0)
    ttk.Button(frm, text="Click lol", command=tlacitko_pushed, style="TButton").grid(column=0, row=1)
    
    counter = ttk.Label(frm, text=f"Numbers clicked: {clicked}", style="TLabel")
    counter.grid(column=0, row=2)
    
    root.mainloop()


if __name__ == "__main__":
    main()
