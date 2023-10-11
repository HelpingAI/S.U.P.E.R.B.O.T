from time import sleep
import time
import sys
import pyfiglet
from os import system

# Ty to @SalladShooter for helping with the text styling!
BOLD = "\033[1m"
END = "\033[0m"

def write(text, speed=0.037):
  for char in text:
    sys.stdout.write(char)
    sys.stdout.flush()
    time.sleep(speed)


def writeFast(text, speed=0.0007):
  for char in text:
    sys.stdout.write(char)
    sys.stdout.flush()
    time.sleep(speed)
def open_main_file():
  os.system('python main.py')


class BruteForceAttacker:

  def __init__(self):
    self.first_char = ' '
    self.last_char = '~'
    self.password_length = 6
    self.tries = 0
    self.done = False
    self.password = "sussyBaka"

  def create_passwords(self, keys, choice):
    if keys == self.password:
      self.done = True
    if len(keys) == self.password_length or self.done:
      return
    for c in range(ord(self.first_char), ord(self.last_char) + 1):
      new_keys = keys + chr(c)
      if choice:
        print(new_keys)
      self.tries += 1
      self.create_passwords(new_keys, choice)


if __name__ == "__main__":
  attacker = BruteForceAttacker()
  write("(y/n) Would you like to skip the intro? (can be laggy): ")
  intro = input("")
  introFix = intro.lower()
  system('clear')
  if introFix == "y":
    pass

  else:
    PPC = "Python Password Cracker"
    ASCII = pyfiglet.figlet_format(PPC, font='rounded')
    writeFast(ASCII)
    print()
    sleep(1)
    write("Please note that nothing you type in is stored.")
    print()
    sleep(1)
    write("\nFeel free to check the code!")
    print()
    sleep(1)
    print()

  write(f"Please enter your {BOLD}password{END}: ")
  password_input = input("")

  with open("commonPasswords.txt", "r") as f:
    commonPasswords = [line.strip() for line in f.readlines()]
    if password_input in commonPasswords:
      position = commonPasswords.index(password_input) + 1
      attacker.password = password_input
      attacker.password_length = len(attacker.password)
      print("\nYour password has been found!")
      sleep(1.5)
      print(
          f"\nIt was in the top 1,000,000 most common passwords list at position: {position}"
      )
      sleep(1.5)
      print("\nIf this is your actual password, please consider changing it!")
      sleep(1.5)
      print("----------------------------------")
      print(f"Password: {BOLD}{attacker.password}{END}")
      print(f"Password length: {BOLD}{attacker.password_length}{END}")
      print(f"Tries: {BOLD}1{END}")
      print(f"Time to crack: {BOLD}0 Seconds{END}")

    else:
      choice_input = input(
          "\n(y or n) Would you like to watch the computer solve? (it takes much longer): "
      )
      show_attempts = choice_input.lower() == 'y'
      attacker.password = password_input
      print("\nCracking your password...")
      start_time = time.time()
      attacker.password_length = len(attacker.password)
      attacker.create_passwords("", show_attempts)
      elapsed_time = time.time() - start_time
      print("\nYour password has been found!")
      print("----------------------------------")
      print(f"Password: {BOLD}{attacker.password}{END}")
      print(f"Password length: {BOLD}{attacker.password_length}{END}")
      print(f"Tries: {BOLD}{attacker.tries}{END}")
      plural = "Seconds" if elapsed_time != 1 else "Second"
      print(f"Time to crack: {BOLD}{elapsed_time:.2f} {plural}{END}")
      print(f"Passwords per second: {BOLD}{int(attacker.tries / elapsed_time)}{END}")

