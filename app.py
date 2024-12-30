from flask import Flask, request, redirect, url_for, render_template
from datetime import datetime

app = Flask(__name__)

class Group:
    def __init__(self, FirstName, LastName, Contact, Category, Description, Date):
        self.FirstName = FirstName
        self.LastName = LastName
        self.Contact = Contact
        self.Category = Category
        self.Description = Description
        self.Date = Date

    def create_record_line(self):
        return self.FirstName + "#//#" + self.LastName + "#//#" + self.Contact + "#//#" + self.Category + "#//#" + self.Description + "#//#" + self.Date

    @staticmethod
    def get_record(line):
        line_split = line.split("#//#")
        return Group(
            FirstName=line_split[0],
            LastName=line_split[1],
            Contact = line_split[2],
            Category=line_split[3],
            Description=line_split[4],
            Date=line_split[5],
        )


@app.route('/')
def home():
    UpdateData()
    groups = []
    with open('Data/Data.txt', 'r') as file:
        for line in file:
            if line.strip():
                group = Group.get_record(line.strip())
                groups.append(group)
    return render_template('index.html', groups=groups)

@app.route('/AddGroup')
def AddGroup():
    return render_template('AddGroup.html')



@app.route('/Save', methods=['POST'])
def Save():
    FirstName = request.form['FirstName']
    LastName = request.form['LastName']
    Contact = request.form['Contact']
    Category = request.form['Category']
    Description = request.form['Description']
    current_date = datetime.now()
    Date = current_date.strftime("%d/%m/%Y")
    group = Group(FirstName=FirstName, LastName=LastName, Contact=Contact, Category=Category, Description=Description, Date=Date)

    with open('Data/Data.txt', 'a') as file:
        file.write(group.create_record_line()+"\n")
        return redirect(url_for('home', saved = "true"))    
    return redirect(url_for('home', saved = "false"))



def UpdateData():
    with open('Data/Data.txt', 'r') as file:
        Lines = []
        OutOfRange = 0
        current_date = datetime.now()
        Date = current_date.strftime("%d/%m/%Y")
        for line in file:
            if line.strip():
                group = Group.get_record(line.strip())
                if (DaysBetweenDates(group.Date, Date) <= 30) :
                    Lines.append(line.strip() + "\n")
                else :
                    OutOfRange = 1
    if  OutOfRange :
        with open('Data/Data.txt', 'w') as file:
            file.writelines(Lines)
    return OutOfRange




def DaysBetweenDates(date_str1, date_str2):

    date_format = "%d/%m/%Y"  
    date1 = datetime.strptime(date_str1, date_format)
    date2 = datetime.strptime(date_str2, date_format)
    
    D = date2 - date1
    
    return abs(D.days)


if __name__ == '__main__':
    app.run(debug=True)
    