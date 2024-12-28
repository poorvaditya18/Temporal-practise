"""
In workflow file we write the workflow business logic
By default every workflow have a name called as workflow type. 
 - Workflow Type : a name assigned to each Workflow. 
 - In python SDK , by default name of the class used to define the workflow.
 - Good Practise, Example : instead of GreetSomeone use GreetingWorkflow, 
 -  So, when you execute this workflow, Temporal internally identifies it as a workflow of type GreetingWorkflow.

About Inpute Parameters and Return Values : 
 - In order for Temporal to store the Workflow's input and output, data used in input parameters and return values must be serializable.
 - By default, Temporal can handle null or binary values, as well as any data that can be serialized into JSON.
 -  note: most of the types typically use in a function, such as integers and floating point numbers, boolean values, and strings, are all handled automatically, as are `dataclasses` composed from these types, but types such as `datetime`, `functions`, or other non-serializable data types are prohibited as either input parameters or return values.

 - We can also create custom data converter to encrypt the data as it enters the Temporal Cluster and decrypt it upon exit, thereby maintaining the confidentiality.
 - Since, the Event History contains the input and output, which is also sent across the network from the application to the Temporal Cluster, you'll have better performance if you limit the amount of data sent.
 -  Temporal Server imposes various limits beyond which it will emit warnings or errors.
"""
from temporalio import workflow

# @workflow.defn : decorator to the class that will define the Workflow Definition
@workflow.defn
class GreetSomeone:

    # @workflow.run:  decorator to the function that defines the Workflow Function. Entry point for workflow execution. 
    @workflow.run
    async def run(self, name:str) -> str:
        return f"Hello {name}!"