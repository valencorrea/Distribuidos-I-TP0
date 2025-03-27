import sys
from constants import WRITE_MODE, YAML_TAB

def write_server(file, clients):
    file.write(YAML_TAB + "server:\n")
    file.write(YAML_TAB + YAML_TAB + "container_name: server\n")
    file.write(YAML_TAB + YAML_TAB + "image: server:latest\n")
    file.write(YAML_TAB + YAML_TAB + "entrypoint: python3 /main.py\n")
    file.write(YAML_TAB + YAML_TAB + "environment:\n")
    file.write(YAML_TAB + YAML_TAB + YAML_TAB + "- PYTHONUNBUFFERED=1\n")
    file.write(YAML_TAB + YAML_TAB + YAML_TAB + "- CLIENTS_AMOUNT=" + str(clients) + "\n")
    file.write(YAML_TAB + YAML_TAB + "volumes:\n")
    file.write(YAML_TAB + YAML_TAB + YAML_TAB + "- ./server/config.ini:/config.ini\n")
    file.write(YAML_TAB + YAML_TAB + "networks:\n")
    file.write(YAML_TAB + YAML_TAB + YAML_TAB + "- testing_net\n")
    file.write("\n")

def write_client(id, file):
    file.write(YAML_TAB + "client" + str(id) + ":\n")
    file.write(YAML_TAB + YAML_TAB + "container_name: client" + str(id) + "\n")
    file.write(YAML_TAB + YAML_TAB + "image: client:latest\n")
    file.write(YAML_TAB + YAML_TAB + "entrypoint: /client\n")
    file.write(YAML_TAB + YAML_TAB + "environment:\n")
    file.write(YAML_TAB + YAML_TAB + YAML_TAB + "- CLI_ID=" + str(id) + "\n")
    file.write(YAML_TAB + YAML_TAB + YAML_TAB + "- CLI_NAME=" + "DummyName" + str(id) + "\n")
    file.write(YAML_TAB + YAML_TAB + YAML_TAB + "- CLI_SURNAME=" + "DummySurname" + str(id) + "\n")
    file.write(YAML_TAB + YAML_TAB + YAML_TAB + "- CLI_ID_NUMBER=" + "12345678\n")
    file.write(YAML_TAB + YAML_TAB + YAML_TAB + "- CLI_DATE_OF_BIRTH=" + "1999-07-10" + "\n")
    file.write(YAML_TAB + YAML_TAB + YAML_TAB + "- CLI_BET_NUMBER=" + "111" + str(id) + "\n")
    file.write(YAML_TAB + YAML_TAB + "volumes:\n")
    file.write(YAML_TAB + YAML_TAB + YAML_TAB + "- ./client/config.yaml:/config.yaml\n")
    file.write(YAML_TAB + YAML_TAB + YAML_TAB + "- ./.data/agency-" + str(id) + ".csv:/.data/agency.csv\n")
    file.write(YAML_TAB + YAML_TAB + "networks:\n")
    file.write(YAML_TAB + YAML_TAB + YAML_TAB + "- testing_net\n")
    file.write(YAML_TAB + YAML_TAB + "depends_on:\n")
    file.write(YAML_TAB + YAML_TAB + YAML_TAB + "- server\n")
    file.write("\n")

def write_clients(file, clients):
    for id in range(1, int(clients)+1):
        write_client(id, file)

def write_services(file, clients):
    file.write("services:\n")
    write_server(file, clients)
    write_clients(file, clients)

def write_networks(file):
    file.write("networks:\n")
    file.write(YAML_TAB + "testing_net:\n")
    file.write(YAML_TAB + YAML_TAB + "ipam:\n")
    file.write(YAML_TAB + YAML_TAB + YAML_TAB + "driver: default\n")
    file.write(YAML_TAB + YAML_TAB + YAML_TAB + "config:\n")
    file.write(YAML_TAB + YAML_TAB + YAML_TAB + YAML_TAB + "- subnet: 172.25.125.0/24\n")

def write_file(file, clients):
    file.write("name: tp0\n")
    write_services(file, clients)
    write_networks(file)

def create_file(name, clients):
    print("Creating", name, "file for", clients, "clients")
    file = open(name, WRITE_MODE)
    write_file(file, clients)
    print("File succesfully created")
    file.close()

def main():
    output_file_name, clients = sys.argv[1], sys.argv[2]
    create_file(output_file_name, clients)

if __name__ == "__main__":
    main()
