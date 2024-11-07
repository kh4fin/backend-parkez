import midtransclient

def create_midtrans_transaction(order_id, gross_amount, user):
    snap = midtransclient.Snap(
        is_production=False,
        server_key='your-server-key',
        client_key='your-client-key'
    )

    transaction_data = {
        "transaction_details": {
            "order_id": order_id,
            "gross_amount": gross_amount
        },
        "customer_details": {
            "email": user.email,
            "first_name": user.first_name,
            "last_name": user.last_name,
        }
    }

    transaction = snap.create_transaction(transaction_data)
    return transaction['redirect_url']