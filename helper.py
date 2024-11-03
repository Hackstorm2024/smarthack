import json
import pandas as pd
import uuid

def transform_and_append_demands(demands):

    try:

        # Transform demands to match CSV format
        transformed_demands = []
        for demand in demands:
            transformed_demands.append({
                "id": str(uuid.uuid4()),  # Generate a unique ID
                "customer_id": demand["customerId"],
                "quantity": demand["amount"],
                "post_day": demand["postDay"],
                "start_delivery_day": demand["startDay"],
                "end_delivery_day": demand["endDay"]
            })

        # Convert to DataFrame
        df = pd.DataFrame(transformed_demands)

        # Append to CSV
        df.to_csv('demands.csv', mode='a', index=False, header=False, sep=';')  # Ensure the delimiter matches the format
    except:
        return
