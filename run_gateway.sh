docker run --rm -it --name gateway \
  --cap-add=NET_ADMIN \
  --cap-add=SYS_ADMIN \
  --sysctl net.ipv4.ip_forward=1 \
  --net client_net \
  --ip 192.168.10.200 \
  --network-alias gateway \
  my-gateway-image

docker network connect --ip 192.168.20.200 server_net gateway