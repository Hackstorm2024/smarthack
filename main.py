from clase import create_clase

transactions = {}

graph = create_clase()
import json
from collections import defaultdict

# Initialize simulation parameters
DAYS = 43
transactions = defaultdict(list)  # Stores transactions for each day

# Function to simulate a day in the network and generate daily JSON
def simulate_day(day, graph, transactions):
    # JSON structure for the day
    day_data = {
        "day": day,
        "movements": []
    }
    
    # Process all transactions scheduled for today
    if day in transactions:
        for transaction in transactions[day]:
            # Get the destination (tank or order) and add the quantity
            if transaction['type'] == 'tank':
                tank = graph['tanks'][transaction['destination']]['node']
                tank.capacity += transaction['quantity']
                print(f"Day {day}: Added {transaction['quantity']} to Tank {tank.name}. Current capacity: {tank.capacity}")
            elif transaction['type'] == 'order':
                order = graph['orders'][transaction['destination']]['order']
                print(f"Day {day}: Order ID {order.customer.id} fulfilled with {transaction['quantity']} from Tank {transaction['source']}.")

            # Add movement to day data
            day_data["movements"].append({
                "connectionId": transaction['source'],  # This is assumed to be the connection's ID
                "amount": transaction['quantity']
            })
    
    # Process refineries to tanks
    for refinery_id, refinery_data in graph['refineries'].items():
        refinery = refinery_data['node']
        for connection in refinery_data['connections']:
            tank_id = connection.to_id
            if tank_id in graph['tanks']:
                tank = graph['tanks'][tank_id]['node']
                if tank.capacity < tank.max_capacity:  # Check capacity
                    # Calculate available space in tank
                    available_space = tank.max_capacity - tank.capacity
                    # Determine the quantity to send (up to the refinery max output or available space)
                    quantity = min(refinery.max_output, available_space)
                    # Schedule a transaction from refinery to tank with lead time
                    arrival_day = day + connection.lead_time_days
                    if arrival_day < DAYS:
                        transactions[arrival_day].append({
                            'type': 'tank',
                            'source': connection.id,  # Assuming the connection has an ID attribute
                            'destination': tank_id,
                            'quantity': quantity
                        })
                        print(f"Day {day}: Scheduled {quantity} from Refinery {refinery.name} to Tank {tank.name} (arrives on Day {arrival_day})")

    # Process tanks to orders
    for tank_id, tank_data in graph['tanks'].items():
        tank = tank_data['node']
        for order_connection in tank_data['connections']['to_orders']:
            order_id = order_connection.to_id
            if order_id in graph['orders']:
                order = graph['orders'][order_id]['order']
                for demand in order.demands:
                    # Check if today's date is within the delivery window
                    if day >= demand.start_delivery_day and day <= demand.end_delivery_day:
                        if tank.capacity >= demand.quantity:  # Check if tank has enough supply
                            # Schedule a transaction from tank to order
                            transactions[day].append({
                                'type': 'order',
                                'source': tank_id,
                                'destination': order_id,
                                'quantity': demand.quantity
                            })
                            tank.capacity -= demand.quantity  # Deduct from tank capacity
                            print(f"Day {day}: Scheduled {demand.quantity} from Tank {tank.name} to Order ID {order.customer.id}")
                            day_data["movements"].append({
                                "connectionId": tank_id,  # Assuming the tank's ID is used here as a unique identifier
                                "amount": demand.quantity
                            })
    
    # Save day_data JSON for the current day
    with open(f"day_{day}.json", "w") as f:
        json.dump(day_data, f, indent=2)

# Run the simulation for each day
for day in range(DAYS):
    simulate_day(day, graph, transactions)


