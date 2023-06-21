import tkinter as tk
from tkinter import END, StringVar, ttk
import cx_Oracle

con=cx_Oracle.connect("system/1234")

class Page1(tk.Frame):
    def __init__(self,parent,controller):
        tk.Frame.__init__(self,parent,height=600,width=700)

        label1=tk.Label(self,text='Login Page',font="arial 25")
        label1.place(x=270,y=30)

        b1=tk.Button(self,text='Next',width=15,height=2,command=lambda:controller.show_frame(Page2))
        b1.place(x=500,y=500)

class Page2(tk.Frame):
    def __init__(self,parent,controller):
        tk.Frame.__init__(self,parent,height=600,width=700)

        label1 = tk.Label(self,text = 'Billing Page',font="arial 25")
        label1.place(x=270,y=30)

        NameLabel = tk.Label(self,text = 'Name',font='10')
        NameLabel.place(x=30,y=120)
        self.NameEntry = tk.Entry(self,font='10')
        self.NameEntry.place(x=160,y=120)

        PhoneLabel = tk.Label(self,text = 'Phone Number',font='10')
        PhoneLabel.place(x=360,y=120)
        self.PhoneEntry = tk.Entry(self,font='10')
        self.PhoneEntry.place(x=480,y=120)

        Quantity = tk.Label(self,text = 'Quantity',font='10')
        Quantity.place(x=30,y=200)
        self.QuantityEntry = tk.Entry(self,font='10')
        self.QuantityEntry.place(x=160,y=200)

        ProductName = tk.Label(self,text = 'Product Name',font='10')
        ProductName.place(x=30,y=160)
        self.ProdNameEntry = ttk.Combobox(self,font='10',width=18)
        self.ProdNameEntry.place(x=160,y=160)

        UnitPrice = tk.Label(self,text = 'Unit Price',font='10')
        UnitPrice.place(x=360,y=160)
        self.UnitPriceEntry = tk.Entry(self,font='10')
        self.UnitPriceEntry.place(x=480,y=160)
        self.UnitPriceEntry.config(state= "disabled")

        AddButton = ttk.Button(self,text='Add Item',command=self.Add_Item)
        AddButton.place(x=480,y=200)

        self.ProdNameEntry.bind('<KeyRelease>',self.Check)
        self.ProdNameEntry.bind('<<ComboboxSelected>>',self.setPrice)

        self.tree=ttk.Treeview(self,height=12)

        # temp variable to strore pid
        self.pid=0

        # Scrollbar fro tree view
        # self.verscrlbar = ttk.Scrollbar(self,orient ="vertical",command = self.tree.yview)
        # self.verscrlbar.place(x=653,y=300)
        # self.tree.configure(yscrollcommand = self.verscrlbar.set)

        self.tree['column'] = ('PID','Description','Quantity','Price')
        self.tree['show'] = 'headings'
        self.tree.column('PID',anchor='c',width=90)
        self.tree.column('Quantity',anchor = 'c',width = 110)
        self.tree.column('Description',anchor = 'c',width = 230)
        self.tree.column('Price',anchor = 'c',width = 160)
        
        self.tree.heading('PID',text = 'PID',anchor = 'c')
        self.tree.heading('Description',text = 'Product',anchor = 'c')
        self.tree.heading('Quantity',text = 'Quantity',anchor = 'c')
        self.tree.heading('Price',text = 'Price',anchor = 'c')

        self.tree.place(x=50,y=250)

        label2=ttk.Label(self,text='Total : ',font=10)
        label2.place(x=500,y=540) 

        generateBtn = ttk.Button(self,text='Download Invoice',command=self.downloadDocument)
        generateBtn.place(x=30,y=540)

        newInvoiceBtn = ttk.Button(self,text='New Invoice',command=lambda: controller.refresh(Page2))     
        newInvoiceBtn.place(x=280,y=540)  

        self.total='0.0'
        self.label3=ttk.Label(self,text=self.total,font=10)
        self.label3.place(x=590,y=540)

        self.dummylist=[]

        label4=ttk.Button(self,text='<--',command=lambda: controller.show_frame(Page1))
        label4.place(x=10,y=10)

        try:
            self.tree.bind("<ButtonRelease-1>",self.display)
            self.tree.bind("<Double 1>",self.delete)
        except:
            print("Enter ")

        UpdateRecLabel = ttk.Button(self,text='Update',command=self.updateRecord)
        UpdateRecLabel.place(x=360,y=200)

        # tree count
        self.Count=0

    def display(self,event):
        index=self.tree.focus()

        try:
            record = self.tree.item(index,'values')
            self.ProdNameEntry.delete(0,END)
            self.QuantityEntry.delete(0,END)

            self.ProdNameEntry.insert(0,record[1])
            self.QuantityEntry.insert(0,record[2])
            
            i=StringVar()
            i.set(str(float(record[3])/int(record[2])))
            self.UnitPriceEntry.config(textvariable=i)

        except:
            pass

    def updateRecord(self):
        try:
            index=self.tree.focus()
            record=self.tree.item(index,'values')
            self.total=str(float(self.total)-float(record[3]))
            t=int(self.QuantityEntry.get())*float(self.UnitPriceEntry.get())

            self.tree.item(index,text='',values=(record[0],self.ProdNameEntry.get(),self.QuantityEntry.get(),t))

            self.total=str(float(self.total)+t)
            self.label3.config(text=self.total)

        except Exception as error:
            print("error",error)

        self.ProdNameEntry.delete(0,END)
        self.QuantityEntry.delete(0,END)
        i=StringVar()
        i.set('')
        self.UnitPriceEntry.config(textvariable=i)

    def Check(self,event):
        strg=str(self.ProdNameEntry.get())
        Cur = con.cursor()
        try:
            command = "select pname from productdet where lower(pname) like '%"+strg+"%'"
            ProductNameList = Cur.execute(command)

            list=[]
            for i in ProductNameList:
                i=str(i[0]).strip()
                list.append(i)

            self.ProdNameEntry['values'] = list
            #self.tk.call('ttk::combobox::PopdownWindow', self)
            
        except Exception as error:
            print("issue",error)

    def setPrice(self,event):
        strg=str(self.ProdNameEntry.get())
        Cur = con.cursor()
        try:
            command = "select pid,unitprice from productdet where pname ='"+strg+"'"
            
            Cur.execute(command)
            ProductNameList = Cur.fetchone()

            svar=StringVar()
            svar.set(ProductNameList[1])
            self.pid=ProductNameList[0]
            self.UnitPriceEntry.config(textvariable=svar)

        except:
            pass

    def Add_Item(self):
        self.dummylist.clear()

        if (self.QuantityEntry.get()=='' or self.ProdNameEntry.get()==''):
            print("Enter something...")
        try:
            t=int(self.QuantityEntry.get())*float(self.UnitPriceEntry.get())
            self.dummylist.append(self.pid)
            self.dummylist.append(self.ProdNameEntry.get())
            self.dummylist.append(self.QuantityEntry.get())
            self.dummylist.append(t)
            self.tree.insert(parent= '',index = 'end',iid=self.Count,text = '',value = self.dummylist)
            self.Count+=1
            self.ProdNameEntry.delete(0,END)
            self.QuantityEntry.delete(0,END)

            i=StringVar()
            i.set('')
            self.UnitPriceEntry.config(textvariable=i)

            self.total=str(float(self.total)+float(t))
            self.label3.config(text=self.total)
        except:
            print("Enter something...")


    def delete(self,event):
        records=self.tree.selection()

        for i in records:
            self.total=str(float(self.total)-float(self.tree.item(i,'values')[3]))
            self.label3.config(text=self.total)
            self.tree.delete(i)

        i=StringVar()
        i.set('')
        self.UnitPriceEntry.config(textvariable=i)

    def downloadDocument(self):
        if self.PhoneEntry.get()=='':
            print("Enter Phone")
            return

        name=str(self.NameEntry.get())
        phone=int(self.PhoneEntry.get())
        Cur=con.cursor()
        try:
            
            command="insert into unitea_customer values("+str(phone)+","+"'"+name+"')"
            Cur.execute(command)
            con.commit()

        except Exception as error:
            print("Already a customer",error)

        v=self.tree.get_children()
        if (len(v)==0):
            print("No products selected")
            return
        Cur=con.cursor()
        Cur.execute("select orderID from unitea_countID")
        order=Cur.fetchone()
        order=order[0]

        Cur=con.cursor()
        Cur.execute("select sysdate from dual")
        dateTime=Cur.fetchone()
        dateTime=dateTime[0]

        dateTime=str(dateTime)
        dateTime=dateTime.split(' ')

        date=dateTime[0]
        time=dateTime[1]

        date="to_date('2022-10-25','yyyy-mm-dd')"

        Cur=con.cursor()
        command="insert into unitea_order(custNumber,orderID,Date_,time_,total) values("+str(phone)+","+str(order)+","+str(date)+",'"+str(time)+"',"+str(self.total)+")"
        Cur.execute(command)

        Cur=con.cursor()
        command="update unitea_countID set orderID="+str(order+1)+" where orderID="+str(order)
        Cur.execute(command)
        
        for index in self.tree.get_children():
            record=self.tree.item(index,'values')
            command="insert into unitea_products(orderID,productID,quantity,price) values("+str(order)+","+str(record[0])+","+str(record[2])+","+str(record[3])+")"
            Cur.execute(command)

        con.commit()
        controller.refresh(Page2)

class PageController(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        
        self.geometry(self.size())
        self.resizable(0,0)
        self.title("Unitea")
        #self.iconbitmap("icon.ico")

        self.window=tk.Frame(self)
        self.window.pack()

        self.window.rowconfigure(0,minsize=600)
        self.window.columnconfigure(0,minsize=700)

        self.frames={}

        self.show_frame(Page2)

    def show_frame(self,PAGE):
        if (PAGE not in self.frames):
            self.frames[PAGE]=PAGE(self.window,self)
            frame=self.frames[PAGE]
            frame.grid(row=0,column=0)
            frame.tkraise()
        else:
            frame=self.frames[PAGE]
            frame.tkraise()

    def size(self):
        x = self.winfo_screenwidth()
        y = self.winfo_screenheight()

        xx = int(x / 2 - 700 / 2)
        yy = int(y / 2 - 600 / 2)
        xx = str(xx)
        yy = str(yy - 10)
        m = "700x600+" + xx + "+" + yy
        return m

    def refresh(self,PAGE):
        self.frames.pop(PAGE)
        self.show_frame(PAGE)


controller=PageController()
controller.mainloop()