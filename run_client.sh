
count=1
for i in $(seq 2 51); do
  docker run --rm \
    --name client$count \
    --net py-mtls_client_net \
    --ip 192.168.10.$i \
    --cap-add=NET_ADMIN \
    -e CLIENT_NAME=client$count \
    my-client-image
  count=$((count + 1))

done

# docker run -it --rm --name client3 --net py-mtls_client_net --ip 192.168.10.3 --cap-add=NET_ADMIN -e CLIENT_NAME=client3 my-client-image