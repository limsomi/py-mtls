#!/bin/bash

echo "[DEPRECATED] use the Makefile"
exit 0

BOLD=$(tput bold)
CLEAR=$(tput sgr0)

BASE_DIR=$(readlink -f $0 | xargs dirname | xargs dirname)
iterate=($BASE_DIR/ssl/server/ $BASE_DIR/ssl/client/)
for dir in "${iterate[@]}"; do
  [[ ! -d "$dir" ]] && mkdir -p "$dir" \
  && echo -e "${BOLD}directory '$dir' was created ${CLEAR}"
done

ssl="./ssl"
client="$ssl/client"
server="$ssl/server"

echo -e "${BOLD}Generating RSA AES-256 Private Key for Root Certificate Authority${CLEAR}"
openssl genrsa -aes256 -out $ssl/CA.key 4096

echo -e "${BOLD}Generating Certificate for Root Certificate Authority${CLEAR}"
openssl req -x509 -new -nodes -key $ssl/CA.key -sha256 -days 1825 -out $ssl/CA.pem

echo -e "${BOLD}Generating RSA Private Key for Server Certificate${CLEAR}"
openssl genrsa -out $server/server.key 4096

echo -e "${BOLD}Generating Certificate Signing Request for Server Certificate${CLEAR}"
openssl req -new -key $server/server.key -out $server/server.csr

echo -e "${BOLD}Generating Certificate for Server Certificate${CLEAR}"
openssl x509 -req -in $server/server.csr -CA $ssl/CA.pem -CAkey $ssl/CA.key -CAcreateserial -out $server/server.crt -days 1825 -sha256

echo -e "${BOLD}Generating RSA Private Key for Client Certificate${CLEAR}"
openssl genrsa -out $client/client.key 4096

echo -e "${BOLD}Generating Certificate Signing Request for Client Certificate${CLEAR}"
openssl req -new -key $client/client.key -out $client/client.csr

echo -e "${BOLD}Generating Certificate for Client Certificate${CLEAR}"
openssl x509 -req -in $client/client.csr -CA $ssl/CA.pem -CAkey $ssl/CA.key -CAcreateserial -out $client/client.crt -days 1825 -sha256

echo -e "${BOLD}Generating PEM file for Client${CLEAR}"
openssl rsa -in ${client}/client.key -out ${client}/nopassword.key
cat ${client}/nopassword.key > ${client}/client.pem
cat ${client}/client.crt >> ${client}/client.pem
cat ${ssl}/CA.pem >> ${client}/client.pem

echo -e "${BOLD}Generating PEM file for Server${CLEAR}"
openssl rsa -in ${server}/server.key -out ${server}/nopassword.key
cat ${server}/nopassword.key > ${server}/server.pem
cat ${server}/server.crt >> ${server}/server.pem
cat ${ssl}/CA.pem >> ${server}/server.pem

echo "Done!"

openssl genrsa -out ssl/foo/foo.key 4096
openssl req -new -key ssl/foo/foo.key -out $client/client.csr
openssl x509 -req -in ssl/foo/foo.csr -CA ssl/CA.pem -CAkey ssl/CA.key -CAcreateserial -out ssl/foo/foo.crt -days 1825 -sha256
openssl rsa -in ssl/foo/foo.key -out ssl/foo/nopassword.key
cat ssl/foo/nopassword.key > ssl/foo/server.pem
cat ssl/foo/server.crt >> ssl/foo/server.pem
cat ssl/foo/CA.pem >> ssl/foo/server.pem