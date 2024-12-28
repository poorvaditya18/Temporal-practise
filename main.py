import asyncio
import sys
from greeting_workflow import GreetSomeone

"""
NOTE : here if we run `python3 main.py `--> this will be normal execution of python file. 
- If we want `Worker` to execute the `Workflow` then use :
    temporal workflow start --type GreetSomeone --task-queue greeting-tasks --workflow-id my-first-workflow --input '"Poorvaditya"'

    NOTE : if we dont want to use temporal CLI then use Temporal Client

- NOTE:
 - task queues are dynamically created, typing the task queue name incorrectly would not cause an error, but it would result in two different task queues, and since the Cluster and Worker wouldn't share the same queue in this case, the Workflow Execution would never progress.
 - The command also specifies a Workflow ID, which is optional, but recommended. If omitted, a UUID will be automatically assigned as the Workflow ID.
 - When submitting a Workflow for execution through the command line, the input is always in JSON format, which is why the input in this command shows double quotes inside of single quotes.
 - Luckily, you can save the input to a file, in JSON format, and specify its path to the --input-file option, rather than using the --input option to specify the data inline, as shown here.


What Happens When you Run the Command: 
- When you run the command, it submits your execution request to the cluster, which responds with the Workflow ID, which will be the same as the one you provided, or assigned UUID if you omitted it.
- It also displays a Run ID, which uniquely identifies this specific execution of the Workflow.
- However, it does not display the result returned by the Workflow, since Workflows might run for months or years. You can use the `temporal workflow show` command to retrieve the result.
"""

import asyncio
from greeting_workflow import GreetSomeone
from temporalio.client import Client

async def main():
    # Here we run the workflow
    # name = sys.argv[1]
    # greet_obj = GreetSomeone()
    # greeting = await greet_obj.run(name)
    # print(greeting)

    # using client to start workflow --> 
    # Connect to Temporal Service
    client = await Client.connect("localhost:7233", namespace="default")

    # Start the workflow
    handle = await client.start_workflow(
        workflow=GreetSomeone,        # Workflow class name in greeting_workflow.py
        task_queue="greeting-tasks",        # Task queue from greeting_worker.py
        id="my-first-workflow",    # Unique workflow ID
        arg='Poorvaditya',              # Input for the workflow's run() method
    )

    print(f"Workflow started with ID: {handle.id}")
    result = await handle.result()
    print(f"Workflow result: {result}")

if __name__ == '__main__':
    asyncio.run(main())