# Food Planner - V0.9
# Zach Black / Guy Turner
# 6/30/2012

import os.path, cPickle, calendar
from Tkinter import *
from datetime import datetime as dt

# Global Variables
username = None
food_db = {}
password = None
meal_db = {}
day_plan = {}

class Application(object):
    """ A GUI application with three buttons. """
    
    def __init__(self, root):
      """ Initialize the widgets. """
      self.create_widgets()

    def create_widgets(self):
      # Create the username label
      self.userlbl = Label(root, text = "Username:")
      self.userlbl.place(x = 100, y = 7)

      # Create the password label
      self.passwordlbl = Label(root, text = "Password:")
      self.passwordlbl.place(x = 104, y = 27)

      # Create the username textbox
      self.usernametxt = Entry(root, width = 20)
      self.usernametxt.place(x = 165 , y = 7)

      # Create the password textbox
      self.passwordtxt = Entry(root, width = 20, show = "*")
      self.passwordtxt.place(x = 165, y = 29)

      # Create the Login Button
      self.loginbttn = Button(root, text = "Login",
                              width = 10, height = 1, command = self.login)
      self.loginbttn.place(x = 300, y = 29)

      # Create the Create New Button
      self.createnewbttn = Button(root, text = "Create New",
                                  width = 10, height = 1, command = self.create)
      self.createnewbttn.place(x = 300, y = 2)
      

      # Create the Food Database Button
      self.fooddatabttn = Button(root, text = "Food Database",
                                 width = 15, height = 3,
                                 command = lambda: Popup(root).food_db())
      self.fooddatabttn.place(x = 125, y = 70)

      # Create the Add Food Button
      self.addfoodbttn = Button(root, text = "Add Food",
                                width = 15, height = 3,
                                command = lambda: Popup(root).food_entry())
      self.addfoodbttn.place(x = 125, y = 130)

      # Create the Meal Database Button
      self.mealdatabttn = Button(root, text = "Meal Database",
                                width = 15, height = 3,
                                command = lambda: Popup(root).meal_text())
      self.mealdatabttn.place(x = 245, y = 70)

      # Create the Add Meal Button
      self.addmealbttn = Button(root, text = "Add Meal",
                                width = 15, height = 3,
                                command = lambda: Popup(root).meal_entry())
      self.addmealbttn.place(x = 245, y = 130)

      # Create the Calendar
      self.calandar = Calendar(root)
      self.calandar.place(x = 85, y = 200)

    def create(self):
      """ Creates a new account. """
      global food_db, password, meal_db, username
      
      username = self.usernametxt.get().capitalize()
      password = self.passwordtxt.get()

      if os.path.isfile(username + ".dat"):
          Popup(root).warning("That user already exists.")
      elif len(username) < 3: # Minimum username size.
          Popup(root).warning("Username must contain three or more characters.")
      else:
          # Reset values to prevent users from duplicating account info:
          food_db = {}
          meal_db = {}
          day_plan = {}
          
          save()

      # Automatically clear text fields:
      self.usernametxt.delete(0, END)
      self.passwordtxt.delete(0, END)

    def login(self):
      """ Attempts to load a user's previous values. """
      global username
      
      username = self.usernametxt.get().capitalize()
      input_password = self.passwordtxt.get() # What the user claims password is.

      if not os.path.isfile(username + ".dat"): # File doesn't exist?
          Popup(root).warning("No user with that name.")
      else:
          data_file = open(username + ".dat", "r")
          password = cPickle.load(data_file)
         
          if password == input_password:
              # Set variables:
              load()
          else:
              Popup(root).warning("Wrong password.")
              
          data_file.close()

      # Automatically clear text fields:
      self.usernametxt.delete(0, END)
      self.passwordtxt.delete(0, END)

