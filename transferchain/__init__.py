'''
# Transferchain SDK

 - Github -> [https://github.com/TransferChain/transferchain-python-sdk](https://github.com/TransferChain/transferchain-python-sdk)

To use this SDK, add the following definitions to your env.
        TRANSFERCHAIN_USER_ID (int): Account user id

        TRANSFERCHAIN_API_TOKEN (str): Transferchain api token

        TRANSFERCHAIN_API_SECRET (str): Transferchain api secret

        TRANSFERCHAIN_WALLET_UUID (str): optinal value, random uuid or current
        wallet uuid

        TRANSFERCHAIN_MNEMONICS (str): Account mnemonics

        TRANSFERCHAIN_DEBUG (bool): Transferchain testing environment

## Example Usages;
Important!

        The time it takes for a transaction to be broadcast on the blockchain
        is 2 seconds.

#### Create master user

```
        from transferchain.client import TransferChain
        tc = TransferChain()
        result = tc.add_master_user()
        user = result.data
```

#### Restore master user
```
        from transferchain.client import TransferChain
        tc = TransferChain()
        result = tc.restore_master_user()
```

#### Add user
```
        from transferchain.client import TransferChain
        tc = TransferChain()
        result = tc.add_master_user()
        user_result = tc.add_user()
        user_object = user_result.data
```

#### Get user
```
        from transferchain.client import TransferChain
        tc = TransferChain()
        result = tc.add_master_user()
        user_result = tc.add_user()
        user_object = user_result.data
        user = tc.get_user(user_object.id)
```

#### Load users
```
        from transferchain.client import TransferChain
        tc = TransferChain()
        tc.load_users()
```

#### Save user
```
        from transferchain.client import TransferChain
        tc = TransferChain()
        result = tc.add_master_user()
        user_result = tc.add_user()
        user_object = user_result.data
        tc.save_user(user_object.id, user_object)
```

!! Don't forget to check out the `transferchain.client` for more examples.

'''
