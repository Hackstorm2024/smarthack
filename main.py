import json
from collections import defaultdict
from clase import create_clase
from config import BASE_URL, API_KEY
from apiclient import start_session, play_round, end_session
from helper import transform_and_append_demands

session_id = start_session(API_KEY, BASE_URL)

# Initialize simulation parameters
DAYS = 42  # Run from day 0 to day 42
graph = create_clase()  # Load the network graph structure if it’s static
transactions = defaultdict(list)  # To store transactions for each day

# Precompute daily demands and incoming supplies for each tank
daily_demands = defaultdict(lambda: defaultdict(int))
daily_incoming_supply = defaultdict(lambda: defaultdict(int))

# Precompute all demands and incoming supplies
for day in range(DAYS):
    for tank_id, tank_info in graph['tanks'].items():
        tank_demand = sum(
            demand.quantity for conn in tank_info['connections']['to_orders']
            for demand in graph['orders'].get(conn.to_id, {}).get('order', {}).demands
            if demand.start_delivery_day <= day <= demand.end_delivery_day
        )
        daily_demands[day][tank_id] = tank_demand
        daily_incoming_supply[day][tank_id] = sum(
            tx['quantity'] for tx in transactions[day] if tx['destination'] == tank_id
        )

# Simulation loop
for day in range(DAYS):
    print(f'==== Day {day} ====')
    day_data = {"day": day, "movements": []}

    graph = create_clase()

    # Accumulate transactions for the current day
    current_day_transactions = transactions[day]
    node_updates = defaultdict(int)  # Accumulate capacity updates per node

    for transaction in current_day_transactions:
        node_type = transaction['type']
        destination_id = transaction['destination']
        amount = transaction['quantity']

        if node_type in graph and destination_id in graph[node_type]:
            destination_node = graph[node_type][destination_id]['node']

            # Allow overflow by not limiting max capacity
            node_updates[(node_type, destination_id)] += amount
            print(f"Updated {node_type} {destination_node.name}'s capacity by {amount}. New capacity (allowing overflow): {destination_node.capacity + amount}")

    # Apply accumulated updates to each node, allowing overflow
    for (node_type, destination_id), total_amount in node_updates.items():
        destination_node = graph[node_type][destination_id]['node']
        destination_node.capacity += total_amount
        print(f"Updated {node_type} {destination_node.name}'s capacity by {total_amount}. New capacity: {destination_node.capacity}")

    # Process each refinery and connected tanks
    for refinery_id, refinery_info in graph['refineries'].items():
        refinery = refinery_info['node']

        for connection in refinery_info['connections']:
            tank_id = connection.to_id
            tank_info = graph['tanks'][tank_id]
            tank_node = tank_info['node']

            # Retrieve precomputed demand and incoming supply
            tank_demand = daily_demands[day][tank_id]
            available_supply = tank_node.capacity + daily_incoming_supply[day][tank_id]

            # Ensure all demand is fulfilled by allowing overflow if needed
            if available_supply < tank_demand:
                additional_supply_needed = tank_demand - available_supply

                # Bypass max output and capacity limits to ensure fulfillment
                refinery.capacity -= additional_supply_needed
                transactions[day].append({
                    'type': 'refinery',
                    'destination': tank_id,
                    'quantity': additional_supply_needed
                })
                print(f"Added {additional_supply_needed} units to Tank {tank_node.name} from Refinery {refinery.name}, allowing overflow.")

                day_data["movements"].append({
                    "connectionId": connection.id,
                    "amount": additional_supply_needed
                })

            # Fulfill demands from the available supply
            remaining_supply = available_supply
            for conn in tank_info['connections']['to_orders']:
                order_id = conn.to_id
                order = graph['orders'].get(order_id, {}).get('order')

                if order is not None:
                    for demand in sorted(order.demands, key=lambda d: d.end_delivery_day):
                        if demand.start_delivery_day <= day <= demand.end_delivery_day:
                            amount_to_fulfill = min(demand.quantity, remaining_supply)

                            transactions[day].append({
                                'type': 'tank',
                                'destination': order_id,
                                'quantity': amount_to_fulfill
                            })
                            remaining_supply -= amount_to_fulfill
                            print(f"Sent {amount_to_fulfill} from Tank {tank_node.name} to fulfill Order {order_id}, allowing overflow.")

                            # Log fulfilled transaction
                            day_data["movements"].append({
                                "connectionId": conn.id,
                                "amount": amount_to_fulfill
                            })

                            if demand.quantity <= amount_to_fulfill:
                                break

    # Write each day's data to a JSON file
    with open(f"day_{day}.json", "w") as file:
        json.dump(day_data, file, indent=2)

    with open(f"day_{day}.json", "r") as f:
        day_data = json.load(f)  # Load the JSON data as a dictionary
        demands = play_round(day_data, session_id, BASE_URL, API_KEY)
        transform_and_append_demands(demands)

    print(f"Day {day} data written to day_{day}.json")

# End session
print(end_session(API_KEY, BASE_URL))
