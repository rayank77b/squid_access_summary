# squid_access_summary
squid log access.log summary


to use:

tail -f /var/log/squid/access.log  | squid_access_summary.py


cat /var/log/squid/access.log  | squid_access_summary.py


zcat /var/log/squid/access.log.2.gz  | squid_access_summary.py
