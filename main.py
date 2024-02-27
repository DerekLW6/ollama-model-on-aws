# Importing the required modules
import paramiko
import sys
import select  # Add this line to import the select module

# Saving SSH connection details
hostname = '54.196.15.142'
port = 22
username = 'ec2-user'
private_key_path = '/workspaces/ollama-model-on-aws/ollama-key.pem'

# Create SSH client
ssh_client = paramiko.SSHClient()

# Automatically add host keys
ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

try:
    # Connect to the SSH server using private key authentication
    ssh_client.connect(hostname, port, username, key_filename=private_key_path)
    print("SSH connection established successfully!")

    # Start an interactive shell session
    ssh_shell = ssh_client.invoke_shell()

    # Keep the shell session open
    while True:
        # Check if the shell session is active
        if ssh_shell.recv_ready():
            # Receive the output from the shell
            output = ssh_shell.recv(1024).decode()
            sys.stdout.write(output)
        
        # Check if the user has entered input
        if sys.stdin in select.select([sys.stdin], [], [], 0)[0]:
            # Read user input
            input_data = sys.stdin.readline()
            
            # Send user input to the shell
            ssh_shell.send(input_data)
        
finally:
    # Close the SSH connection
    ssh_client.close()
    print("SSH connection closed.")