class Food(object):
    """ A single component of a real-world meal. """

    def __init__(self, name, amount, calories):
        self.__name = name
        self.__amount = amount
        self.__calories = calories

    def __str__(self):
        return str(self.name) + " -- " + str(self.amount) + " " + \
              str(self.name) + ": " + str(self.calories) + " calories."

    def get_name(self):
        return self.__name

    def set_name(self, newName):
        self.__name = newName

    name = property(get_name, set_name)

    def get_amount(self):
        return self.__amount

    def set_amount(self, newAmount):
        self.__amount = newAmount

    amount = property(get_amount, set_amount)
    
    def get_calories(self):
        return int(self.__calories)

    def set_calories(self, newCalories):
        self.__calories = newCalories

    calories = property(get_calories, set_calories)

class Meal(object):
    """ A multi-food object representing real-world meals. """

    def __init__(self, name, food_ls, time = None):
       self.__name = name
       self.food_ls = food_ls
       self.calories = 0
       self.time = time
       self.totalcal()

    def __str__(self):
       info = ""
       info += str(self.name) + ": " + str(self.calories) + "\n"
       for food in self.food_ls:
           info += "\t" + food + "\n"
           
       return info

    def totalcal(self):
        """ Calculate the collective amount of calories from the food within. """
        total = 0
        for food in self.food_ls:
            total += food_db[food].get_calories()
        self.calories = total

    def get_name(self):
       return self.__name

    def set_name(self, newName):
        self.__name = newName

    name = property(get_name, set_name)

    def get_food_ls(self):
       return self.food_ls

    def get_time(self):
       return self.time

    def get_calories(self):
       return int(self.calories)

class Calendar(Frame):

    def __init__(self, master):
     Frame.__init__(self, master)
     self.grid(row = 5, column = 0, sticky = W)
     self.create_days()

    def create_days(self):
     """ Populates the calendar. """
     calendar.setfirstweekday(calendar.MONDAY)
     
     # Used to arrange the calendar based on system time:
     year = dt.now().year
     month = dt.now().month
     
     firstDay, numDays = calendar.monthrange(year, month)

     # Create days of the week label.
     DAY_NAMES = ("SUN", "MON", "TUES", "WED", "THUR", "FRI", "SAT")
     counter = 0
     for day in DAY_NAMES:
         self.label = Label(self, text = day)
         self.label.grid(row = 0, column = counter, sticky = S)
         counter += 1

     # Generates actual calendar buttons.
     day = 1
     row = 2
     col = firstDay + 1
     for i in range(1, 8): # 7 Days
         while day <= numDays:
             if col >= 7:
                 break
                
             # Gives each cal button a method for identifying its assigned day:
             def show(dl = str(day)):
                 """ Creates a new Calendar attribute and opens a popup. """
                 self.dl = dl # day label
                 Popup(root).cal_window(self, month)
                
             self.button = Button(self, text = str(day), width = 5, height = 2,
                                  command = show)
             self.button.grid(row = row, column = col, sticky = W)
             col += 1 # Start a new day.
             day += 1
         col = 0
         row += 1 # Start a new week.

