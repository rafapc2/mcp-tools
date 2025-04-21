
import { McpServer } from "@modelcontextprotocol/sdk/server/mcp.js";
import { StdioServerTransport } from "@modelcontextprotocol/sdk/server/stdio.js";
import {z} from "zod";

const server = new McpServer({
  name: "Demo- Weather",
  description: "Weather API",
  version: "0.0.1",
});

//tools to implement
server.tool(
  'Fetch-weather',
  'Fetch the weather for a given city',
  {
    city: z.string().describe('City name'),
  },
  async({ city }) => {
    const response1 = await fetch(`https://geocoding-api.open-meteo.com/v1/search?name=${city}&count=10&language=en&format=json`)
    const data1 = await response1.json();
    if (data1.results.length === 0 ){
      return {
        content: [
          {
            type: "text",
            text: `City ${city} not found.`
          }
        ]
      }
    }

    const {latitude, longitude} = data1.results[0]
    const weatherResponse = await fetch(`https://api.open-meteo.com/v1/forecast?latitude=${latitude}&longitude=${longitude}&current_weather=true&hourly=temperature_2m&current=is_day,temperature_2m,relative_humidity_2m,apparent_temperature&forecast_days=1`)
    const weatherData = await weatherResponse.json();

    https://api.open-meteo.com/v1/forecast?latitude=52.52&longitude=13.41&
    return{
      content: [
        {
          type: "text",
          text: JSON.stringify(weatherData, null, 2)
        }
      ]
    }
  }

)

// listening client conections
const transport = new StdioServerTransport();
await server.connect (transport)
//console.log("Server started");
