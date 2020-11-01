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

def print_title(title):
   print(f"\n{__color.UNDERLINE}{__color.BOLD}{title}{__color.END}\n")

def print_subtitle(subtitle):
   print(f"{subtitle}\n")

""" Prints the string with a tab """
def printt(string):
	print(f"\t{string}")

""" Receives a float and an amount of decimal digits.
    Returns the float formatted with that amount of digits.
	By default, uses 2 digits.
"""
def pretty_f(f, d=2): 
	float_format = f"%.{d}f"
	return float_format % f