#!/usr/bin/env python3
from objects import *
import pyfiglet

# Major function #1
def payload_gen(hport):
    lines = ["CONTROLLER_SERVER_USER=" + server_user, "DOMAIN=" + controller_ip, "RPORT=" + str(hport), "PI_USER=" + pi_user, "CONNCHECK=" + conn_check]
    append_to_file(sidedoor_conf, lines) #Append configuration lines to config file using "w+" method
    make_tarfile(payload,"./src")

#Major function #2
def script_push(pi_user, raspberry_ip):
    cmd1="scp -rp " + payload + " " + pi_user + "@" + raspberry_ip + ":/home/" + pi_user + "/"
    cmd2="ssh " + pi_user + "@" + raspberry_ip + " \'" + "sudo tar -xvzf " + payload + " && chmod +x " + "/home/" + pi_user + "/src/nbn-pi-deploy.sh" + "\'"
    cmd3="ssh " + pi_user + "@" + raspberry_ip + " \"" + "/home/" + pi_user + "/src/nbn-pi-deploy.sh" + "\""
    print("Running: ", cmd1)
    run(cmd1)
    print("Running: ", cmd2)
    run(cmd2)
    print("Running: ", cmd3)
    run(cmd3)
    print("Finished running script_push")

def runtime(hport):
    if os.path.exists(csv_database) == False:
        run(str("touch " + csv_database))
    index = row_index(csv_database) #Index starts at zero
    print(pyfiglet.figlet_format("NBN-Pi"))
    print("Credits: Nassim Bentarka | GitHub: @NassimBentarka\n\nThis script configures the RPi to be deployed for a given company.\n")
    raspberry_ip = input("Please enter the Raspberry Pi IP or hostname: ")
    #company_name = input_inquire(clients_list,"Please choose the company name:") # Optional feature for convinience only. Create the CSV file as mentionned in the variable $clients_list before you uncomment this line.
    client_name = input("Please enter the client/company name: ")
    hport = hport + index
    payload_gen(hport) #Main Element #1
    script_push(pi_user, raspberry_ip) #Main Element #2
    csv_append(csv_database,id, hport, client_name)
    testing()

if __name__ == '__main__':
    runtime(hport)