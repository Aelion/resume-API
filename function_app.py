import logging

import azure.functions as func

app = func.FunctionApp(http_auth_level=func.AuthLevel.ANONYMOUS)

@app.route(route="HttpExample")                                      
@app.blob_output(arg_name="outblob", path="testblob/counter.txt", connection="Dupa")
@app.blob_input(arg_name="inputblob", path="testblob/counter.txt", connection="Dupa")
def main(req: func.HttpRequest, outblob: func.Out[str], inputblob: str) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')
    
    name = req.params.get('name')
    if not name:
        try:
            req_body = req.get_json()
        except ValueError:
            pass
        else:
            name = req_body.get('name')

    if name:
        return func.HttpResponse(f"Hello, {name}. This HTTP triggered function executed successfully.")
    else:
        if (len(inputblob)==0):
            outblob.set("1")    
        
        count = int(inputblob)+1
        outblob.set(str(count))
        return func.HttpResponse(f"{{ \"count\":{count} }}", status_code=200)
