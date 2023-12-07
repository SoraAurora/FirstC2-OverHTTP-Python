// requires undici , discord.js , dotenv

const { Client, IntentsBitField } = require('discord.js');
const { request } = require('undici');

class Handler extends Client {
  constructor() {
    super({
      intents: [
        IntentsBitField.Flags.Guilds,
        IntentsBitField.Flags.GuildMembers,
        IntentsBitField.Flags.GuildMessages,
        IntentsBitField.Flags.MessageContent,
      ],
    });

    // Insert what ip your API will call 
    this.baseURL = 'http://127.0.0.1:80';

    // Registering discord command handler
    this.on('ready', () => {
      console.log(`${this.user.tag} is online.`);
    });

    this.on('messageCreate', this.handleCommand.bind(this));

    // discord bot token here :D generate from discord applications -> get token
    this.login('');
  }

  async handleCommand(message) {
    if (!message.content.startsWith('/') || message.author.bot) return;
    // this is very bad coding practice i simply try to get functionality to work as POC , you can do way WAYY better by using parameter queries for discord commands like /sendcommand {query1} {query2} this ensures even if theres spaces in the command it wil go through
    const args = message.content.slice(1).trim().match(/(?:[^\s"]+|"[^"]*")+/g);
    
    const command = args.shift().toLowerCase();

    switch (command) {
      case 'sendcommand':
        // Usage: /sendcommand <command> <agentid>
        if (args.length < 2) {
          message.reply('Usage: /sendcommand <command> <agentid>');
          return;
        }
        const sendCommandResponse = await this.sendCommand(args[0], args.slice(1).join(' '));
        const sendcommandresponseresult = "```" + sendCommandResponse.result + "```"
        message.reply(`--- Result for ${sendCommandResponse.agentid} --- \n${sendcommandresponseresult}`);
        break;

      case 'listagents':
        const listAgentsResponse = await this.listAgents();
        message.reply(`List of Agents: ${JSON.stringify(listAgentsResponse)}`);
        break;

      case 'setcheckintime':
        // Usage: /setcheckintime <check_in_time>
        if (args.length < 1) {
          message.reply('Usage: /setcheckintime <check_in_time>');
          return;
        }
        const setCheckInTimeResponse = await this.setCheckInTime(args[0]);
        message.reply(`Set Check-In Time Response: ${JSON.stringify(setCheckInTimeResponse)}`);
        break;

      default:
        // if Unknown command urmomgay
        message.reply('Unknown command. Available commands: sendcommand, listagents, setcheckintime');
        break;
    }
  }

  // actual api calls function

  async sendCommand(command, agentid) {
    const endpoint = `${this.baseURL}/send_command`;
    const data = { command, agentid };

    try {
      const response = await request(endpoint, {
        method: 'POST',
        body: JSON.stringify(data),
        headers: {
          'Content-Type': 'application/json',
        },
      });

      // Wait for 3 seconds
      await new Promise(resolve => setTimeout(resolve, 3000));

      // Trigger getResponse for the same agentid
      const getResponseResponse = await this.getResponse(agentid);


      return getResponseResponse;
    } catch (error) {
      console.error('Error sending command:', error.message);
      throw error; 
    }
  }

  async getResponse(agentid) {
    const endpoint = `${this.baseURL}/get_response`;

    try {
      const response = await request(endpoint, {
        method: 'GET',
        body: JSON.stringify({ agentid }),
        headers: {
          'Content-Type': 'application/json',
        },
      });

      if (response.statusCode !== 200) {
        throw new Error(`HTTP error! Status: ${response.statusCode}`);
      }

      const responseData = await response.body.json();
      return responseData;
    } catch (error) {
      console.error('Error getting response:', error.message);
      throw error;
    }
  }

  async listAgents() {
    const endpoint = `${this.baseURL}/list_agents`;
    
    try {
      const response = await request(endpoint, {
        method: 'GET',
      });
      
      if (response.statusCode !== 200) {
        throw new Error(`HTTP error! Status: ${response.statusCode}`);
      }
  
      const responseData = await response.body.json();
      
      return responseData.agents;
    } catch (error) {
      console.error('Error listing agents:', error.message);
      throw error;
    }
  }

  async setCheckInTime(checkInTime) {
    const endpoint = `${this.baseURL}/set_check_in_time`;
    const data = { check_in_time: checkInTime };

    try {
      const response = await request(endpoint, {
        method: 'POST',
        body: JSON.stringify(data),
        headers: {
          'Content-Type': 'application/json',
        },
      });

      if (response.statusCode !== 200) {
        throw new Error(`HTTP error! Status: ${response.statusCode}`);
      }

      const responseData = await response.body.json();
      return responseData;
    } catch (error) {
      console.error('Error setting check-in time:', error.message);
      throw error;
    }
  }
}

// Create an instance of the bot
const bot = new Handler();
