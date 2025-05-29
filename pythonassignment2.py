#8 Movie Ticket Booking System
import json
import os

class Movie:
    def __init__(self, title, showtime):
        self.title = title
        self.showtime = showtime
        self.seats = [[f"{chr(65+row)}{col+1}" for col in range(5)] for row in range(5)]
        
    def display_seats(self):
        print("Seating for " + self.title + " at " + self.showtime + ":")
        print("[SCREEN]")
        for row in self.seats:
            print(" ".join(row))

    def book_seat(self, seat_input):
        for row in range(5):
            for col in range(5):
                if self.seats[row][col] == seat_input:
                        self.seats[row][col] = "X"
                        return True
        return False # seat not found/already booked -> make user try again

    # def valid_seat(self, seat_input):

    def to_dict(self):
         return {
              "title": self.title,
              "showtime": self.showtime,
              "seating": self.seats
         }
    
    @classmethod
    def from_dict(cls, data):
        movie = cls(data["title"], data["showtime"])
        movie.seats = data["seating"]
        return movie
    

class BookingSystem:
    def __init__(self, file='movies.json'):
          self.file = file
          self.movies = self.load_movies()

    def load_movies(self):
         if os.path.exists(self.file):
              with open(self.file, 'r') as f:
                   data = json.load(f)
                   return [Movie.from_dict(m) for m in data]
         else:
              return [
                   Movie("Interstellar", "7:00 PM"),
                   Movie("Zootopia", "2:00 PM"),
                   Movie("Interstellar", "3:00 PM")
              ]
    
    def save_movies(self):
         with open(self.file, 'w') as f:
              json.dump([m.to_dict() for m in self.movies], f, indent = 2)

    def show_movies(self):
         print("Available Movies: ")
         for i, movie in enumerate(self.movies):
              print(f"{i+1}. {movie.title} at {movie.showtime}")

    def book_ticket(self):
         self.show_movies()
         try:
            choice = int(input("Select a movie by number: "))
            movie = self.movies[choice-1]
         except (ValueError, IndexError):
              print("Invalid selection.")
              return
         
         movie.display_seats()
         seat_code = input("Enter seat code (ex. A3): ").upper()

         if movie.book_seat(seat_code):
              print("Ticket booked successfully!")
              print(f"Receipt: {movie.title} at {movie.showtime}, Seat: {seat_code}")
              self.save_movies()
         else: print("Seat is unavailable.")

    def run(self):
         while True:
              print("---MOVIE TICKET BOOKING---")
              print("1. View Movies")
              print("2. Book Ticket")
              print("3. Exit")
              
              choice = input("Choose an option: ")

              if choice == '1':
                   self.show_movies()
                   for movie in self.movies:
                        movie.display_seats()
              elif choice == '2':
                   self.book_ticket()
              elif choice == '3':
                   print("Thank you for visiting, Goodbye!")
                   break
              else:
                   print("Invalid option")

''' RUN # 8
if __name__ == "__main__":
    system = BookingSystem()
    system.run()
'''

# 3 Task Scheduler with Priorities

import heapq
from datetime import datetime

class Task:
     def __init__(self, task, deadline, done=False):
          self.task = task
          self.deadline = deadline
          self.done = done
          self.duedate = datetime.strptime(deadline, "%Y-%m-%d")
     # for heapq - python uses this comparator 
     def __lt__(self, other): 
          return self.duedate < other.duedate #earlier deadline=higher priority
     # for storing in archive - JSON format
     def to_dict(self):
          return {
               "task": self.task,
               "deadline": self.deadline,
               "done": self.done,
          }
     def from_dict(item):
          return Task(item['task'], item['deadline'], item['done'])