class Popup(Toplevel):
    """ Generic template for a popup. """

    def __init__(self, master):
      Toplevel.__init__(self, master)
      

    def warning(self, message):
      self.grid()
      self.fail = Label(self, text = message)
      self.fail.grid(row = 0, column = 0, sticky = W)

    def cal_window(self, cal, month):
        """ A Calendar Button Window. """
        self.title(str(month) + " / " + cal.dl)
        self.geometry("400x300")
        
        # Text label for the Meal time.
        timeLbl = Label(self, text = "Time: ")
        timeLbl.place(x = 20, y = 10, anchor = CENTER)

        # Time entry box for the Meal time.
        self.timeEntry = Entry(self)
        self.timeEntry.place(x = 100, y = 10, anchor = CENTER)

        # Meal Label
        mealLbl = Label(self, text = "Meal Name: ")
        mealLbl.place(x = 38, y = 35, anchor = CENTER)

        # Meal Entry Box for Meal name.
        self.mealEntry = Entry(self)
        self.mealEntry.place(x = 135, y = 35, anchor = CENTER)

        # Total Calories Label
        self.totalCalories = Text(self, width = 4, height = 1)
        self.totalCalories.insert(END, "0")
        self.totalCalories.place(x = 85, y = 50)

        # Total Calories Label Labeler
        caloriesLabel = Label(self, text = "Total Calories:")
        caloriesLabel.place(x = 2, y = 50)
        
        # Update Day Button
        updateBtn = Button(self, text = "Update", command = lambda: self.update_day_plan(cal.dl))
        updateBtn.place(x = 210, y = 67, anchor = CENTER)
        
        # Separates the "Meal Plan" from the "Meal Entry" widgets.
        separator = Label(self,
                          text = "__________________________" + \
                          "____________________________")
        separator.place(x = 65, y = 85)

        # Add to Plan Button
        addBtn = Button(self, text = "Add to Plan", command = lambda: self.add_to_plan(cal.dl))
        addBtn.place(x = 162, y = 110)

        # The Meal Plan textbox.
        self.mealTxt = Meal_Plan(self)
        self.mealTxt.place(x = 30, y = 140)

        # Check the Day Planner for any pre-existing meals:
        try:
            for ind in day_plan[cal.dl]:
                self.mealTxt.mealTxt.insert(END, str(ind) + " :\n\t" + str(day_plan[cal.dl][ind]))
        except:
            pass

    def update_day_plan(self, day):
        """ Allows for organizing meals throughout the day through a dictionary. """
        global meal_db, day_plan

        # User-created integer representing time of day:
        index = self.timeEntry.get()

        # Today's meals:
        daily = {}

        try:
            meal = meal_db[self.mealEntry.get()]
        except:
            self.mealEntry.delete(0, END)
            self.mealEntry.insert(0, "Invalid Meal.")
        else:
            if not index.isdigit():
                popupWarning = Popup(self)
                popupWarning.warning("Dat ain't an integer, bitch! Enter an integer!!")

            else:
                # add the meal to the day plan dictionary
                daily[index] = meal
                day_plan[day] = daily

                # update the day calories
                calories = int(self.totalCalories.get(1.0))
                calories += meal.get_calories()
                self.totalCalories.delete(1.0, END)
                self.totalCalories.insert(END, str(calories))

                # clear the entry widgets
                self.mealEntry.delete(0, END)
                self.timeEntry.delete(0, END)

    def add_to_plan(self, day):
        # REMEMBER TO CHANGE MONTHRANGE
        self.mealTxt.mealTxt.delete(1.0, END)
        for ind in day_plan[day]:
            self.mealTxt.mealTxt.insert(END, str(ind) + " :\n\t" + str(day_plan[day][ind]))
        save()

    def food_db(self):
      """ A Food Database Viewer Window. """
      self.title("Food Database")
      self.geometry("250x310")
      self.grid()

      db = Food_Database(self, food_db)
      db.grid(row = 0, column = 0, sticky = W)

    def meal_text(self):
      """ A Meal Database Viewer Window. """
      self.title("Meal Database")
      self.geometry("400x310")
      self.grid()

      db = Meal_Database(self, meal_db)
      db.grid(row = 0, column = 0, sticky = W)

    def food_entry(self):
      """ A Food Entry Wizard Window. """
      self.title("Food Entry Wizard")
      self.geometry("300x115")
      self.grid()

      # Empty Lines for Appearance
      self.nulllbl = Label(self, text = "")
      self.nulllbl.grid(row = 0, column = 0, sticky = W)

      self.nulllbl2 = Label(self, text = "  ")
      self.nulllbl2.grid(row = 2, column = 2, sticky = W)

      # Name Label
      self.namelbl = Label(self, text = "Name: ")
      self.namelbl.grid(row = 1, column = 0, sticky = W)

      # Name Entry
      self.nametxt = Entry(self)
      self.nametxt.grid(row = 1, column = 1, sticky = W)

      # Amount Label
      self.amountlbl = Label(self, text = "Amount: ")
      self.amountlbl.grid(row = 2, column = 0, sticky = W)

      # Amount Entry
      self.amounttxt = Entry(self)
      self.amounttxt.grid(row = 2, column = 1, sticky = W)

      # Calories Label
      self.calorieslbl = Label(self, text = "Calories: ")
      self.calorieslbl.grid(row = 3, column = 0, sticky = W)

      # Calories Entry
      self.caloriestxt = Entry(self)
      self.caloriestxt.grid(row = 3, column = 1, sticky = W)

      # Add to Database Button
      self.submitbtn = Button(self, text = "Add to Database",
                              command = self.add_food)
      self.submitbtn.grid(row = 2, column = 3, sticky = W)
          
    def meal_entry(self):
      """ A Food Entry Wizard Window. """
      self.title("Meal Entry Wizard")
      self.geometry("330x345")
      self.grid()

      # Empty Lines for Appearance
      self.nulllbl = Label(self, text = "")
      self.nulllbl.grid(row = 0, column = 0, sticky = W)

      self.nulllbl2 = Label(self, text = "  ")
      self.nulllbl2.grid(row = 4, column = 2, sticky = W)

      self.nulllbl3 = Label(self, text = "")
      self.nulllbl3.grid(row = 2, column = 0, sticky = W)

      self.nulllbl4 = Label(self, text = "")
      self.nulllbl4.grid(row = 4, column = 0, sticky = W)

      # Name Label
      self.namelbl = Label(self, text = "Name of Meal: ")
      self.namelbl.grid(row = 1, column = 0, sticky = W)

      # Name Entry
      self.nametxt = Entry(self)
      self.nametxt.grid(row = 1, column = 1, sticky = W)

      # Food Database
      self.db = Food_Database(self, food_db, 25, 12)
      self.db.grid(row = 3, column = 0, columnspan = 2, sticky = W)

      # Total Calories Label
      self.calorieslbl = Label(self, text = "Total Calories: ")
      self.calorieslbl.grid(row = 8, column = 0, sticky = W)

      self.caloriesamtlbl = Label(self, text = "0")
      self.caloriesamtlbl.grid(row = 8, column = 1, sticky = W)

      # Add to Database Button
      self.submitbtn = Button(self, text = "Add to Database",
                              command = self.add_meal)
      self.submitbtn.grid(row = 4, column = 3, sticky = W)

      # Update Meal Button
      self.update_mealbtn = Button(self, text = "Update Meal",
                                   command = self.update_meal)
      self.update_mealbtn.grid(row = 3, column = 2, sticky = W, columnspan = 2)

    def update_meal(self):
       global meal_db

       name = self.nametxt.get()
       indexls = self.db.dbtxt.curselection() # All food items user clicked
       meal = Meal(name, [])

       for index in indexls:
           meal.food_ls.append(self.db.dbtxt.get(str(index)))

       meal.totalcal()
       self.caloriesamtlbl.configure(text = str(meal.calories))
       meal_db[meal.get_name()] = meal

       # Automatically unselects all food:
       self.db.dbtxt.select_clear(0, END)

    def add_meal(self):
       self.caloriesamtlbl.configure(text = "0")
       self.nametxt.delete(0, END)
       save()

    def add_food(self):
       global food_db
      
       food = Food(self.nametxt.get(), self.amounttxt.get(),
                  self.caloriestxt.get())
       food_db[str(food)] = food
       self.nametxt.delete(0, END)
       self.amounttxt.delete(0, END)
       self.caloriestxt.delete(0, END)
       save()

