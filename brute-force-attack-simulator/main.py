# Simulation of brute force attacks
# Code to understand how inefficient and short passwords are vulnerable to brute force attacks
import random
import getpass

# Updated character set to include uppercase letters and symbols
chars = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789!@#$%^&*()-_=+[]{}|;:'\",.<>?/`~"

# Convert to list for random selection
allchar = list(chars)

# Prompt user to enter a password via terminal (masked input)
pwd = getpass.getpass("Enter a password (letters, numbers, and symbols only): ")

# Validate the input password
if not all(char in allchar for char in pwd):
    print("Invalid input! Please use only letters, numbers, and symbols.")
else:
    sample_pwd = ""

    while sample_pwd != pwd:
        # Generate random password of the same length
        sample_pwd = random.choices(allchar, k=len(pwd))

        # Print the randomly generated password attempt
        print("<==== " + "".join(sample_pwd) + " ====>")

        # Check if the generated password matches the input password
        if sample_pwd == list(pwd):
            print("The Password is: " + "".join(sample_pwd))
            break
