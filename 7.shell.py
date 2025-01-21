import os
import subprocess as sp

# Function os execution
def os_execution():
    while True:
        print("os function")

# Function subprocess execution
def subprocess_execution():
    while True:
        print("subprocess function")

# Main function
def main():
    print("Python Shell. Type 'exit' to quit")
    select = input("Choose execution mode [os/subprocess]: ").lower()
    while select not in ('os', 'subprocess'):
        print("Invalid mode. Please choose 'os' or 'subprocess'")
        select = input("Choose execution mode [os/subprocess]: ").lower()

    while True:
        command = input("$ ")
        if command.lower() in ('exit', quit):
            break
        if command:
            if select == 'os':
                os_execution()
            if select == 'subprocess':
                subprocess_execution()

if __name__ == "__main__":
    main()

