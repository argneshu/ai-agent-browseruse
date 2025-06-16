import asyncio
from browser_use import Agent
from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv
load_dotenv()

prompt = "Open https://swaglabs.in/ website, add red t-shirt to cart and check that t-shirt color should be red"


async def main():
    agent = Agent(
        task=prompt,
        llm=ChatGoogleGenerativeAI(model="gemini-1.5-flash-002"),
    )
    await agent.run()

asyncio.run(main())
