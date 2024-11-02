import pandas as pd

def create_clase():
    # Define the Tank class
    class Tank:
        def __init__(self, id, name, capacity, max_input, max_output, overflow_penalty, underflow_penalty,
                    over_input_penalty, over_output_penalty, initial_stock, node_type):
            self.id = id
            self.name = name
            self.capacity = initial_stock
            self.max_input = max_input
            self.max_output = max_output
            self.overflow_penalty = overflow_penalty
            self.underflow_penalty = underflow_penalty
            self.over_input_penalty = over_input_penalty
            self.over_output_penalty = over_output_penalty
            self.max_capacity = capacity
            self.node_type = node_type

        def __repr__(self):
            return f"Tank(id={self.id}, name={self.name}, capacity={self.capacity})"

    # Define the Connection class
    class Connection:
        def __init__(self, id, from_id, to_id, distance, lead_time_days, connection_type, max_capacity):
            self.id = id
            self.from_id = from_id
            self.to_id = to_id
            self.distance = distance
            self.lead_time_days = lead_time_days
            self.connection_type = connection_type
            self.max_capacity = max_capacity

        def __repr__(self):
            return f"Connection(id={self.id}, from_id={self.from_id}, to_id={self.to_id}, distance={self.distance})"

    # Define the Customer class
    class Customer:
        def __init__(self, id, name, max_input, over_input_penalty, late_delivery_penalty, early_delivery_penalty, node_type):
            self.id = id
            self.name = name
            self.max_input = max_input
            self.over_input_penalty = over_input_penalty
            self.late_delivery_penalty = late_delivery_penalty
            self.early_delivery_penalty = early_delivery_penalty
            self.node_type = node_type

        def __repr__(self):
            return f"Customer(id={self.id}, name={self.name}, max_input={self.max_input})"

    # Define the Demand class
    class Demand:
        def __init__(self, id, customer_id, quantity, post_day, start_delivery_day, end_delivery_day):
            self.id = id
            self.customer_id = customer_id
            self.quantity = quantity
            self.post_day = post_day
            self.start_delivery_day = start_delivery_day
            self.end_delivery_day = end_delivery_day

        def __repr__(self):
            return f"Demand(id={self.id}, customer_id={self.customer_id}, quantity={self.quantity})"

    # Define the Order class
    class Order:
        def __init__(self, customer, demands):
            self.customer = customer
            self.demands = demands

        def __repr__(self):
            return f"Order(customer={self.customer}, demands={self.demands})"

    # Define the Refinery class
    class Refinery:
        def __init__(self, id, name, capacity, max_output, production, overflow_penalty, underflow_penalty,
                    over_output_penalty, production_cost, production_co2, initial_stock, node_type):
            self.id = id
            self.name = name
            self.capacity = initial_stock
            self.max_output = max_output
            self.production = production
            self.overflow_penalty = overflow_penalty
            self.underflow_penalty = underflow_penalty
            self.over_output_penalty = over_output_penalty
            self.production_cost = production_cost
            self.production_co2 = production_co2
            self.max_capacity = capacity
            self.node_type = node_type

        def __repr__(self):
            return f"Refinery(id={self.id}, name={self.name}, capacity={self.capacity})"

    # Load data
    tanks_df = pd.read_csv('tanks.csv', delimiter=';')
    connections_df = pd.read_csv('connections.csv', delimiter=';')
    customers_df = pd.read_csv('customers.csv', delimiter=';')
    demands_df = pd.read_csv('demands.csv', delimiter=';')
    refineries_df = pd.read_csv('refineries.csv', delimiter=';')

    # Create nodes
    tanks = {row['id']: Tank(**row) for _, row in tanks_df.iterrows()}
    connections = [Connection(**row) for _, row in connections_df.iterrows()]
    customers = {row['id']: Customer(**row) for _, row in customers_df.iterrows()}
    demands = [Demand(**row) for _, row in demands_df.iterrows()]
    refineries = {row['id']: Refinery(**row) for _, row in refineries_df.iterrows()}

    # Create orders
    orders = {}
    for customer_id, customer in customers.items():
        customer_demands = [d for d in demands if d.customer_id == customer_id]
        orders[customer_id] = Order(customer=customer, demands=customer_demands)

    # Create the graph structure
    graph = {'refineries': {}, 'tanks': {}, 'orders': {}}

    # Populate refineries in graph
    for refinery_id, refinery in refineries.items():
        graph['refineries'][refinery_id] = {
            'node': refinery,
            'connections': [conn for conn in connections if conn.from_id == refinery_id]
        }

    # Populate tanks in graph
    for tank_id, tank in tanks.items():
        graph['tanks'][tank_id] = {
            'node': tank,
            'connections': {
                'from_refineries': [conn for conn in connections if conn.to_id == tank_id and conn.from_id in refineries],
                'to_orders': [conn for conn in connections if conn.from_id == tank_id and conn.to_id in orders]
            }
        }

    # Populate orders in graph
    for customer_id, order in orders.items():
        graph['orders'][customer_id] = {
            'order': order,
            'connections': [conn for conn in connections if conn.to_id == customer_id]
        }

    return graph
