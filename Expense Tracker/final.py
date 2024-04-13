# libraries which are used in this code.
import psycopg2
import numpy as np
import matplotlib.pyplot as plt

# To establish connection with pgAdmin.
con=psycopg2.connect(host="localhost", port="5432",database="ExpenseTracker",user="postgres",password="admin")

# User class : contains various method for checking.
class User:
    flag=False
    idPass={'Perin':'Admin@1234'}


    # checkId: check id and password entered by user.
    def checkId(self):
        idCount=3
        passCount=3
        while idCount!=0:
            id=input("Enter the id(Only 3 attempt allowed) : ")
            if id not in self.idPass:
                idCount-=1

                if idCount==0:
                        print("You entered incorrect id 3 times please try again after some time.")

                else:
                    print(f'Wrong id {idCount} attempt left.')

            else:
                break
                    
        if id in self.idPass:

            while passCount!=0:
                password=input("Enter the password(Only 3 attempt allowed) : ")
                pas=self.idPass.get(id)

                if pas==password:
                    self.flag=True
                    break

                else:
                    passCount-=1

                    if passCount==0:
                        print("You entered incorrect password 3 times please try again after some time.")

                    else:
                        print(f'Wrong password {passCount} attempt left.')
    

    # makeId : makes id and password.
    def makeId(self):
        while True:
            id=input('Enter the id : ')
            if id not in self.idPass:
                break
            else:
                print("------------ User already exists ------------")

        if id not in self.idPass:
            password=input("Enter password : ")
            self.idPass[id]=password
            print('Id and password created sucessfully.')
        self.checkId()


    # checkAmount : checks whether entered amount is in valid datatype.
    def checkAmount(self):
        while True:
            try:
                checkA=float(input("Enter the amount of Expense : "))
                if checkA <= 0:
                    print("------------ Amount must be greater than zero ------------")
                    raise ValueError
                break
            
            except ValueError:
                print("------------ Please enter valid data only ------------")
        return checkA
    

    # checkAmount : checks whether entered value is in valid datatype.
    def checkValue(self):
        while True:
            try:
                checkO=int(input("Enter your choice : "))
                break
            
            except ValueError:
                print("------------ Please enter valid data only ------------")
        return checkO


