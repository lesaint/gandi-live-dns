'''
Created on 13 Aug 2017
@author: cave
Copy this file to config.py and update the settings
'''
#!/usr/bin/env python
# encoding: utf-8

'''
Get your Personal Access Token (PAT)
PAT must be recreated using the Organization Admin application.
https://admin.gandi.net/organizations/account/pat
'''
api_secret = '---my_secret_API_KEY----'

'''
Gandiv5 LiveDNS API Location
https://api.gandi.net/docs/
https://api.gandi.net/v5/
'''
api_endpoint = 'https://api.gandi.net/v5'

#your domain with the subdomains in the zone file/UUID 
domain = 'mydomain.tld'

#enter all subdomains to be updated, subdomains must already exist to be updated
subdomains = ["subdomain1", "subdomain2", "subdomain3"]

#300 seconds = 5 minutes
ttl = '300'

''' 
IP address lookup service 
run your own external IP provider:
+ https://github.com/mpolden/ipd
+ <?php $ip = $_SERVER['REMOTE_ADDR']; ?>
  <?php print $ip; ?>
e.g. 
+ https://ifconfig.co/ip
+ http://ifconfig.me/ip
+ http://whatismyip.akamai.com/
+ http://ipinfo.io/ip
+ many more ...
'''
ifconfig = 'choose_from_above_or_run_your_own'
