import asyncio
import sys
from greeting_workflow import GreetSomeone

async def main():
    # Here we run the workflow
    name = sys.argv[1]
    greet_obj = GreetSomeone()
    greeting = await greet_obj.run(name)
    print(greeting)

if __name__ == '__main__':
    asyncio.run(main())