# class ExpenseTracker : contains methods for track Expense. 
class ExpenseTracker(User): 

    def __init__(self):
        self.expense={}
        self.typeOfExpense=""
        self.amount=0
        self.note=""
        self.temp=""
        self.toFlag=True
        self.dateForJump=""


    # addExpense : store expense to database.
    def addExpense(self):
        print("Enter the Catergory of Expense : ")
        print('1 for Fuel\n2 for Clothes\n3 for Eating Out\n4 for Entertainment\n5 for General\n6 for Gifts\n7 for Holidays\n8 for Shopping\n9 for Sports\n10 for Travel\n11 for other')
        print("-------------------------------------------------")

        while True:
            choice=self.checkValue()

            match choice:
                case 1:
                    self.typeOfExpense="Fuel"
                    break

                case 2:
                    self.typeOfExpense="Clothes"
                    break

                case 3:
                    self.typeOfExpense="Eating Out"
                    break

                case 4:
                    self.typeOfExpense="Entertainment"
                    break

                case 5:
                    self.typeOfExpense="General"
                    break

                case 6:
                    self.typeOfExpense="Gifts"
                    break

                case 7:
                    self.typeOfExpense="Holidays"
                    break

                case 8:
                    self.typeOfExpense="Shopping"
                    break

                case 9:
                    self.typeOfExpense="Sports"
                    break

                case 10:
                    self.typeOfExpense="Travel"
                    break

                case 11:
                    self.typeOfExpense=input("Enter the type of Expense : ")
                    break

                case _:
                    print("------------ Invaild choice ------------")
            

        if self.typeOfExpense not in self.expense:
            self.amount=self.checkAmount()
            self.note=input("Enter any note : ")
            self.expense[self.typeOfExpense]={'amount':self.amount,'notes':self.note}
        
        else:
            self.toFlag=False
            print("------------------- Expense already in data you have to edit it -------------------")


    # removeExpense : remove expense from database.
    def removeExpense(self):
        toBeRemoved=input("Enter the Expense you want to remove : ")
        if toBeRemoved in self.expense:
            self.expense.pop(toBeRemoved)
            cur=con.cursor()
            cur.execute('delete from march where catergory=%s and date=%s',(toBeRemoved,self.dateForJump))
            con.commit()
            cur.close()
            print(f'------------------- {toBeRemoved} Expense removed sucessfully -------------------')

        else:
            print("------------ Expense not found ------------")


    # editExpense : edit expense from database.
    def editExpense(self):
        toBeEdit=input("Enter the Expense you want to edit : ")

        if toBeEdit in self.expense:
            self.typeOfExpense=toBeEdit
            print("---------------------------------------------------")
            print('Enter 1 for add amount to Expense\nEnter 2 for remove amount from Expense')
            print("---------------------------------------------------")
            op=self.checkValue()

            match op:
            
                case 1:
                    amountToAdd=self.checkAmount()
                    noteToAdd=input("Enter any note : ")
                    self.expense[toBeEdit]['amount']+=amountToAdd
                    self.amount=self.expense[toBeEdit]['amount']
                    t=' '+noteToAdd
                    self.expense[toBeEdit]['notes']+=str(t)
                    self.temp=self.expense[toBeEdit]['notes']
                    print(f"------------------- {toBeEdit} Expense modified sucessfully -------------------")

                
                case 2:
                    while True:
                        amountToSubtract=self.checkAmount()
                        if(self.expense[toBeEdit]['amount']>=amountToSubtract):
                            noteToAdd=input("Enter any note : ")
                            self.expense[toBeEdit]['amount']-=amountToSubtract
                            self.amount=self.expense[toBeEdit]['amount']
                            t=' '+noteToAdd
                            self.expense[toBeEdit]['notes']+=t
                            self.temp=self.expense[toBeEdit]['notes']
                            print(f"------------------- {toBeEdit} Expense modified sucessfully -------------------")
                            break
                        else:
                            print("------------ Please enter amonut less then stored amount ------------")
                        

                case _:
                    print("-------- Invaild choice please try again --------")
                    
        else:
            print("------------ Expense not found ------------")


    # viewExpense : view all expenses of particular date.
    def viewExpense(self):
        if len(self.expense)!=0:
            for i,j in self.expense.items():
                print("---------------------------------------------------")
                print(f'Expense type : {i}')
                print(f'Expense amount : {j['amount']}')
                print(f'Expense note : {j['notes']}')
        
        else:
            print("------------- No any data to view --------------")


    # validateDate : checks that date is in valid format or not.
    def validateDate(self,date):

        day=[31,28,31,30,31,30,31,31,30,31,30,31]
        month=[1,2,3,4,5,6,7,8,9,10,11,12]

        if len(date)==10:

            if date[2]=="-" and date[5]=="-":

                if int(date[3:5])<13:

                    dayTemp=int(date[0:2])
                    if dayTemp>0 and dayTemp<32:

                        monthTemp=int(date[3:5])
                        monthIndex=month.index(monthTemp)
                        if dayTemp<=day[monthIndex]:
                            return True
                        
                        else:
                            print("---------------------------------------------------")
                            print('Please enter valid date according to the month')
                            return False
                        
                    else:
                        print("---------------------------------------------------")
                        print("Please enter date between 1 to 31")
                        return False
                    
                else:
                   print("---------------------------------------------------")
                   print("Please enter vaild month")   
                   return False 
                
            else:
                print("---------------------------------------------------")
                print("please use valid format")
                return False
            
        else:
            print("---------------------------------------------------")
            print("Please enter valid date")
            return False
        

    # calculateExpense : calculate all expenses.
    def calculateExpense(self):
        totalExpense=sum(i['amount'] for i in self.expense.values())
        print(f'Total amount of expense of date {self.dateForJump} is : {totalExpense}')
        print("---------------------------------------------------")
        cur=con.cursor()
        cur.execute('select sum(amount) from march')
        result=cur.fetchone()
        print(f'Total amount of expense of all dates is : {float(result[0])}')


    # jumpToOtherDate : jump to record other date expenses.
    def jumpToOtherDate(self):
        valueFor=False
        while valueFor!=True:
            print("---------------------------------------------------")
            self.dateForJump=input("Enter the date(DD-MM-YYYY) : ")
            valueFor=et.validateDate(self.dateForJump)

        cur=con.cursor()
        cur.execute('select * from march where date=%s',(self.dateForJump,))
        result=cur.fetchall()
        self.expense={}

        if len(result)==0:
            self.expense={}

        else:
            for i,j,k,l in result:
                self.expense[j]={'amount':float(k),'notes':str(l)}
        cur.close()


    # specificDay : visualisation of spectific day expense via graphs with the help of matplotlib.
    def specificDay(self):
        font1={'family':'serif','color':'black','size':25}
        font2={'family':'serif','color':'blue','size':20}
        flag=False
        while flag!=True:

            date=input("Enter the date(DD-MM-YYYY) : ")
            flag=self.validateDate(date)

        cur=con.cursor()
        cur.execute('select catergory,amount from march where date=%s',(date,))
        result=cur.fetchall()
        x=np.array([])
        y=np.array([])

        if len(result)!=0:
            for i,j in result:
                x=np.append(x,i)
                y=np.append(y,float(j))

            plt.subplot(1,2,1)
            plt.xlabel("Catergory",fontdict=font2)
            plt.ylabel("Amount",fontdict=font2)
            plt.bar(x,y)

            plt.subplot(1,2,2)
            plt.pie(y,labels=x,autopct='%1.1f%%')
            plt.legend(title="Catergories : ")
            plt.suptitle("Catergorywise Expense",fontsize=25,color="black",family="serif")
            plt.show()

        else:
            print("------------------ No data to create charts ------------------")


    # comparisonBetweenDays : comaparison of expenses of dates via graphs with the help of matplotlib.
    def comparisonBetweenDays(self):
        font1={'family':'serif','color':'black','size':25}
        font2={'family':'serif','color':'blue','size':20}
        days=int(input("How many days chart you want : "))
        dates=[]
        for i in range(days):

            flag=False
            while flag!=True:
                date=input("Enter the date(DD-MM-YYYY) : ")
                flag=self.validateDate(date)
            dates.append(date)

        dates=tuple(dates)
        cur=con.cursor()
        cur.execute('select date,sum(amount) as total from march where date(date) in %s group by date(date) order by date asc',(dates,))
        result=cur.fetchall()
        x=np.array([])
        y=np.array([])

        for i,j in result:
            x=np.append(x,str(i))
            y=np.append(y,float(j))

        plt.subplot(1,2,1)
        plt.xlabel("Dates",fontdict=font2)
        plt.ylabel("Total Expense",fontdict=font2)
        plt.bar(x,y)

        plt.subplot(1,2,2)
        plt.xlabel("Dates",fontdict=font2)
        plt.ylabel("Total Expense",fontdict=font2)
        plt.suptitle("Changes in Total Expense",fontsize=25,color="black",family="serif")
        plt.plot(x,y)
        plt.show()


    # comparisonOfTimePeriod : comaparison of expenses between dates via graphs with the help of matplotlib.
    def comparisonOfTimePeriod(self):
        font1={'family':'serif','color':'black','size':25}
        font2={'family':'serif','color':'blue','size':20}
        startFlag=False
        endFlag=False
        
        while startFlag!=True or endFlag!=True:
            print("---------------------------------------------------")
            startDate=input("Enter start date : ")
            endDate=input("Enter end date : ")
            startFlag=self.validateDate(startDate)
            endFlag=self.validateDate(endDate)

        cur=con.cursor()
        cur.execute('select date,sum(amount) as total from march where date(date) between %s and %s group by date(date) order by date asc',(startDate,endDate))
        result=cur.fetchall()
        x=np.array([])
        y=np.array([])

        for i,j in result:
            x=np.append(x,str(i))
            y=np.append(y,float(j))

        plt.subplot(1,2,1)
        plt.xlabel("Dates",fontdict=font2)
        plt.ylabel("Total Expense",fontdict=font2)
        plt.bar(x,y)

        plt.subplot(1,2,2)
        plt.xlabel("Dates",fontdict=font2)
        plt.ylabel("Total Expense",fontdict=font2)
        plt.suptitle("Changes in Total Expense",fontsize=25,color="black",family="serif")
        plt.plot(x,y)
        plt.show()


    # exploreViaCharts : combines all matplotlib methods.
    def exploreViaCharts(self):
        while True:
            print("---------------------------------------------------")
            print("Enter 1 for view specific day expense chart")
            print("Enter 2 for view comparison chart of days")
            print("Enter 3 for view comparison between particular time period")
            print("Enter 4 for exit")
            print("---------------------------------------------------")
            option=self.checkValue()

            if option==4:
                break

            match option:

                case 1:
                    self.specificDay()

                case 2:
                    self.comparisonBetweenDays()

                case 3:
                    self.comparisonOfTimePeriod()

                case _:
                    print("------------ Invaild choice ------------")


