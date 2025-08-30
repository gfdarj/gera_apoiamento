from tkinter import *
from tkinter import messagebox

from openpyxl.styles.builtins import title


#import tkinter as tk

#janela = tk.Tk()
#janela.title("Minha Interface Gráfica")
#label = tk.Label(janela, text="Olá, Tkinter!")
#label.pack()
#botao = tk.Button(janela, text="Clique Aqui")
#botao.pack()
#janela.mainloop()

class Application(Frame):
    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.msg = Label(self, text="Hello World")
        self.msg.pack ()
        self.btn_edital = Button (self, text="Gerar Edital", command=self.mensagem("ok"))
        self.btn_edital.pack ()
        self.btn_conclusao = Button (self, text="Gerar Conclusão", command=self.mensagem("ok"))
        self.btn_conclusao.pack ()
        self.bye = Button (self, text="Bye", command=self.quit)
        self.bye.pack ()
        self.pack()


    def mensagem(self, msg):
        messagebox.showinfo("minha_mensagem", msg)



app = Application()
app.mensagem("teste")
app.master.title = "Teste TK"
app.master.geometry("600x600+300+300")







def abrir(): Message("abrir")

def salvar(): print ("salvar")

def ajuda() : print ("ajuda")

principal=Menu(app)
menu_gerar=Menu(principal)
menu_gerar.add_command(label="Conclusões",command=abrir)
menu_gerar.add_command(label="Edital",command=salvar)
principal.add_cascade(label="Gerar",menu=menu_gerar)
principal.add_command(label="Ajuda",command=ajuda)
app.master.configure(menu=principal)



# VARIAVEIS DO TK
soma = DoubleVar(app.master)
parcela = DoubleVar(app.master)

def aritmetica (e):
    soma.set(soma.get()+parcela.get())

lsoma = Label(textvar=soma)
eparcela = Entry(textvar=parcela)
eparcela.bind("<Return>", aritmetica)
lsoma.pack()
eparcela.pack()



v1 = IntVar(app.master)
v2 = StringVar(app.master)

def exibe():
    l.config (text="v1=%d,v2=%s"%(v1.get(),v2.get()))

c1 = Checkbutton (text="V1", var=v1, command=exibe)
c2 = Checkbutton (text="V2", var=v2, command=exibe,\
 onvalue="Sim", offvalue="Nao")
l = Label()
for w in (c1,c2,l):w.pack()
exibe()



cor = StringVar(app.master)
cor.set("black")
l = Label(background=cor.get())
l.pack(fill='both',expand=True)

def pinta(): l.configure(background=cor.get())

for txt,val in (("preto","black"),\
 ("vermelho","red"),\
 ("azul","blue"), ("verde","green")):
 Radiobutton(text=txt,value=val,variable=cor,\
 command=pinta).pack(anchor=W)




def insere(): e.insert(INSERT,"*")
def limpa(): e.delete(INSERT,END)
e=Entry(font="Arial 24")
i=Button(text="Insere*",command=insere)
l=Button(text="Limpa",command=limpa)
e.pack()
for w in (i,l): w.pack(side='left')





#c = Canvas()
#c.pack()
#o = c.create_oval(1,1,200,100,outline="blue",\
#width=5,fill="red")
#widget = Button(text="Tk Canvas")
#w = c.create_window(10,120,window=widget,anchor=W)
#l = c.create_line(100,0,120,30,50,60,100,120,\
#fill="black",width=2)
#r = c.create_rectangle(40,150,100,200,fill="white")
#img = PhotoImage(file="python.gif")
#i = c.create_image (150,150,image=img,anchor=NW)
#a = c.create_arc (150,90,250,190,start=30,extent=60,\
#outline="green",fill="orange")
#t = c.create_text(200,35,text="Texto\nTexto",
#font="Arial 22")





lb = Listbox()
lb.pack(side=LEFT,expand=True,fill="both")
sb = Scrollbar()
sb.pack(side=RIGHT,fill="y")
sb.configure(command=lb.yview)
lb.configure(yscrollcommand=sb.set)
for i in range(100):
 lb.insert(END,i)




# Função para exibir uma mensagem quando o botão for clicado
def exibir_mensagem():
  print("O botão foi clicado!")

# Adicionar um botão
botao = Button(app.master, text="Clique Aqui", command=exibir_mensagem)
botao.pack()






mainloop()