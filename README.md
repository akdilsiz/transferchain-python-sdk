# Transferchain SDK


The Transferchain SDK is a Python library that provides easy integration with the Transferchain platform. With this SDK, you can interact with Transferchain's blockchain technology to create and manage user accounts, perform transactions, and more. To get started, you need to define several environment variables, and this README will guide you through the process.


### SDK and User Documentation
SDK Docs [https://transferchain-python-sdk.readthedocs.io/](https://transferchain-python-sdk.readthedocs.io/)  
User Docs [https://docs.transferchain.io/](https://docs.transferchain.io/)


## Getting Started

### Prerequisites

Before using the Transferchain SDK, make sure you have the following prerequisites in place:

- Python 3.6 or later installed on your system.
- Access to the Transferchain platform and API credentials (API token and secret).

### Installation

You can install the SDK via pip:

```bash
pip install transferchain-python-sdk
```
### Environment Variables
To use this SDK, add the following environment variables to your environment:

- `TRANSFERCHAIN_USER_ID (int)`: Your account's user ID.
- `TRANSFERCHAIN_API_TOKEN (str)`: Your Transferchain API token.
- `TRANSFERCHAIN_API_SECRET (str)`: Your Transferchain API secret.
- `TRANSFERCHAIN_WALLET_UUID (str)`: An optional value, a random UUID or your current wallet UUID.
- `TRANSFERCHAIN_MNEMONICS (str)`: Your account mnemonics.

### Example Usages
Here are some example usages of the Transferchain SDK:

##### Create a Master User
```python
from transferchain.client import TransferChain

tc = TransferChain()
result = tc.add_master_user()
user = result.data
```

#### Restore a Master User
```python
from transferchain.client import TransferChain

tc = TransferChain()
result = tc.restore_master_user()
```
#### Add a User
```python
from transferchain.client import TransferChain

tc = TransferChain()
result = tc.add_master_user()
user_result = tc.add_user()
user_object = user_result.data
```
#### Get a User
```python
from transferchain.client import TransferChain

tc = TransferChain()
result = tc.add_master_user()
user_result = tc.add_user()
user_object = user_result.data
user = tc.get_user(user_object.id)
```
#### Load Users From DB
```python
from transferchain.client import TransferChain

tc = TransferChain()
tc.load_users()
```
#### Save User
```python
from transferchain.client import TransferChain

tc = TransferChain()
result = tc.add_master_user()
user_result = tc.add_user()
user_object = user_result.data
tc.save_user(user_object.id, user_object)
```
For more examples and detailed usage instructions, don't forget to check out the `transferchain.client` module.

#### Important Note
Please note that the time it takes for a transaction to be broadcast on the blockchain is approximately 2 seconds. Ensure that you handle this delay appropriately in your application.

For further information and updates, please visit the Transferchain Python SDK GitHub repository.

If you encounter any issues or have questions, feel free to reach out to our support team.

### LICENSE
transferchain-go-sdk is licensed under the MIT. See [LICENSE](./LICENSE) for the full license text.
