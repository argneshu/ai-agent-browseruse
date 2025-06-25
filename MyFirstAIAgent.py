import asyncio
from browser_use import Agent
from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv
load_dotenv()

prompt = "Open Facebook login, list test scenarios of login page, then output Playwright TypeScript test code"


async def main():
    agent = Agent(
        task=prompt,
        llm=ChatGoogleGenerativeAI(model="gemini-1.5-flash"),
    )
    result = await agent.run()
    print(result)

asyncio.run(main())
