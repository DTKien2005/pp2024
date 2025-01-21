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
        # Handle redirection and pipes
        if '|' in command: # In this case still error when run 3 tasks must fix
            processes = []
            commands = command.split('|')
            for i, cmd in enumerate(commands):
                cmd = cmd.strip().split()
                if i == 0:
                    p = sp.Popen(cmd, stdout=sp.PIPE)
                else:
                    p = sp.Popen(cmd, stdin=processes[-1].stdout, stdout=sp.PIPE)
                processes.append(p)

            outputs, errors = processes[-1].communicate()
            if outputs:
                print(outputs.decode())
            if errors:
                print(errors.decode())

        # Make a file
        elif '>' in command:
            commands = command.split('>')
            cmd = commands[0].strip().split()
            outfile = commands[1].strip()
            with open(outfile, 'w') as f:
                sp.run(cmd, stdout=f)

        # Input file
        elif '<' in command:
            commands = command.split('<')
            cmd = commands[0].strip().split()
            infile = commands[1].strip()
            with open(infile, 'r') as f:
                sp.run(cmd, stdin=f)
        else:
            # Simple command execution
            args = command.split()
            result = sp.run(args, capture_output=True, text=True)
            if result.stdout:
                print(result.stdout)
            if result.stderr:
                print(result.stderr)
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

