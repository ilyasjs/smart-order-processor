import azure.functions as func
import datetime
import json
import logging
import uuid
import os
from azure.servicebus import ServiceBusClient, ServiceBusMessage

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
    # create order message
    order_message = json.dumps({
        "order_id": order_id,
        "item": item,
        "quantity": quantity,
        "status": "received"
    })

    # send to Service Bus
    try:
        connection_string = os.environ["SERVICE_BUS_CONNECTION"]
        with ServiceBusClient.from_connection_string(connection_string) as client:
            with client.get_queue_sender("orders-queue") as sender:
                sender.send_messages(ServiceBusMessage(order_message))
        logging.info(f"Order {order_id} sent to Service Bus queue")
    except Exception as e:
        logging.error(f"Failed to send to Service Bus: {str(e)}")
        return func.HttpResponse(
            body=json.dumps({"error": "failed to queue order"}),
            status_code=500,
            mimetype="application/json"
        )
    logging.info(f"Order {order_id} sent to Service Bus queue")
    # return a 200 response with the order ID
    return func.HttpResponse(
        body=order_message,
        status_code=200,
        mimetype="application/json"
        )

@app.route(route="get_order_status", methods=["GET"])
def get_order_status(req: func.HttpRequest) -> func.HttpResponse:
    logging.info("Get order status function triggered")  

    order_id = req.params.get('order_id')
    if not order_id:
        return func.HttpResponse(
            body=json.dumps({"error": "order ID is required"}),
            status_code=400,
            mimetype="application/json"
            )
    return func.HttpResponse(
        body=json.dumps({"order_id": order_id, "status": "processing"}),
        status_code=200,
        mimetype="application/json"
    )


@app.route(route="process_payment", methods=["POST"])
def process_payment(req: func.HttpRequest) -> func.HttpResponse:
    logging.info("Process payment function triggered")
    
    api_key = req.headers.get('x-api-key')
    if not api_key:
        return func.HttpResponse(
            body=json.dumps({"error": "invalid API key"}),
            status_code=401,
            mimetype="application/json"
            )
    
    try:
        req_body = req.get_json()
    except ValueError:
        return func.HttpResponse(
            body=json.dumps({"error": "invalid JSON in request body"}),
            status_code=400,
            mimetype="application/json"
        )
    
    if not req_body:
        return func.HttpResponse(
            body=json.dumps({"error": "request body is required"}),
            status_code=400,
            mimetype="application/json"
        )
    order_id = req_body.get('order_id')
    amount = req_body.get('amount')
    payment_method = req_body.get('payment_method')


    if not order_id or not amount or not payment_method:
        return func.HttpResponse(
            body=json.dumps({"error": "order ID, amount and payment method are required"}),
            status_code=400,
            mimetype="application/json"
                
        )
    
    return func.HttpResponse(
        body=json.dumps({
            "order_id": order_id,
            "amount": amount,
            "payment_method": payment_method,
            "status": "payment_received"
        }),
        status_code=200,
        mimetype="application/json"
    )