import sys
import os
import Variable
import State

def main():
    print "bruk deoply som argument"



if __name__ == '__main__':
    try:
        if sys.argv[1] == 'deploy':
            import paramiko

            # Connect to remote host
            client = paramiko.SSHClient()
            client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            client.connect('caracal.stud.ntnu.no', username='olehda', password='Shamuix22')

            # Setup sftp connection and transmit this script
            sftp = client.open_sftp()
            sftp.put('readfile.py', 'readfile.py')
            sftp.put('gui.py', 'gui.py')
            sftp.put('State.py', 'State.py')
            sftp.put('Variable.py', 'Variable.py')
            sftp.put('nono-cat.txt', 'nono-cat.txt')

            sftp.close()

            # Run the transmitted script remotely without args and show its output.
            # SSHClient.exec_command() returns the tuple (stdin,stdout,stderr)
            stdout = client.exec_command('python readfile.py')[1]
            for line in stdout:
                # Process each line in the remote output
                print line

            client.close()
            sys.exit(0)
    except IndexError:
        pass

    # No cmd-line args provided, run script normally
    main()