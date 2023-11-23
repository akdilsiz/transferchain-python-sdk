# Import the TransferChain class from the SDK
from transferchain.client import TransferChain

# Initialize TransferChain
tc = TransferChain()

# Example: Add a User
result_add_user = tc.add_user()
added_user = result_add_user.data
print(f"User added: {added_user.id}")