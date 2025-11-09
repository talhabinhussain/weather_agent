from agents import Agent, Runner, RunConfig, RunContextWrapper, function_tool
from agent_config.gemini_config import Model, external_client
from pydantic import BaseModel
from typing import Union, Optional
from agent_tools.weather_tool import get_weather
from agent_tools.send_email_tool import send_weather_email



config = RunConfig(model=Model, tracing_disabled=True, model_provider=external_client)



weather_agent = Agent(
    name="Weather Agent",
    instructions="""
    # Weather Agent
    - You are a Weather update agent.
    - Fetch real-time weather updates for the user.
    - Show their current city and current temperature.
    - Call the get_weather tool for real-time weather updates.
    - Format the update with a readable response.
    - If the user asks to send weather via email, use the send_weather_email tool.
    - When sending email, format the weather data nicely before sending.
    - Always confirm when email is sent.

""",
    tools=[get_weather,send_weather_email],
    tool_use_behavior="run_llm_again" 
)


msg = input("Enter your question (e.g., 'Get weather for Karachi' or 'Send weather for Islamabad to my_email@gmail.com'): ")

result = Runner.run_sync(weather_agent, msg, run_config=config)

print(result.final_output)