To set up Azure Functions with Python locally in the proper order without confusion, here is a well-structured step-by-step workflow following the Microsoft Learn guidance you're referring to:

### Correct Order of Steps for Azure Functions Python Project Setup

1. **Create a project folder (your working directory):**  
   This is where your Azure Functions app code and configuration will live.  
   Example:  
   ```bash
   mkdir myfuncapp
   cd myfuncapp
   ```

2. **Create a Python virtual environment inside this folder:**  
   This isolates dependencies.  
   Example for Windows:  
   ```bash
   python -m venv .venv
   ```
   Or for Linux/macOS:  
   ```bash
   python3 -m venv .venv
   ```

3. **Activate the virtual environment:**  
   In Windows Powershell:  
   ```bash
   .\.venv\Scripts\Activate.ps1
   ```
   In macOS/Linux or Windows Command Prompt:  
   ```bash
   source .venv/bin/activate
   ```

4. **Check and install Azure Functions Core Tools (func) if not present:**  
   To check if Core Tools are installed and accessible:  
   ```bash
   func --version
   ```
   If this outputs the version number, func is installed and working.

   If not installed, follow the install directions for your OS from https://learn.microsoft.com/en-us/azure/azure-functions/functions-run-local#install-the-azure-functions-core-tools
   download the msi file for windows and install it.

5. **Initialize the Azure Functions project here (inside your existing folder):**  
   Run:  
   ```bash
   func init . --worker-runtime python
   ```
   The dot `.` means initialize the current folder as a function app project without creating a new folder inside it.

6. **Create your first function:**  
   ```bash
   func new --name HttpExample --template "HTTP trigger" --authlevel "anonymous"
   ```

Note:
When you create a new function with func new in a Python Azure Functions project, the default behavior has changed in recent Core Tools versions: instead of creating a new subfolder per function, it places the function code directly into the function_app.py file (or the main Python file specified in your project). This is especially true for Python projects using the "single file" pattern by default.

The @app.route(route="HttpExample", auth_level=func.AuthLevel.ANONYMOUS) decorator is how the Azure Functions Python worker maps HTTP triggers to handler functions inside that file.

So, it is normal that your HTTP trigger function is inside function_app.py instead of a subfolder. The folder-per-function structure is more common in C# or Node.js runtimes.

If you want to create separate files or folders per function, you can customize the project architecture, but the default single-file method works perfectly.


7. **Check your environment and run your function app locally:**  
   ```bash
   func start
   ```
#### This means your function named HttpExample is available locally at the URL:
http://localhost:7071/api/HttpExample

What to do next to test your function:
Open a web browser or API tool like Postman.

Enter the URL exactly:
http://localhost:7071/api/HttpExample

Make a GET request to this URL.


How to pass the name parameter:
Option 1: Pass name as a query string (GET request)
Simply attach ?name=YourName to the function URL and open it in the browser or use CURL/Postman with a GET request.

Example URL:

text
http://localhost:7071/api/HttpExample?name=Sarad
This URL passes Sarad as the value for the name parameter.

#### Option 2: Pass name in the JSON request body (POST request)
Send a POST request with JSON body:

json
{
  "name": "Sarad"
}
Using CURL:

bash
curl -X POST \
  http://localhost:7071/api/HttpExample \
  -H "Content-Type: application/json" \
  -d "{\"name\":\"Sarad\"}"

##### multi line curl commands
in windows command prompt, no \ allowed. so just type everything in 1 line
in widows powershell, backtick  ` is line continuation
in bash, \ is allowed as continuation character

```

(.venv) C:\Users\sarad\Documents\VSCodeProjects\AzureDurableFunction>curl -X POST http://localhost:7071/api/HttpExample -H "Content-Type: application/json" -d "{\"name\":\"sk\"}"
Hello, sk. This HTTP triggered function executed successfully.
(.venv) C:\Users\sarad\Documents\VSCodeProjects\AzureDurableFunction>

