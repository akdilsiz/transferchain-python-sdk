# Import the TransferChain class from the SDK
from transferchain.client import TransferChain

# Initialize TransferChain
tc = TransferChain()

# When the SDK is initialized for the first time, creating a master user for that SDK is facilitated by using the 'add_master_user' operation.
# Example: Create a Master User
result_add_master_user = tc.add_master_user()
master_user = result_add_master_user.data
print(f"Master User created: {master_user.id}")