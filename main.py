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

Good Practice : You can structure your application such that the same client is shared between those two parts of the code. However, in this course I've kept the Worker initialization and starter code separate so that it's easier to distinguish the role of each.
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

    """
        NOTE: 
        - when starting a Workflow from code, we don't have to specify the input in JSON format like you did on the command line. You can just use any of the allowed types, such as integers or strings or data classes, and the SDK will convert it into JSON for you automatically.
        - Recall that Workflows can run for very long periods of time. The call to `start_workflow` does not wait for workflow completion, so the line that logs the "Started Workflow" message and displays the Workflow ID and Run ID will run a fraction of a second later, even if the Workflow takes years to complete.
        - once Workflow Execution is complete, `start_workflow` returns a `WorkflowHandle` that provides access to the result

        - If you wanted to block the program at Workflow invocation time you would condense the code and use the `execute_workflow` method instead. This would make your Workflow `synchronous`.
    """
    handle = await client.start_workflow(
        GreetSomeone.run,
        sys.argv[1],
        id="greeting-workflow",
        task_queue="greeting-tasks",
    )

    print(f"Started workflow. Workflow ID: {handle.id}, RunID {handle.result_run_id}")

    # The handle.result() call used to retrieve the result will block until Workflow Execution is finished. If the Workflow Execution completes successfully, the result variable will be assigned its output. If the Workflow Execution completes unsuccessfully, an exception is raised.
    result = await handle.result()
    print(f"Result: {result}")

if __name__ == '__main__':
    asyncio.run(main())