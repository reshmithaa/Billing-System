# pip install cx-Oracle
# pip install docxtpl

import cx_Oracle
con=cx_Oracle.connect("system/1234")
if con:
    print("Successfully connected dbms")
else:
    print("Failed to connect dbms")
ch=int(input("Do u want to delete all tables(1/0) (1 recommended): "))
if (ch==1):
    Cur=con.cursor()
    try:
        Cur.execute("drop table unitea_countID")
    except:
        pass
    try:
        Cur.execute("drop table unitea_products")
    except:
        pass
    try:
        Cur.execute("drop table unitea_order")
    except:
        pass
    try:
        Cur.execute("drop table unitea_customer")
    except:
        pass
    try:
        Cur.execute("drop table productdet")
    except:
        pass

    print("Successfully deleted all table")

print("Downloading required tables...")
con.commit()
try:
    Cur = con.cursor()
    command = """create table productdet(
                    pid number(3),
                    constraint pid_pk primary key(pid),
                    constraint pid_ck check(to_char(pid) = initcap(to_char(pid))),
                    pname char(20),
                    constraint pname_ck check(pname = initcap(pname)),
                    unitprice float
                )"""
    Cur.execute(command)
except Exception as error:
    print('Error in Creating Table...',error)
else:
    print('Successfully Created the table')
    try:
        command='''insert into productdet values(01,'Black Tea',30)'''
        Cur.execute(command)
        command='''insert into productdet values(02,'Ginger Tea',10)'''
        Cur.execute(command)
    except:
        pass

try:
    Cur=con.cursor()
    command = '''create table unitea_customer(custNumber number(10) primary key,custName varchar(20),
                                    CONSTRAINT ck_name CHECK (custName=initcap(custName)))
    '''
    Cur.execute(command)
except:
    pass


try:
    Cur=con.cursor()
    command = '''create table unitea_order(custNumber number(10),orderID number(5) primary key,Date_ date,time_ varchar(20),total number(20,2),
                        CONSTRAINT fk_order_ foreign key(custNumber) REFERENCES unitea_customer)
    '''
    Cur.execute(command)
except:
    pass
try:
    Cur=con.cursor()
    command= '''create table unitea_products(orderID number(5),productID number(3),quantity number(5),price float,
                        CONSTRAINT pk_unitea_products primary key(orderID,productID),
                        CONSTRAINT fk_unitea_products foreign key(orderID) REFERENCES unitea_order,
                        CONSTRAINT fk_unitea_products1 foreign key(productID) REFERENCES productdet
                        )
    '''
    Cur.execute(command)
except:
    pass

try:
    Cur=con.cursor()
    command= '''create table unitea_countID(orderID number(5),productID number(3))
    '''
    Cur.execute(command)
    Cur.execute("insert into unitea_countID values(1,3)")

finally:
    con.commit()