# To access methods of user class.   
owner=User()

while True:
    print("------------ Enter 1 for login -------------")
    print("---------- Enter 2 for make new id ---------")
    print("----------- Enter 3 for exit ---------------")
    option=owner.checkValue()

    match option:
        case 1:
            owner.checkId()
            break

        case 2:
            owner.makeId()
            break

        case 3:
            exit()

        case _:
            print("-------- Invaild choice please try again --------")
            print("---------------------------------------------------")

if owner.flag:
    print("---------------------------------------------------")
    print('------------ Welcome to expance tacker ------------')

    # to access methods of expenseTracker class.
    et=ExpenseTracker()
    value=False
    date=""

    while value!=True:
        print("---------------------------------------------------")
        date=input("Enter the date(DD-MM-YYYY) : ")
        value=et.validateDate(date)

    et.dateForJump=date
    cur=con.cursor()
    cur.execute('select * from march where date=%s',(date,))
    result=cur.fetchall()

    for i,j,k,l in result:
        et.expense[j]={'amount':float(k),'notes':str(l)}
    cur.close()

    while True:
        print("---------------------------------------------------")
        print("Enter 1 for add Expense")
        print("Enter 2 for remove Expense")
        print("Enter 3 for edit Expense")
        print("Enter 4 for view Expense")
        print("Enter 5 for view total amount of expense")
        print("Enter 6 for jump to other date")
        print("Enter 7 for track your expense via creative charts!!!")
        print("Enter 8 for exit")
        print("---------------------------------------------------")

        option=owner.checkValue()

        if option==8:
            con.close()
            break

        match option:

            case 1:
                et.addExpense()
                if et.toFlag:
                    cur=con.cursor()
                    cur.execute('insert into march(date,catergory,amount,note) values(%s,%s,%s,%s)',(date,et.typeOfExpense,et.amount,et.note))
                    result=con.commit()
                    print(f'------------------- {et.typeOfExpense} sucessfully added -------------------')
                    cur.close()

            case 2:
                et.removeExpense()

            case 3:
                et.editExpense()
                cur=con.cursor()
                cur.execute('update march set amount=%s,note=%s where catergory=%s and date=%s',(et.amount,et.temp,et.typeOfExpense,date))
                result=con.commit()
                cur.close()
                
            case 4:
                et.viewExpense()

            case 5:
                et.calculateExpense()

            case 6:
                et.jumpToOtherDate()
                date=et.dateForJump

            case 7:
                et.exploreViaCharts()
                
            case _:
                print("------------ Invaild choice ------------")