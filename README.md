# FirstC2-OverHTTP-Python

![Screenshot 2023-11-29 033018](https://github.com/SoraAurora/FirstC2-OverHTTP-Python/assets/91508322/da377ebf-723d-45a3-a779-7f4ed8c798ca)

This is my first C2 Over http protocol.

It has three parts , TeamServer , Handlers and Agents

Handlers send commands to TeamServer and forwards said commands to agent, agent sends data back down the chain and the handlers will get it.

Note :
The agent spawns a shell to run , this is not safe by far if your goal is concealment.
This is a work in progress

Instructions

1. Run TeamServer
2. Run Handler
3. Run Agents

To kill an agent simply send the command 'kill' to said agents.
# Inital Detection 
![image](https://github.com/SoraAurora/FirstC2-OverHTTP-Python/assets/91508322/bba7f34c-d86a-4fae-a8df-2204d0b6ad0d)

So far not alot of signatures but pattern behaviour are quite suspicious which flagged alot overall not bad for first Implant :D
# Change Log:
12/7/2023 - Added ability to Control C2 Server through Discord Bots
