import azure.functions as func
import datetime
import json
import logging
import uuid

app = func.FunctionApp()

@app.route(route="place_order", methods=["POST"])
def place_order(req: func.HttpRequest) -> func.HttpResponse:
    logging.info("Place order function triggered")
    
    #parse the request body as JSON
    try:
        req_body = req.get_json()
    except ValueError:
        return func.HttpResponse(
            body=json.dumps({"error": "invalid JSON in request body"}),
            status_code=400,
            mimetype="application/json"
            )
    item = req_body.get("item")
    quantity = req_body.get("quantity")

    # validate that 'item' and 'quantity' exist
    if not item or not quantity:
        # return 400 bad request
        return func.HttpResponse(
            body=json.dumps({"error": "item and quantity are required"}),
            status_code=400,
            mimetype="application/json"
            )
    
    # generate a unique order ID
    order_id = str(uuid.uuid4())
    # return a 200 response with the order ID
    return func.HttpResponse(
        body=json.dumps({"order_id": order_id, "status": "received"}),
        status_code=200,
        mimetype="application/json"
        )
