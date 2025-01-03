import subprocess

def run_command(command):
    """
    Runs a shell command and returns the output.

    Args:
        command (str): The command to execute.

    Returns:
        tuple: A tuple containing the standard output, standard error, and exit code.
    """
    try:
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        return result.stdout, result.stderr, result.returncode
    except Exception as e:
        return "", str(e), -1

if __name__ == "__main__":
    # Example usage
    user_command = input("Enter a command to run: ")
    stdout, stderr, exit_code = run_command(user_command)
    
    print(f"Output:\n{stdout}")
    if stderr:
        print(f"Error:\n{stderr}")
    print(f"Exit Code: {exit_code}")
