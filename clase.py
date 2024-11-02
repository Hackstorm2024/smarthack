import pandas as pd

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
df = pd.read_csv('tanks.csv', delimiter=';')

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


##############################################


# Definim clasa Connection
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

# Citim fișierul CSV
df = pd.read_csv('connections.csv', delimiter=';')

# Creăm o listă de obiecte Connection
connections = []
for _, row in df.iterrows():
    connection = Connection(
        id=row['id'],
        from_id=row['from_id'],
        to_id=row['to_id'],
        distance=row['distance'],
        lead_time_days=row['lead_time_days'],
        connection_type=row['connection_type'],
        max_capacity=row['max_capacity']
    )
    connections.append(connection)


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
df = pd.read_csv('customers.csv', delimiter=';')

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
df = pd.read_csv('demands.csv', delimiter=';')

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
df = pd.read_csv('rafineries.csv', delimiter=';')

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


##############################################


# Definim clasa Team
class Team:
    def __init__(self, id, color, name, api_key, internal_use):
        self.id = id
        self.color = color
        self.name = name
        self.api_key = api_key
        self.internal_use = internal_use

    def __repr__(self):
        return f"Team(id={self.id}, name={self.name}, color={self.color})"

# Citim fișierul CSV
df = pd.read_csv('teams.csv', delimiter=';')

# Creăm o listă de obiecte Team
teams = []
for _, row in df.iterrows():
    team = Team(
        id=row['id'],
        color=row['color'],
        name=row['name'],
        api_key=row['api_key'],
        internal_use=row['internal_use']
    )
    teams.append(team)