class Meal_Database(Frame):
    """A class for dem food databases"""

    def __init__(self, master, dictionary, w = 47, h = 18, sidebar = True):
       Frame.__init__(self, master)

       self.dictionary = dictionary
       self.w = w
       self.h = h
       self.sidebar = sidebar
       self.grid()

       scrollbar = Scrollbar(self)
       scrollbar.pack(side = RIGHT, fill = Y)

       if sidebar:
           scrollbar2 = Scrollbar(self)
           scrollbar2.pack(side = BOTTOM, fill = X)
           # creates a meal textbox with x and y scrollbar
           self.db = Text(self, width = w, height = h, wrap = NONE,
                yscrollcommand = scrollbar.set,
                xscrollcommand = scrollbar2.set)
           
           scrollbar2.config(orient = HORIZONTAL, command = self.db.xview)
       else:
           # creates a meal textbox with only a y scollbar
           self.db = Text(self, width = w, height = h, wrap = WORD,
                yscrollcommand = scrollbar.set)
           

       scrollbar.config(command = self.db.yview)

       message = ""
       for meal in meal_db:
           message += str(meal_db[meal]) + "\n"
          
       self.db.insert(0.0, message)

       self.db.pack(side = LEFT, fill = BOTH)
   

class Food_Database(Frame):
    """A class for dem meal databases"""

    def __init__(self, master, dictionary, w = 38, h = 18, sidebar = True):
       Frame.__init__(self, master)

       self.dictionary = dictionary
       self.w = w
       self.h = h
       self.sidebar = sidebar
       self.grid()

       scrollbar = Scrollbar(self)
       scrollbar.pack(side = RIGHT, fill = Y)

       if sidebar:
           scrollbar2 = Scrollbar(self)
           scrollbar2.pack(side = BOTTOM, fill = X)
           
           self.dbtxt = Listbox(self, width = self.w, height = self.h,
                                yscrollcommand = scrollbar.set,
                                xscrollcommand = scrollbar2.set,
                                selectmode = EXTENDED,
                                activestyle = "none")

           scrollbar2.config(orient = HORIZONTAL, command = self.dbtxt.xview)
       else:
           self.dbtxt = Listbox(self, width = self.w, height = self.h,
                                yscrollcommand = scrollbar.set,
                                selectmode = EXTENDED,
                                activestyle = "none")

       scrollbar.config(command = self.dbtxt.yview)
           
       item_ls = []
       for item in self.dictionary:
           item_ls.append(item)
       item_ls.sort()
       for key in item_ls:
            self.dbtxt.insert(END, self.dictionary[key])

       self.dbtxt.pack(side = LEFT, fill = BOTH)

