import sys
import os

class __color:
   PURPLE = '\033[95m'
   CYAN = '\033[96m'
   DARKCYAN = '\033[36m'
   BLUE = '\033[94m'
   GREEN = '\033[92m'
   YELLOW = '\033[93m'
   RED = '\033[91m'
   BOLD = '\033[1m'
   UNDERLINE = '\033[4m'
   END = '\033[0m'

class Printer:
   output_file = sys.stdout
   mode = "a"

""" Sets the output file for the following prints.
   If the file exists, deletes the content
"""
def set_output(file):
   my_path = f"results/{file}"
   if os.path.isfile(my_path):
      os.remove(my_path)
   Printer.output_file = my_path

""" Reset the output to stdout"""
def reset_output():
   Printer.output_file = sys.stdout

""" Prints a pretty title"""
def print_title(title):
   if Printer.output_file != sys.stdout:
      with open(Printer.output_file, Printer.mode) as my_file:
         div = "="*80
         my_file.write(f"{div}\n{title}\n{div}\n\n")
   else:
      print(f"\n{__color.UNDERLINE}{__color.BOLD}{title}{__color.END}\n")

""" Prints a pretty subtitle"""
def print_subtitle(subtitle):
   if Printer.output_file != sys.stdout:
      with open(Printer.output_file, Printer.mode) as my_file:
         my_file.write(f"{subtitle}\n\n")
   else: print(f"{subtitle}\n")

""" Prints the string without a tab"""
def printf(string):
   if Printer.output_file != sys.stdout:
      with open(Printer.output_file, Printer.mode) as my_file:
         my_file.write(f"{string}\n")
   else: 
      print(f"{string}")

""" Prints the string with a tab """
def printt(string):
   string = string.replace("\n", "\n\t")
   if Printer.output_file != sys.stdout:
      with open(Printer.output_file, Printer.mode) as my_file:
	      my_file.write(f"\t{string}\n")
   else:
      print(f"\t{string}")

""" Prints a blank line"""
def newline():
   if Printer.output_file != sys.stdout:
      with open(Printer.output_file, Printer.mode) as my_file:
         my_file.write("\n")
   else:
      print()

""" Prints a divider"""
def div(count=80):
   if Printer.output_file != sys.stdout:
      with open(Printer.output_file, Printer.mode) as my_file:
         my_file.write(f"\n{'='*count}\n\n")
   else:
      print(f"\n{'='*count}\n")

""" Receives a float and an amount of decimal digits.
    Returns the float formatted with that amount of digits.
	By default, uses 2 digits.
"""
def pretty_f(f, d=2): 
	float_format = f"%.{d}f"
	return float_format % f

""" Prints a series. Uses a tab if tab is True."""
def print_series(series, tab=True):
   if (tab): printt(series.to_string())
   else: printf(series.to_string())
