from brownie import SimpleStorage
from scripts.helpful_scripts import get_account

def deploy_simple_storage():
    account = get_account()
    
    simple_storage = SimpleStorage.deploy({ 'from': account })
    stored_value = simple_storage.retrieve()
    print(stored_value)

def main():
    deploy_simple_storage()