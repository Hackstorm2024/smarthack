from clase import create_clase
import json
from collections import defaultdict

DAYS = 43
transactions = defaultdict(list)
graph = create_clase()

# Calculul costului și emisiilor pentru transport
def calculate_costs(connection, quantity):
    co2_per_km = getattr(connection, 'co2_per_km', 0)
    distance_cost = connection.distance * quantity
    co2_emissions = co2_per_km * connection.distance * quantity
    return distance_cost, co2_emissions

# Simularea unei zile
def simulate_day(day, graph, transactions):
    day_data = {"day": day, "movements": []}
    
    # Executăm tranzacțiile pentru ziua curentă
    if day in transactions:
        for transaction in transactions[day]:
            if transaction['type'] == 'tank':
                tank = graph['tanks'][transaction['destination']]['node']
                tank.capacity += transaction['quantity']
                print(f"Day {day}: Added {transaction['quantity']} to Tank {tank.name}. Current capacity: {tank.capacity}")
            elif transaction['type'] == 'order':
                order = graph['orders'][transaction['destination']]['order']
                print(f"Day {day}: Order ID {order.customer.id} fulfilled with {transaction['quantity']} from Tank {transaction['source']}.")
            day_data["movements"].append({
                "connectionId": transaction['source'],
                "amount": transaction['quantity']
            })
    
    # Planificarea transporturilor
    for refinery_id, refinery_data in graph['refineries'].items():
        refinery = refinery_data['node']
        sorted_connections = sorted(
            refinery_data['connections'],
            key=lambda conn: (calculate_costs(conn, refinery.max_output)[0], conn.distance)
        )
        for connection in sorted_connections:
            tank_id = connection.to_id
            if tank_id in graph['tanks']:
                tank = graph['tanks'][tank_id]['node']
                available_space = tank.max_capacity - tank.capacity
                quantity = min(refinery.max_output, available_space)
                distance_cost, co2_emissions = calculate_costs(connection, quantity)

                # Verificăm cerințele clienților din viitor
                upcoming_demands = []
                for order in graph['orders'].values():
                    for demand in order['order'].demands:  # Presupunând că cererile sunt stocate aici
                        if demand.start_delivery_day <= day + connection.lead_time_days <= demand.end_delivery_day:
                            upcoming_demands.append(demand)

                if upcoming_demands:
                    # Programăm transportul dacă se poate îndeplini cererea
                    arrival_day = day + connection.lead_time_days
                    if arrival_day < DAYS:
                        transactions[arrival_day].append({
                            'type': 'tank',
                            'source': connection.id,
                            'destination': tank_id,
                            'quantity': quantity
                        })
                        print(f"Day {day}: Scheduled {quantity} from Refinery {refinery.name} to Tank {tank.name} (arrives on Day {arrival_day}). Cost: {distance_cost}, CO2: {co2_emissions:.2f}")

    # Procesăm comenzile clienților
    for tank_id, tank_data in graph['tanks'].items():
        tank = tank_data['node']
        sorted_order_connections = sorted(
            tank_data['connections']['to_orders'],
            key=lambda conn: (calculate_costs(conn, tank.capacity)[0], conn.distance)
        )
        for order_connection in sorted_order_connections:
            order_id = order_connection.to_id
            if order_id in graph['orders']:
                order = graph['orders'][order_id]['order']
                for demand in sorted(order.demands, key=lambda d: d.end_delivery_day):
                    if day >= demand.start_delivery_day and day <= demand.end_delivery_day:
                        if tank.capacity >= demand.quantity:
                            transactions[day].append({
                                'type': 'order',
                                'source': tank_id,
                                'destination': order_id,
                                'quantity': demand.quantity
                            })
                            tank.capacity -= demand.quantity
                            distance_cost, co2_emissions = calculate_costs(order_connection, demand.quantity)
                            print(f"Day {day}: Scheduled {demand.quantity} from Tank {tank.name} to Order ID {order.customer.id}. Cost: {distance_cost}, CO2: {co2_emissions:.2f}")
                            day_data["movements"].append({
                                "connectionId": tank_id,
                                "amount": demand.quantity
                            })
                            break
    
    # Salvăm datele zilei curente
    with open(f"day_{day}.json", "w") as f:
        json.dump(day_data, f, indent=2)

# Rulăm simularea pentru fiecare zi
for day in range(DAYS):
    simulate_day(day, graph, transactions)

# Finalizarea transporturilor rămase
for day in range(DAYS):
    if day in transactions:
        print(f"Finalizing transactions on day {day}")
        for transaction in transactions[day]:
            if transaction['type'] == 'tank':
                tank = graph['tanks'][transaction['destination']]['node']
                tank.capacity += transaction['quantity']
                print(f"Finalized {transaction['quantity']} to Tank {tank.name}.")
            elif transaction['type'] == 'order':
                order = graph['orders'][transaction['destination']]['order']
                print(f"Finalized Order ID {order.customer.id} with {transaction['quantity']} from Tank {transaction['source']}.")
