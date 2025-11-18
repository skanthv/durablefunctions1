"""

### Step 1: HTTP Starter Function

#### Explanation line-by-line:

- `import azure.functions as func`  
  Imports Azure Functions Python SDK. It provides the `HttpRequest` and `HttpResponse` types and other function app tools.

- `import azure.durable_functions as df`  
  Imports the Durable Functions Python SDK, which contains classes to work with orchestration clients and contexts.

- `import logging`  
  Standard Python logging module to log information useful for debugging.

- `async def main(req: func.HttpRequest, starter: str) -> func.HttpResponse:`  
  Defines the main asynchronous function that Azure Functions will execute.  
  - `req`: Represents the incoming HTTP request.  
  - `starter`: The orchestration client binding, automatically injected to manage orchestration.  
  - The function returns an `HttpResponse`.

- `client = df.DurableOrchestrationClient(starter)`  
  Creates a client object to interact with the Durable Functions runtime for starting and managing orchestrations.

- `instance_id = await client.start_new("OrchestratorFunction", None, None)`  
  Starts a new instance of the orchestrator function named `"OrchestratorFunction"`.  
  - The two `None` values are for instance ID override and input to the orchestrator, here omitted for simplicity.

- `logging.info(f"Started orchestration with ID = '{instance_id}'.")`  
  Logs the orchestration instance ID for traceability.

- `return client.create_check_status_response(req, instance_id)`  
  Returns an HTTP response containing URLs the caller can use to check the status of the orchestration, such as query status, get results, or terminate.

This function listens for an HTTP POST, starts a workflow orchestration, and returns status URLs.


ensure to have function.json configured properly in same folder
This declares the HTTP trigger and the orchestration client binding your code uses.


"""


import azure.functions as func
import azure.durable_functions as df
import logging

async def main(req: func.HttpRequest, starter: str) -> func.HttpResponse:
    client = df.DurableOrchestrationClient(starter)
    instance_id = await client.start_new("OrchestratorFunction", None, None)

    logging.info(f"Started orchestration with ID = '{instance_id}'.")

    return client.create_check_status_response(req, instance_id)