class TaskManager:
     def __init__(self, taskfile="tasks.json", archivefile="archive.json"):
          self.taskfile = taskfile
          self.archivefile = archivefile
          self.tasks = self.get_tasks()
     
     def get_tasks(self):
          if os.path.exists(self.taskfile):
               with open(self.taskfile, "r") as f:
                    data = json.load(f)
                    return [Task.from_dict(item) for item in data]
          return []
     
     def set_tasks(self):
          with open(self.taskfile, "w") as f:
               json.dump([task.to_dict() for task in self.tasks if not task.done], f)
     
     def set_archives(self, task):
          archive = []
          if os.path.exists(self.archivefile):
               with open(self.archivefile, "r") as f:
                    archive = json.load(f)
          archive.append(task.to_dict())
          with open(self.archivefile, "w") as f:
               json.dump(archive, f)
     
     def add_task(self):
          task = input("Enter task: ")
          deadline = input("Enter deadline (YYYY-MM-DD): ")
          self.tasks.append(Task(task, deadline))
          self.set_tasks()
     
     def view_tasks(self):
          heap = [t for t in self.tasks if not t.done]
          heapq.heapify(heap)
          print("Pending Tasks:")
          for t in heapq.nsmallest(len(heap), heap):
               print(f"{t.task} | Deadline: {t.deadline}")
     
     def mark_done(self, name):
          for task in self.tasks:
               if task.task == name and not task.done:
                    task.done = True
                    self.set_archives(task)
                    break
          self.tasks = [t for t in self.tasks if not t.done] #removes the task just completed
          self.set_tasks()
          print("Task complete and archived!")
     
     def run(self):
          manager = TaskManager()
          
          while True:
               print("-- TASKS --")
               manager.view_tasks()
               print("1. add task")
               print("2. mark task as done")
               print("3. exit")

               choice = input("Choose an option: ")

               if choice == '1':
                    manager.add_task()
               elif choice == '2':
                    done = input("Enter a task to mark as done: ")
                    manager.mark_done(done)
               elif choice == '3':
                    print("Goodbye!")
                    break
               else:
                    print("Invalid choice.")


''' runs #3 task scheduler
if __name__ == "__main__":
     system = TaskManager()
     system.run()
'''

# 11 - ATM Machine Simulation

class Account:
     def __init__(self, id, pin, balance = 0):
          self.id = id
          self.pin = pin
          self.balance = balance
     
     def allow_access(self, pin):
          if (pin == self.pin):
               return True
     
     def view_balance(self):
          print(f"Balance: {self.balance}")
     
     def withdraw(self, amount):
          if amount < self.balance:
               self.balance -= amount
          else:
               print("Insufficient funds.")
               self.view_balance()
    
     def deposit(self, amount):
          self.balance += amount
     
     def to_dict(self):
          return {
               "id": self.id,
               "pin": self.pin,
               "balance": self.balance
          }
     
     def from_dict(item):
          return Account(item["id"], item["pin"], item["balance"])
     
class AccountManager:
     def __init__(self, file="accounts.json"):
          self.accountsfile = file
          self.accounts = self.get_accounts()
     
     def get_accounts(self):
          if os.path.exists(self.accountsfile):
               with open(self.accountsfile, "r") as f:
                    try:
                         data = json.load(f)
                         return [Account.from_dict(item) for item in data]
                    except json.JSONDecodeError:
                         return[]
          return[]

     def set_accounts(self):
          with open(self.accountsfile, "w") as f:
               json.dump([account.to_dict() for account in self.accounts], f)
     
     def run(self):
          manager = AccountManager()

          while True:
               print("---ATM LOGIN---")
               print("1. Login to Existing Account")
               print("2. Make New Account")
               print("3. Exit")

               choice = input("Choose an option (number): ")

               if choice == '1':
                    id = input("Enter your user id: ")
                    matched = False
                    for account in manager.accounts:
                         if account.id == id:
                              matched = True
                              pin = input("Enter your pin: ")
                              if account.allow_access(pin):
                                   print("Login success!")
                                   print("1. View Balance")
                                   print("2. Withdrawal")
                                   print("3. Deposit")
                                   print("4. Exit")
                                   option = input("Enter your choice: ")
                                   if option == '1':
                                        account.view_balance()
                                   elif option == '2':
                                        amount = int(input("Enter withdrawal amount? $"))
                                        account.withdraw(amount)
                                   elif option == '3':
                                        amount = int(input("Enter deposit amount: $"))
                                        account.deposit(amount)
                                   elif option == '4':
                                        print("Goodbye!")
                                        exit()
                                   else:
                                        print("Invalid input.")
                                   manager.set_accounts()
                              else:
                                   print("Incorrect pin.")
                                   continue
                    if not matched:
                         print("Account doesn't exist")
               if choice == '2':
                    id = input("Create new user id: ")
                    for account in manager.accounts:
                         if account.id == id:
                              print("This user id is taken. Please try another.")
                              continue
                    pin = input("Create new pin: ")
                    manager.accounts.append(Account(id, pin))
                    manager.set_accounts()
                    print("Success! Login with your new account!")
               if choice == '3':
                    print("Goodbye!")
                    exit()
''' runs #11 
if __name__ == "__main__":
     system = AccountManager()
     system.run()
'''