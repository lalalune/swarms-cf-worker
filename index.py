from swarms import OpenAIChat

def handleRequest(event):
    request = event.request

    # check if request is a GET, if it is, look for a query string
    if request.method == 'GET':
        # Get the query string from the URL
        queryString = request.url.split('?', 1)[1]
        # Parse the query string into a dictionary
        queryParams = dict(qc.split('=') for qc in queryString.split('&'))
        # Access the 'name' query parameter
        input = queryParams['input']
        agent_id = queryParams['agent_id']

    if request.method == 'POST':
        requestJson = request.json()
        input = requestJson['input']
        agent_id = requestJson['agent_id']

    # Use a JavaScript method to read the request body as text
    bodyPromise = request.text()  # Get a promise to read the body text

    def onBodyRead(bodyText):
        # Access environment variable (make sure it's defined in your wrangler.toml or Cloudflare dashboard)
        api_key = OPENAI_API_KEY  # Environment variables are accessed as if they're global variables

        # Initialize the language model
        llm = OpenAIChat(openai_api_key=api_key, model_name="gpt-3.5-turbo-0125")

        conv = Conversation()

        # TODO:load conversation memory from db, based on agent_id and user_id

        # TODO: add the messages to the conversation memory with conv.add

        task = (
            conv.return_history_as_string()
        )  # Get the conversation history
        out = llm(task)

        # TODO: more intricate agent example

        # Construct and return the response
        response = __new__(Response(out, {
            'headers': {'content-type': 'text/plain'}
        }))
        return response

    # Return the promise chain
    return bodyPromise.then(onBodyRead)

# Add event listener for fetch events
addEventListener('fetch', lambda event: event.respondWith(handleRequest(event)))
