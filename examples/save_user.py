# Import the TransferChain class from the SDK
from transferchain.client import TransferChain

# Initialize TransferChain
tc = TransferChain()

# Example: Add a User
result_add_user = tc.add_user()
added_user = result_add_user.data

# Example: Save User
tc.save_user(added_user.id, added_user)
print(f"User {added_user.id} saved.")

