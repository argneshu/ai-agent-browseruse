import asyncio
from multiprocessing import context
from browser_use import Agent, Browser
from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv
load_dotenv()

prompt1 = "Open https://swaglabs.in/ website and add any t-shirt to cart"
prompt2 = "Open https://www.amazon.in and click samsung mobile"

browser = Browser()
async def run_agent(prompt):
        agent = Agent(
        task=prompt,
        llm=ChatGoogleGenerativeAI(model="gemini-2.0-flash"),
        )
        result = await agent.run()

       
    

async def main():
      tasks = [ 
            run_agent(prompt1),
            run_agent(prompt2)
        ]

      await asyncio.gather(*tasks, return_exceptions=True)

# async def main():
#     # Create two isolated browser contexts
#     context1 = await browser.new_context()
#     context2 = await browser.new_context()

#     # Run agents concurrently with different contexts
#     await asyncio.gather(
#         run_agent(prompt1, context1),
#         run_agent(prompt2, context2),
#         return_exceptions=False
#     )

#     # Close the shared browser after tasks complete
#     await browser.close()

asyncio.run(main())
