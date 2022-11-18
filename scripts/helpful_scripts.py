from brownie import accounts, config, network
from pathlib import Path
import requests
import random
import json
from metadata.sample_metadata import metadata_template

LOCAL_BLOCKCHAIN_ENVIRONMENTS = ["hardhat", "development", "ganache", "mainnet-fork"]

image_to_URI_map = {
    'development': {
        'BilBoyd-Car1': 'https://ipfs.io/ipfs/QmU5wYjLxLRzGcfH2FkXKw1MjbmqYjwUdGWyVJh7kSWPBR?filename=BilBoyd-Car1.json',
        'BilBoyd-Car2': 'https://ipfs.io/ipfs/QmSL8ZpdEMiLSDbabN3M3wbmBVXee2F9Hcodpv6es7Cj1T?filename=BilBoyd-Car2.json',
        'BilBoyd-Car3': 'https://ipfs.io/ipfs/QmWhqMNbW4y3js4rbTGAzZpwXSvvn5CN8emLy7bMgEyS5t?filename=BilBoyd-Car3.json'
    }, 
    'goerli': {
        'BilBoyd-Car1': 'https://ipfs.io/ipfs/QmQvHYsVXHx85eEWVeVzVoLsnURKmFapHze4HrRDy2GJMb?filename=BilBoyd-Car1.json',
        'BilBoyd-Car2': 'https://ipfs.io/ipfs/Qmd1CMvZnkW9ZUQ86SRofnQvDAv2XYRJiMt2u6VBfAzCkU?filename=BilBoyd-Car2.json',
        'BilBoyd-Car3': 'https://ipfs.io/ipfs/QmcuEbQmmPqL7Erq9saRu8o8D7ruLUShx5PqGkQVFMvKE4?filename=BilBoyd-Car3.json'
    }
}

def get_image_URI(image_name: str):
    return image_to_URI_map[network.show_active()][image_name]

def get_account(index=None, id=None):
    if index:
        return accounts[index]
    if network.show_active() in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        return accounts[0]
    if id:
        return accounts.load(id)
    return accounts.add(config['wallets']['pr-key'])

def create_metadata(image_name: str):
    metadata_file_name = (f"./metadata/{network.show_active()}/{image_name}.json")
    collectible_metadata = metadata_template
    if Path(metadata_file_name).exists():
        print(f"{metadata_file_name} already exists! Delete it to overwrite")
    else:
        print(f"Creating Metadata file: {metadata_file_name}")
        collectible_metadata["name"] = image_name
        collectible_metadata["description"] = f"{image_name} - A nice car to lease by BilBoyd!"
        image_path = f"./img/{image_name}.jpg"
        image_uri = upload_to_ipfs(image_path)
        
        collectible_metadata["image"] = image_uri
        collectible_metadata["attributes"] = generate_attributes(image_name)
        with open(metadata_file_name, "w") as file:
            json.dump(collectible_metadata, file)
        upload_to_ipfs(metadata_file_name)

def generate_attributes(image_name: str):
    colors = ['red', 'yellow', 'white', 'brown']
    models = ['MCG BMW Alpina B10', 'MCG BMW Alpina B11', 'MCG BMW Alpina B12', 'MCG BMW Alpina B13']
    matriculation_years = [1998, 1992, 1993, 1996]
    org_values = ['20000 NOK', '200000 NOK', '40000 NOK', '90000 NOK']
    
    return [
        { 'trait_type': 'model', 'value': random.choice(models) },
        { 'trait_type': 'colour', 'value': random.choice(colors) }, 
        { 'trait_type': 'matriculation_year', 'value': random.choice(matriculation_years) },
        { 'trait_type': 'org_value', 'value': random.choice(org_values) }
    ]

def upload_to_ipfs(filepath):
    with Path(filepath).open("rb") as fp:
        file_binary = fp.read()
        ipfs_url = "http://127.0.0.1:5001"
        endpoint = "/api/v0/add"
        response = requests.post(ipfs_url + endpoint, files={"file": file_binary})
        ipfs_hash = response.json()["Hash"]
        # "./img/0-PUG.png" -> "0-PUG.png"
        filename = filepath.split("/")[-1:][0]
        image_uri = f"https://ipfs.io/ipfs/{ipfs_hash}?filename={filename}"
        print(image_uri)
        return image_uri