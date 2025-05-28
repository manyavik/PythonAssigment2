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

if __name__ == "__main__":
    system = BookingSystem()
    system.run()