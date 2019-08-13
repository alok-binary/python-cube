from __future__ import print_function
import olap.xmla.xmla as xmla
import requests
import numpy as np
import pandas as pd
import time
import urllib3
#urllib3.disable_warnings()

print('checkpoint 1')

username = '' #please add a username here or get it from a configuration file
password = '' #please add a password here or get it from a configuration file
endpoint = "https://iccube.regentmarkets.com/xmla"

print('checkpoint 2')

p = xmla.XMLAProvider()
print('p:',p)

print('checkpoint 3')

# mondrian
c = p.connect(location=endpoint,
              username=username, password=password, sslverify=False)

print('checkpoint 4')

print('now sleeping...')
time.sleep(3)
print('done sleeping!')
print('c_dict:',c.__dict__)

print('checkpoint 5')

# to analysis services (if iis proxies requests at /olap/msmdpump.dll)
# you will need a valid kerberos principal of course
# c = p.connect(location="https://my-as-server/olap/msmdpump.dll",
#               sslverify="/path/to/my/as-servers-ca-cert.pem")
# to icCube
# c = p.connect(location="http://localhost:8282/icCube/xmla", username="demo",
#               password="demo")
# getting info about provided data

print(c.getDatasources())

print('checkpoint 6')

#print(c.getMDSchemaCubes())
# for ssas a catalog is needed, so the call would be like
# get a catalogname from a call to c.getDBSchemaCatalogs()
# c.getMDSchemaCubes(properties={"Catalog":"a catalogname"})
# execute a MDX (working against the foodmart sample catalog of mondrian)

cmd = """select

        [Contract Payout USD DER].[Contract Payout USD DER] on 0,
        
        non empty [Client ].[Country].members on 1,
        [Contract Underlying].[Contract Underlying] on 2
        
        from [Bet]
"""

print('checkpoint 7')

#res = c.Execute(cmd, Catalog="cube_closed_contracts")
res = c.Execute(cmd, Catalog='cube_closed_contracts')

print('checkpoint 8')

#return only the Value property from the cells
print('---')
print(res.getSlice(properties="Value"))
# or two props
#print(res.getSlice(properties=["Value", "FmtValue"]))
print('---')

print('checkpoint 9')

# to return some subcube from the result you can
# return all

print('result.getSlice():')
print(res.getSlice())

print('checkpoint 10')

print('type(result):')
print(type(res))

print('checkpoint 11')

print('type(result.getSlice():')
print(type(res.getSlice()))

print('checkpoint 12')

# carve out the 4th column
#res.getSlice(Axis0=3)
# same as above, SlicerAxis is ignored
#res.getSlice(Axis0=3, SlicerAxis=0)
# return the data sliced at the 2nd and 3rd row
#res.getSlice(Axis1=[1,2])
# return the data sliced at the 2nd and 3rd row and at the 4th column
#res.getSlice(Axis0=3, Axis1=[1,2])
