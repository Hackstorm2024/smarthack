import pandas as pd
import networkx as nx

#initializam graf
G = nx.DiGraph()

# Definim clasa Tank
class Tank:
    def __init__(self, id, name, capacity, max_input, max_output, overflow_penalty, underflow_penalty,
                 over_input_penalty, over_output_penalty, initial_stock, node_type):
        self.id = id
        self.name = name
        self.capacity = capacity
        self.max_input = max_input
        self.max_output = max_output
        self.overflow_penalty = overflow_penalty
        self.underflow_penalty = underflow_penalty
        self.over_input_penalty = over_input_penalty
        self.over_output_penalty = over_output_penalty
        self.initial_stock = initial_stock
        self.node_type = node_type

    def __repr__(self):
        return f"Tank(id={self.id}, name={self.name}, capacity={self.capacity})"

# Citim fișierul CSV
df = pd.read_csv('C:/smarthack/files/tanks.csv', delimiter=';')

# Creăm o listă de obiecte Tank
tanks = []
for _, row in df.iterrows():
    tank = Tank(
        id=row['id'],
        name=row['name'],
        capacity=row['capacity'],
        max_input=row['max_input'],
        max_output=row['max_output'],
        overflow_penalty=row['overflow_penalty'],
        underflow_penalty=row['underflow_penalty'],
        over_input_penalty=row['over_input_penalty'],
        over_output_penalty=row['over_output_penalty'],
        initial_stock=row['initial_stock'],
        node_type=row['node_type']
    )
    tanks.append(tank)
    G.add_node(tank.id, type='tank', name=tank.name, capacity=tank.capacity,
               max_input=tank.max_input, max_output=tank.max_output,
               overflow_penalty=tank.overflow_penalty, underflow_penalty=tank.underflow_penalty,
               over_input_penalty=tank.over_input_penalty, over_output_penalty=tank.over_output_penalty,
               initial_stock=tank.initial_stock)

##############################################

# Definim clasa Customer
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

# Citim fișierul CSV
df = pd.read_csv('C:/smarthack/files/customers.csv', delimiter=';')

# Creăm o listă de obiecte Customer
customers = []
for _, row in df.iterrows():
    customer = Customer(
        id=row['id'],
        name=row['name'],
        max_input=row['max_input'],
        over_input_penalty=row['over_input_penalty'],
        late_delivery_penalty=row['late_delivery_penalty'],
        early_delivery_penalty=row['early_delivery_penalty'],
        node_type=row['node_type']
    )
    customers.append(customer)
    G.add_node(customer.id, type='customer', name=customer.name, max_input=customer.max_input,
               over_input_penalty=customer.over_input_penalty,
               late_delivery_penalty=customer.late_delivery_penalty,
               early_delivery_penalty=customer.early_delivery_penalty)

##############################################

# Definim clasa Refinery
class Refinery:
    
    def __init__(self, id, name, capacity, max_output, production, overflow_penalty, underflow_penalty,
                 over_output_penalty, production_cost, production_co2, initial_stock, node_type):
        self.id = id
        self.name = name
        self.capacity = capacity
        self.max_output = max_output
        self.production = production
        self.overflow_penalty = overflow_penalty
        self.underflow_penalty = underflow_penalty
        self.over_output_penalty = over_output_penalty
        self.production_cost = production_cost
        self.production_co2 = production_co2
        self.initial_stock = initial_stock
        self.node_type = node_type

    def __repr__(self):
        return f"Refinery(id={self.id}, name={self.name}, capacity={self.capacity})"

# Citim fișierul CSV
df = pd.read_csv('C:/smarthack/files/refineries.csv', delimiter=';')

# Creăm o listă de obiecte Refinery
refineries = []
for _, row in df.iterrows():
    refinery = Refinery(
        id=row['id'],
        name=row['name'],
        capacity=row['capacity'],
        max_output=row['max_output'],
        production=row['production'],
        overflow_penalty=row['overflow_penalty'],
        underflow_penalty=row['underflow_penalty'],
        over_output_penalty=row['over_output_penalty'],
        production_cost=row['production_cost'],
        production_co2=row['production_co2'],
        initial_stock=row['initial_stock'],
        node_type=row['node_type']
    )
    refineries.append(refinery)
    G.add_node(refinery.id, type='refinery', name=refinery.name, capacity=refinery.capacity,
               max_output=refinery.max_output, production=refinery.production,
               overflow_penalty=refinery.overflow_penalty, underflow_penalty=refinery.underflow_penalty,
               over_output_penalty=refinery.over_output_penalty,
               production_cost=refinery.production_cost, production_co2=refinery.production_co2,
               initial_stock=refinery.initial_stock)

# Definim clasa Connection
connections_df = pd.read_csv('C:/smarthack/files/connections.csv', delimiter=';')
for _, row in connections_df.iterrows():
    G.add_edge(row['from_id'], row['to_id'], 
               id=row['id'], 
               distance=row['distance'], 
               lead_time_days=row['lead_time_days'], 
               connection_type=row['connection_type'], 
               max_capacity=row['max_capacity'])


##############################################

# Definim clasa Demand
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

# Citim fișierul CSV
df = pd.read_csv('C:/smarthack/files/demands.csv', delimiter=';')

# Creăm o listă de obiecte Demand
demands = []
for _, row in df.iterrows():
    demand = Demand(
        id=row['id'],
        customer_id=row['customer_id'],
        quantity=row['quantity'],
        post_day=row['post_day'],
        start_delivery_day=row['start_delivery_day'],
        end_delivery_day=row['end_delivery_day']
    )
    demands.append(demand)

##############################################
