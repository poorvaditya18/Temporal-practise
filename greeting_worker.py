"""
Role of Worker: 
- Workers execute your Workflow code
- Worker itself is provided by the Temporal SDK, but your application will include code to configure and run it.
- When that code executes, the Worker establishes a persistent connection to the Temporal Cluster and begins polling a Task Queue on the Cluster, seeking work to perform.
- note: Since Workers execute your code, any Workflows you execute will make no progress unless `one Worker is running.`
- When you start a Temporal Worker (e.g., running greeting_worker.py), it connects to the Temporal Cluster and registers all the Workflow Types (classes with the @workflow.defn decorator) and Activity Types it knows about.

Initializing a Worker: 
 1. `A Temporal Client`, which is used to communicate with the Temporal Cluster.
 2. `The name of a Task Queue`, which is maintained by the Temporal Server and polled by the Worker.
 3. `The Workflow Definition class`, used to register the Workflow implementation with the Worker.


The lifetime of Worker:
- The `worker.run()` function used to start this Worker is a blocking function that doesn't stop unless it is shut down or encounters a fatal error.
- NOTE : worker.run() call runs indefinitely and never returns. Workers in Temporal are designed to continuously poll the Temporal service for new tasks to execute (both workflows and activities). As long as the worker is running, it will keep listening for new tasks in the task queue.
- If the Workflows it handles are relatively short, then a single Worker might execute thousands or even millions of them during its lifetime.
- NOTE: a Workflow can run for years, while the server where a Worker process is running might be rebooted after a few months by an administrator doing maintenance.
- If your Workflow Type (the specific kind of workflow you're running) is registered with multiple Workers, another Worker will automatically take over if the original Worker stops or crashes.
- If no other Workers are available, Temporal simply pauses the Workflow at the exact point it stopped.
When the original Worker restarts (or a new Worker registers for the Workflow Type), the Workflow will resume from where it left off.

Task Queue:
- task_queue:  lets the Worker know which Task Queue to poll and what Workflow is registered to be executed by the worker.
- Worker will then begin a "long poll" on the specified task queue.
- Task queue names are case sensitive. Keep it short and simple as practical"
"""
import asyncio

from temporalio.client import Client
from temporalio.worker import Worker

from greeting_workflow import GreetSomeone


async def main():
    client_connection = await Client.connect("localhost:7233", namespace="default")
    # Run the worker
    worker = Worker(client_connection, task_queue="greeting-tasks", workflows=[GreetSomeone])
    await worker.run()

if __name__ == "__main__":
    asyncio.run(main())
