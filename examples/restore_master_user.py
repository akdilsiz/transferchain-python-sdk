# Import the TransferChain class from the SDK
from transferchain.client import TransferChain

# Initialize TransferChain
tc = TransferChain()

# It writes the addresses of the master and user in the blockchain to the SDK database using the mnemonics found in the environment, and returns all transactions found to the SDK user.
# Example: Restore a Master User
result_restore_master_user = tc.restore_master_user()
restored_master_user = result_restore_master_user.data
print(f"Master User restored: {restored_master_user}")