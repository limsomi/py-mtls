## PoC mTLS

```bash
user@node:$ bin/mtls.sh
directory 'ssl/server/' was created
directory 'ssl/client/' was created
Generating RSA AES-256 Private Key for Root Certificate Authority
Generating RSA private key, 4096 bit long modulus
.......................................................................................................................................................................................++++
............................................................++++
e is 65537 (0x10001)
Enter pass phrase for ./ssl/CA.key:
Verifying - Enter pass phrase for ./ssl/CA.key:
Generating Certificate for Root Certificate Authority
Enter pass phrase for ./ssl/CA.key:
You are about to be asked to enter information that will be incorporated
into your certificate request.
What you are about to enter is what is called a Distinguished Name or a DN.
There are quite a few fields but you can leave some blank
For some fields there will be a default value,
If you enter '.', the field will be left blank.
-----
Country Name (2 letter code) []:ES
State or Province Name (full name) []:Madrid
Locality Name (eg, city) []:
Organization Name (eg, company) []:Python CA
Organizational Unit Name (eg, section) []:
Common Name (eg, fully qualified host name) []:
Email Address []:
Generating RSA Private Key for Server Certificate
Generating RSA private key, 4096 bit long modulus
...........................++++
..............................................................................++++
e is 65537 (0x10001)
Generating Certificate Signing Request for Server Certificate
You are about to be asked to enter information that will be incorporated
into your certificate request.
What you are about to enter is what is called a Distinguished Name or a DN.
There are quite a few fields but you can leave some blank
For some fields there will be a default value,
If you enter '.', the field will be left blank.
-----
Country Name (2 letter code) []:ES
State or Province Name (full name) []:Madrid
Locality Name (eg, city) []:
Organization Name (eg, company) []:Python CA
Organizational Unit Name (eg, section) []:Python Server
Common Name (eg, fully qualified host name) []:
Email Address []:

Please enter the following 'extra' attributes
to be sent with your certificate request
A challenge password []:
Generating Certificate for Server Certificate
Signature ok
subject=/C=ES/ST=Madrid/O=Python CA/OU=Python Server
Getting CA Private Key
Enter pass phrase for ./ssl/CA.key:
Generating RSA Private Key for Client Certificate
Generating RSA private key, 4096 bit long modulus
...........................................................................................................++++
.....................................................................................................................................++++
e is 65537 (0x10001)
Generating Certificate Signing Request for Client Certificate
You are about to be asked to enter information that will be incorporated
into your certificate request.
What you are about to enter is what is called a Distinguished Name or a DN.
There are quite a few fields but you can leave some blank
For some fields there will be a default value,
If you enter '.', the field will be left blank.
-----
Country Name (2 letter code) []:ES
State or Province Name (full name) []:Madrid
Locality Name (eg, city) []:
Organization Name (eg, company) []:Python CA
Organizational Unit Name (eg, section) []:Python Client
Common Name (eg, fully qualified host name) []:
Email Address []:

Please enter the following 'extra' attributes
to be sent with your certificate request
A challenge password []:
Generating Certificate for Client Certificate
Signature ok
subject=/C=ES/ST=Madrid/O=Python CA/OU=Python Client
Getting CA Private Key
Enter pass phrase for ./ssl/CA.key:
Generating PEM file for Client
writing RSA key
Generating PEM file for Server
writing RSA key
Done!

user@node:$ openssl verify -verbose -CAfile ssl/CA.pem ssl/server/server.crt
ssl/server/server.crt: OK

user@node:$ openssl verify -verbose -CAfile ssl/CA.pem ssl/client/client.crt
ssl/client/client.crt: OK

# SERVER HTTP with SSL
user@node:$ SSLKEYLOGFILE=~/sslkeylog.log curl https://localhost:1234 -k
```