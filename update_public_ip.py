#!/usr/bin/env python3
import requests
import os
import json
ip = requests.get('https://checkip.amazonaws.com').text.strip()
token = os.getenv('API_TOKEN')
zone = 'managedDNSZonehere'
record_name = 'dyndns.example.com'
current_ip = requests.get('https://checkip.amazonaws.com').text.strip()
uri = "https://api.cloudflare.com/client/v4/"

# Build the request headers once. These headers will be used throughout the script.
headers = {
    "Authorization": "Bearer " + token,
    "Content-Type": "application/json",
    }
## This block verifies that your API key is valid.
## If not, the script will terminate.
verify_uri = uri + "tokens/verify"
r = requests.get(uri,data={},headers=headers)
if not r.ok:
    print("Invalid api token")
    exit()

# Retrieves the domain's zone identifier based on the zone name. If the identifier is not found, the script will terminate.

zone_uri = uri + "v4/zones?name={}".format(zone)
r = requests.get(zone_uri,data={},headers=headers)
zone_id = r.json()['result'][0]['id']
if not zone_id:
    print("Couldn't find zone_id, exiting")
    exit()

# Retrieve the existing DNS record details from Cloudflare.
dns_uri = uri + "zones/{}/dns_records?name={}".format(zone_id,record_name)
r = requests.get(dns_uri,data={},headers=headers)

old_ip = r.json()['result'][0]['content']
record_type = r.json()['result'][0]['type']
record_id = r.json()['result'][0]['id']
record_ttl = r.json()['result'][0]['ttl']
is_record_proxied = r.json()['result'][0]['proxied']

# update Dynamic DNS Record
if old_ip == current_ip:
    print("Old_ip equals current IP. Nothing to do. *flies away*")
    exit()

update_uri = uri + "v4/zones/{}/dns_records/{}".format(zone_id,record_id)

data = {
    "content": current_ip,
    "name": record_name,
    "proxied": is_record_proxied,
    "type": record_type,
    "ttl": record_ttl
}
r = requests.put(update_uri,headers=headers,data=json.dumps(data))
print(r.json())
if r.ok: 
    print("Updated old IPv4 {} to new IPv4 {}".format(old_ip,current_ip))
