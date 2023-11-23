# Import the TransferChain class from the SDK
import os
from transferchain.client import TransferChain

# Initialize TransferChain
tc = TransferChain()

# Get TRANSFERCHAIN_USER_ID variable from env
user_id = os.environ.get('TRANSFERCHAIN_USER_ID')

# When any storage or transfer operation is desired, a user is required, and the 'get_user' method provides the necessary information related to the required user.
# Example: Get a User
user_id_to_get = user_id
user_info = tc.get_user(user_id_to_get)
print(f"User information: {user_info.id}")