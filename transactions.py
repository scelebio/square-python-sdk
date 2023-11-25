import csv
from square.client import Client
from apimatic_core.configurations.global_configuration import GlobalConfiguration
import json


# Initialize Square client
client = Client(
    access_token='',
    environment='production'
)

'''
result = client.payments.list_payments(
    begin_time = "2020-01-01T00:00:00Z",
  location_id = "LVZZWKNFGJVEQ"
)

if result.is_success():
  print(result.body)
elif result.is_error():
  print(result.errors)

# save everything to csv
csv_file_path = '/Users/sarpercelebioglu/Parking Management Dropbox/Sarper Celebioglu/Parking Management/04_Accounting/Revenues/RCE revenue/transactions.csv'
with open(csv_file_path, 'w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(["Transaction ID", "Transaction Time", "Transaction Amount", "Transaction Status"])
    for transaction in result.body['payments']:
        writer.writerow([transaction['id'], transaction['created_at'], transaction['amount_money']['amount'], transaction['status']])
'''

def list_all_payments(location_id=None):
    all_payments = []
    cursor = None

    # Loop until all pages have been fetched
    while True:
        result = client.payments.list_payments(
            location_id=location_id,
            cursor=cursor  # Use the cursor for pagination
        )
        if result.is_success():
            body = result.body
            payments = body.get('payments', [])
            all_payments.extend(payments)
            cursor = body.get('cursor')  # Square API returns the cursor for the next page here
            if not cursor:  # No more pages left to fetch
                break
        else:
            print(f"Error in API call for location {location_id}:", result.errors)
            break

    return all_payments

location_ids=['LFFPWY9HBSY6J']

csv_file_path = '/Users/sarpercelebioglu/Parking Management Dropbox/Sarper Celebioglu/Parking Management/04_Accounting/Revenues/RCE revenue/transactions.csv'  # Replace with your desired path

# Collect all unique keys from all payments
unique_keys = set()
for location_id in location_ids:
    payments = list_all_payments(location_id=location_id)
    for payment in payments:
        unique_keys.update(payment.keys())

# Write to the CSV file
with open(csv_file_path, mode='w', newline='') as file:
    writer = csv.DictWriter(file, fieldnames=unique_keys)
    writer.writeheader()
    for location_id in location_ids:
        payments = list_all_payments(location_id=location_id)
        for payment in payments:
            payment_data = {key: payment.get(key, '') for key in unique_keys}
            writer.writerow(payment_data)

print("CSV file created with all transaction data for multiple locations.")
