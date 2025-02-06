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
        if '|' in command:
            processes = []
            commands = command.split('|')

            for i, cmd in enumerate(commands):
                cmd = cmd.strip().split()
                if i == 0:
                    # First command: no stdin
                    p = sp.Popen(cmd, stdout=sp.PIPE)
                elif i == len(commands) - 1:
                    # Last command: redirect output to a file if specified
                    if '>' in cmd:
                        output_index = cmd.index('>')
                        output_file = cmd[output_index + 1]
                        cmd = cmd[:output_index]  # Remove '>' and file name from the command
                        with open(output_file, 'w') as f:
                            p = sp.Popen(cmd, stdin=processes[-1].stdout, stdout=f)
                    elif '<' in cmd:
                        input_index = cmd.index('<')
                        input_file = cmd[input_index + 1]
                        cmd = cmd[:input_index]
                        with(input_file, 'r') as f:
                            p = sp.Popen(cmd, stdin=processes[-1].stdout, stdout=f)
                    else:
                        p = sp.Popen(cmd, stdin=processes[-1].stdout, stdout=sp.PIPE)
                else:
                    p = sp.Popen(cmd, stdin=processes[-1].stdout, stdout=sp.PIPE)

                # Append the process to the list
                processes.append(p)

            # If the last command's output is not redirected to a file, collect it
            if '>' not in commands[-1] and '<' not in commands[-1]:
                final_output, _ = processes[-1].communicate()
                print(final_output.decode())  # Decode bytes to string if needed

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
            result = sp.run(command, shell=True, text=True)
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

