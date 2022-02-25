# Generate random string of length n
def random_string(n):
   import random
   import string
   return ''.join(random.choice(string.ascii_letters) for i in range(n))


# Remove a file in a directory
def remove_file(file):
   import os
   try:
      os.remove(file)
   except FileNotFoundError:
      print("Error: File not found")