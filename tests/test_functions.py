import azure.functions as func
from function_app import place_order
from unittest.mock import patch

def test_place_order_missing_quantity():
    # create a fake HTTP request
    req = func.HttpRequest(
        method='POST',
        url='/api/place_order',
        body=b'{"item": "laptop"}',  # missing quantity
        headers={'Content-Type': 'application/json'},
        params={}
    )
    
    # call the function directly
    response = place_order(req)
    
    # check the response
    assert response.status_code == 400

def test_place_order_invalid_json():
    # create a fake HTTP request with invalid JSON
    req = func.HttpRequest(
        method='POST',
        url='/api/place_order',
        headers={'Content-Type': 'application/json'},
        body=b'not valid json',
        params={}
    )

    response = place_order(req)
    
    # check the response
    assert response.status_code == 400

def test_place_order_service_bus_failure():
    with patch('function_app.ServiceBusClient') as mock_sb:
        mock_sb.from_connection_string.side_effect = Exception("Connection failed")
        
        req = func.HttpRequest(
            method='POST',
            url='/api/place_order',
            body=b'{"item": "laptop", "quantity": 2}',
            headers={'Content-Type': 'application/json'},
            params={}
        )
        response = place_order(req)
        assert response.status_code == 500

def test_place_order_success():
    with patch('function_app.ServiceBusClient') as mock_sb, \
         patch.dict('os.environ', {'SERVICE_BUS_CONNECTION': 'fake-connection'}):
        
        mock_client = mock_sb.from_connection_string.return_value.__enter__.return_value
        mock_sender = mock_client.get_queue_sender.return_value.__enter__.return_value
        mock_sender.send_messages.return_value = None

        req = func.HttpRequest(
            method='POST',
            url='/api/place_order',
            body=b'{"item": "laptop", "quantity": 2}',
            headers={'Content-Type': 'application/json'},
            params={}
        )
        response = place_order(req)
        print(f"\nResponse body: {response.get_body()}")
        assert response.status_code == 200