import requests
import time

class CommandHandler:
    def __init__(self, base_url):
        self.base_url = base_url

    def send_command(self, command , agentid):
        endpoint = f'{self.base_url}/send_command'
        data = {'command': command , 'agentid': agentid}
        response = requests.post(endpoint, json=data)
        return response.json()

    def get_response(self , agentid):
        endpoint = f'{self.base_url}/get_response'
        data = {'agentid': agentid }
        response = requests.get(endpoint,json=data)
        return response.json()
    
    def list_agents(self):
        endpoint = f'{self.base_url}/list_agents'
        response = requests.get(endpoint)
        return response.json()
    def set_check_in_time(self,check_in_time):
        endpoint = f'{self.base_url}/set_check_in_time'
        data = {'check_in_time':check_in_time }
        response = requests.post(endpoint , json=data)
        return response.json()

# Example usage:
if __name__ == '__main__':
    # Replace 'http://127.0.0.1:5000' with the actual base URL of your command control center
    command_handler = CommandHandler('http://127.0.0.1:5000')

    check_in_time = int(input("Enter Time for Agent to Check in : "))
    check_in_time_res = command_handler.set_check_in_time(check_in_time)
    print(f"Check in status : {check_in_time_res['status']}")
    exit = True

    while exit:
        option = int(input("--Menu--\n0. Exit\n1. List Agents\n2. Send command to agent\n>>"))
        if option == 1:
            # List Registered Agent
            agents = command_handler.list_agents()
            print(f"Registered Agents: {agents['agents']}")
        elif option == 2:
            command = str(input("Enter command : "))
            agentid = str(input("Enter Agent ID : "))
            send_command_res = command_handler.send_command(command,agentid)
            time.sleep(check_in_time*2)
            get_response_res = command_handler.get_response(agentid)
            print(get_response_res['result'])
        elif option == 0:
            exit = False
