#!/usr/bin/env python3
# encoding: utf-8
'''
Gandi v5 LiveDNS - DynDNS Update via REST API and CURL/requests

@author: cave
License GPLv3
https://www.gnu.org/licenses/gpl-3.0.html

Created on 13 Aug 2017
https://api.gandi.net/docs/
https://api.gandi.net/docs/reference/#RESTful-interface -> https://api.gandi.net/v5/
'''

import requests, json
import config
import argparse


def _read_json(u):
    try:
        return u.json()
    except requests.exceptions.JSONDecodeError:
        print(
            'Error: HTTP Status Code', u.status_code,
            'when trying to get IP from subdomain', config.subdomains[0],
            'response', u.text,
        )
        exit(1)


def get_dynip(ifconfig_provider):
    ''' find out own IPv4 at home <-- this is the dynamic IP which changes more or less frequently
    similar to curl ifconfig.me/ip, see example.config.py for details to ifconfig providers 
    ''' 
    r = requests.get(ifconfig_provider)
    ip = r.text.strip('\n')
    print('Checking dynamic IP: ' , ip)
    return ip


def get_dnsip():
    ''' find out IP from first Subdomain DNS-Record
    Get details of the record with name (aka. rrset_name) and type (aka. rrset_type) in domain (aka. fqdn)
    GET /livedns/domains/{fqdn}/records/{rrset_name}/{rrset_type}:
    
    The first subdomain from config.subdomain will be used to get   
    the actual DNS Record IP
    '''

    url = config.api_endpoint + '/livedns/domains/' + config.domain + '/records/' + config.subdomains[0] + '/A'
    headers = {"Authorization": "Bearer " + config.api_secret}
    u = requests.get(url, headers=headers)
    json_object = _read_json(u)

    if u.status_code == 200:
        dnsip = json_object['rrset_values'][0]
        print('Checking IP from DNS Record' , config.subdomains[0], ':', dnsip)
        return dnsip
    else:
        print(
            'Error: HTTP Status Code', u.status_code,
            'when trying to get IP from subdomain', config.subdomains[0],
            'message/response', json_object['message'] if json_object.get('message') else u.text,
        )
        exit()


def update_records(dynIP, subdomain):
    ''' update DNS Records for Subdomains 
        Change the "NAME"/"TYPE" record from the zone UUID
        PUT /zones/<UUID>/records/<NAME>/<TYPE>:
        curl -X PUT -H "Content-Type: application/json" \
                    -H 'X-Api-Key: XXX' \
                    -d '{"rrset_ttl": 10800,
                         "rrset_values": ["<VALUE>"]}' \
                    https://dns.gandi.net/api/v5/zones/<UUID>/records/<NAME>/<TYPE>
    '''
    url = config.api_endpoint + '/livedns/domains/' + config.domain + '/records/' + subdomain + '/A'
    payload = {"rrset_ttl": config.ttl, "rrset_values": [dynIP]}
    headers = {"Content-Type": "application/json", "Authorization": "Bearer " + config.api_secret}
    u = requests.put(url, data=json.dumps(payload), headers=headers)
    json_object = _read_json(u)

    if u.status_code == 201:
        print('Status Code:', u.status_code, ',', json_object['message'], ', IP updated for', subdomain)
        return True
    else:
        print(
            'Error: HTTP Status Code ', u.status_code,
            'when trying to update IP from subdomain', subdomain,
            'message/response', json_object['message'] if json_object.get('message') else u.text,
        )
        exit()



def main(force_update, verbosity):

    if verbosity:
        print("verbosity turned on - not implemented by now")
   
    #compare dynIP and DNS IP 
    dynIP = get_dynip(config.ifconfig)
    dnsIP = get_dnsip()

    if force_update:
        print("Going to update/create the DNS Records for the subdomains")
        for sub in config.subdomains:
            update_records(dynIP, sub)
    else:
        if dynIP == dnsIP:
            print("IP Address Match - no further action")
        else:
            print("IP Address Mismatch - going to update the DNS Records for the subdomains with new IP", dynIP)
            for sub in config.subdomains:
                update_records(dynIP, sub)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-v', '--verbose', help="increase output verbosity", action="store_true")
    parser.add_argument('-f', '--force', help="force an update/create", action="store_true")
    args = parser.parse_args()
        
        
    main(args.force, args.verbose)





    
