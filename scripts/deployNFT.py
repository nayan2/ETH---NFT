from brownie import CarLease
import os
from scripts.helpful_scripts import get_account, create_metadata, get_image_URI

sample_token_uri = "https://ipfs.io/ipfs/Qmd9MCGtdVz2miNumBHDbvj8bigSgTwnr4SbyH6DNnpWdt?filename=0-PUG.json"
OPENSEA_URL = 'https://testnets.opensea.io/assets/goerli/{}/{}'

# def main():
#     account = get_account()
#     car_lease = CarLease.deploy({ 'from': account })
#     tx = car_lease.safeMint(account, sample_token_uri, { 'from': account })
#     tx.wait(1)
#     print(f'The address is - {car_lease.address} \\ {car_lease.tokenIdCounter()}') 

def main():
    account = get_account()
    car_lease = CarLease.deploy({ 'from': account })
    print(car_lease.address)
    
    for path in os.listdir('./img'):
        car_lease = CarLease[-1]
        
        image_name = path.split('.')[0]
        create_metadata(image_name)
        image_URI = get_image_URI(image_name)
        print(image_URI)
        
        # Mint the token
        tx = car_lease.safeMint(account, image_URI, {"from": account})
        tx.wait(1)
        print(OPENSEA_URL.format(car_lease.address, car_lease.tokenIdCounter() - 1))
        
    