class Meal_Plan(Frame):
    """ An entrybox for the Meal Plan. """

    def __init__(self, master, w = 40, h = 8):
       Frame.__init__(self, master)

       self.w = w
       self.h = h
       self.grid()

       scroll1 = Scrollbar(self)
       scroll1.pack(side = RIGHT, fill = Y)
       scroll2 = Scrollbar(self)
       scroll2.pack(side = BOTTOM, fill = X)
       self.mealTxt = Text(self, width = w, height = h,
                           yscrollcommand = scroll1.set,
                           xscrollcommand = scroll2.set, wrap = NONE)
       
       scroll1.config(orient = VERTICAL, command = self.mealTxt.yview)
       scroll2.config(orient = HORIZONTAL, command = self.mealTxt.xview)

       self.mealTxt.pack(side = LEFT, fill = BOTH)
    
def save():
    data_file = open(username.capitalize() + ".dat", "w")
    cPickle.dump(password, data_file)
    cPickle.dump(food_db, data_file)
    cPickle.dump(meal_db, data_file)
    cPickle.dump(day_plan, data_file)
    data_file.close()

def load():
    global password, food_db, meal_db
    data_file = open(username.capitalize() + ".dat", "r")
    password = cPickle.load(data_file)
    food_db = cPickle.load(data_file)
    meal_db = cPickle.load(data_file)
    day_plan = cPickle.load(data_file)
    data_file.close()

    print day_plan


#main
root = Tk()
root.title("Food Planner")
root.geometry("500x440")
app = Application(root)
root.mainloop()
