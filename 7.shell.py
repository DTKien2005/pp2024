import os
import subprocess as sp

# Function os execution
def os_execution(command):
    try:
        result = os.system(command)
        if result != 0:
            print(f"Command failed with exit code {result}")
    except Exception as e:
        print(f"Error: {e}")

# Function subprocess execution
def subprocess_execution(command):
    try:
        if '|' in command:
            process = []
            commands = command.split('|')
            print(commands)
        else:
            result = sp.run(command.split())  # This is normal case 1st
        #error in here and fix it
        # when run error so we need to separate 3 case
    except Exception as e:
        print(f"Error: {e}")

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
                os_execution(command)
            if select == 'subprocess':
                subprocess_execution(command)

if __name__ == "__main__":
    main()