```

#### How to stop the function app?
Go back to your terminal window running func start and press Ctrl+C.

#### Optional:
You can also run with more detailed logs:

bash
func start --verbose

### Create Durable functions
Run the command below to list all Python templates installed:
func templates list --language python
This will show you all templates you can use with func new.
Durable Functions templates might be slightly differently named or missing:

(.venv) C:\Users\sarad\Documents\VSCodeProjects\AzureDurableFunction>func templates list --language python
'local.settings.json' found in root directory (C:\Users\sarad\Documents\VSCodeProjects\AzureDurableFunction).
Resolving worker runtime to 'python'.
Python Templates:
  Azure Blob Storage trigger
  Azure Cosmos DB trigger
  Dapr Publish Output Binding
  Dapr Service Invocation Trigger
  Dapr Topic Trigger
  Durable Functions activity
  Durable Functions entity
  Durable Functions HTTP starter
  Durable Functions orchestrator
  Azure Blob Storage Trigger (using Event Grid)
  Azure Event Grid trigger
  Azure Event Hub trigger
  HTTP trigger
  Kafka output
  Kafka trigger
  MySql Input Binding
  MySql Output Binding
  MySql Trigger
  Azure Queue Storage trigger
  RabbitMQ trigger
  Azure Service Bus Queue trigger
  Azure Service Bus Topic trigger
  SQL Input Binding
  SQL Output Binding
  SQL Trigger
  Timer trigger


(.venv) C:\Users\sarad\Documents\VSCodeProjects\AzureDurableFunction>


## next steps
We will create three components:

HTTP Starter (to start the orchestration)

Orchestrator Function (defines the workflow)

Activity Function (actual work executed by the orchestrator)

## Orchestration starter function
Create a folder HttpStart in your project with a file __init__.py containing code


# Before running code checklist


- Each function (like `HttpStart` and `HttpExample`) has its own folder.
- Inside each function folder, you should have:
  - An `__init__.py` file for the code.
  - A `function.json` for bindings.


## 1. **Check that each function folder is complete:**

For each folder (example: `HttpStart`):
- `__init__.py` contains the complete function code.
- `function.json` configures the trigger and bindings.

If you moved `HttpExample` out, confirm its folder still keeps both files and is inside the root project like `HttpStart`.

## 2. **Ensure host.json and local.settings.json exist in the root**  
These files control app-level configuration and connection settings.

## 3. **Check requirements.txt**  
Make sure your requirements include:
```
azure-functions
azure-functions-durable
```

## 4. **Activate your virtual environment**
**YES, you should always activate your `.venv` before running or developing your functions.**  
- This ensures you use the correct, isolated Python packages (not system-wide).

## 5. **Run func start from your root folder**
- After activating `.venv`, in the root folder (`AZUREDURABLEFUNCTION`), run:
  ```
  func start
  ```

## 6. **Verify setup in terminal**
- When the host starts, it should list all functions found (both `HttpStart` and `HttpExample`), with their URL endpoints.
- You should now be able to call each endpoint (e.g., by POST to `/api/HttpStart`).



# httpexample . function.json explanation
```
Explanation of Each Line
"bindings": [
Declares all the bindings (triggers and outputs) for the function. Bindings connect your code to the Azure Functions runtime.

First binding - HTTP trigger:
json
    {
      "authLevel": "anonymous",
      "type": "httpTrigger",
      "direction": "in",
      "name": "req",
      "methods": ["get", "post"]
    }
"authLevel": "anonymous"
Anyone can call this endpoint (no authentication required).

"type": "httpTrigger"
This function is triggered by an HTTP request.

"direction": "in"
The data flows into the function (it's an input).

"name": "req"
This binds the HTTP request to a Python parameter named req in your __init__.py code.

"methods": ["get", "post"]
Allows both GET and POST HTTP methods to trigger the function.

Second binding - HTTP output:
json
    {
      "type": "http",
      "direction": "out",
      "name": "$return"
    }
"type": "http"
This binding defines the HTTP response output.

"direction": "out"
Data flows out of the function (it's an output).

"name": "$return"
The return value from your function code will be sent back to the HTTP caller.

Where to place this file
Save this as function.json inside your HttpExample folder (beside __init__.py).

Why needed
This tells Azure Functions how to connect incoming HTTP requests to your code and respond properly. Without it, your function won’t be discovered or indexed by the runtime.
```