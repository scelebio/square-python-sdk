import csv
from square.client import Client
from apimatic_core.configurations.global_configuration import GlobalConfiguration
from datetime import datetime


# Initialize Square client
client1 = Client(
    access_token='EAAAF1ZpSxMh_6qSmmYhN_yJGCv322ZSNKB_9PKc36BRr5Ww3ALrWgqP3_dYD5Cw',
    environment='production'
)

client2 = Client(
    access_token='EAAAF92BUf0jaZfE9kT8b_UnyssKUgs0rm5aMlq0Rx4tD03YZryc2uGoxSqeMf6x',
    environment='production'
)

# Mapping of location IDs to names
location_names = {
    "LVZZWKNFGJVEQ": "155 Eddy Lot",
    "LTW9X4EHBAA02": "170 Columbus Garage",
    "LG1JMYXMWTZ1Q": "25 Mason Lot",
    "LPEY06PGRHDSZ": "51 Mason Garage",
    "LQYD3Y5D76DZK": "520 Mason Garage",
    "L75XD571ENXXC": "635 Sansome Lot",
    "LYHXJ641AXX7W": "660 Sutter Lot",
    "LFFPWY9HBSY6J": "750 Bush Garage",
    "L7GCYEB2VZ091": "847 Front Garage",
    "LR6HXYMJBM46T": "Post & Taylor Garage",
    "L0N7RBT948527": "Prestige Park LLC",
    "LZB0QNJWCC243": "Royal Parking LLC",
    "BFYHS1WWN8N73": "SF City Parking, LLC",
    "C0XSFKPN4YNJH": "136 Townsend Garage"
    # Add other mappings as needed
}



def list_unpaid_invoices(client, location_ids):
    all_invoices = []
    for location_id in location_ids:
        cursor = None
        while True:
            result = client.invoices.list_invoices(location_id=location_id, cursor=cursor)
            if result.is_success():
                body = result.body
                invoices = body.get('invoices', [])
                filtered_invoices = [invoice for invoice in invoices if invoice['status'] in ['UNPAID', 'PARTIALLY_PAID']]
                all_invoices.extend(filtered_invoices)
                cursor = body.get('cursor')
                if not cursor:
                    break
            else:
                print(f"Error in fetching invoices for location {location_id}:", result.errors)
                break
    return all_invoices

location_ids_1 = ['LVZZWKNFGJVEQ', 'LTW9X4EHBAA02', 'LG1JMYXMWTZ1Q', 'LPEY06PGRHDSZ', 'LQYD3Y5D76DZK', 'L75XD571ENXXC', 'LYHXJ641AXX7W', 'LFFPWY9HBSY6J', 'L7GCYEB2VZ091', 'LR6HXYMJBM46T', 'L0N7RBT948527', 'LZB0QNJWCC243', 'BFYHS1WWN8N73']
location_ids_2 = ['C0XSFKPN4YNJH']
invoice_columns = ['location_id','invoice_date', 'invoice_number', 'recipient_name', 'phone_number', 'email_address', 'amount']

csv_file_path = '/Users/sarpercelebioglu/Parking Management Dropbox/Sarper Celebioglu/Parking Management/04_Accounting/financing/outstanding_invoices/outstanding.csv'

# ... [Previous parts of the script] ...
# Usage example
unpaid_invoices_client1 = list_unpaid_invoices(client1, location_ids_1)
unpaid_invoices_client2 = list_unpaid_invoices(client2, location_ids_2)

# Combine invoices from both clients
combined_unpaid_invoices = unpaid_invoices_client1 + unpaid_invoices_client2

# Write to CSV
with open(csv_file_path, mode='w', newline='') as file:
    
    writer = csv.DictWriter(file, fieldnames=invoice_columns)
    writer.writeheader()

    for invoice in combined_unpaid_invoices:
        row = {col: '' for col in invoice_columns}

        # Correctly map location_id to location name
        location_id = invoice.get('location_id', '')
    
        row['location_id'] = location_names.get(invoice.get('location_id'), invoice.get('location_id'))

        row['invoice_number'] = location_names.get(invoice.get('invoice_number'), invoice.get('invoice_number'))
        primary_recipient = invoice.get('primary_recipient', {})
        recipient_name = f"{primary_recipient.get('given_name', '')} {primary_recipient.get('family_name', '')}".strip()
        phone_number = primary_recipient.get('phone_number', '')
        email_address = primary_recipient.get('email_address', '')
        payment_requests = invoice.get('payment_requests', {})
        
          # Extract due_date from the first item in payment_requests
        payment_requests = invoice.get('payment_requests', [])
        if payment_requests and isinstance(payment_requests, list):
            first_request = payment_requests[0]
            invoice_date = first_request.get('due_date', 'No Due Date')
        else:
            invoice_date = 'No Due Date'

        row['recipient_name'] = recipient_name
        row['phone_number'] = phone_number
        row['email_address'] = email_address
        row['invoice_date'] = invoice_date

        next_payment_amount = invoice.get('next_payment_amount_money', {}).get('amount', 0)
        row['amount'] = int(next_payment_amount) / 100

        writer.writerow(row)

print("CSV file created with all transaction data for multiple locations.")

