# #  gateway 컨테이너 실행
# docker run -it --rm --cap-add=NET_ADMIN --name gateway --net my_spa_net --ip 192.168.100.200 my-gateway-image
# #  server 컨테이너 실행
docker run -d --cap-add=NET_ADMIN --name server1 --net server_net --ip 192.168.20.100 -e SERVER_NAME=server1 my-server-image
docker run -d --cap-add=NET_ADMIN --name server2 --net server_net --ip 192.168.20.101 -e SERVER_NAME=server2 my-server-image
docker run -d --cap-add=NET_ADMIN --name server3 --net server_net --ip 192.168.20.102 -e SERVER_NAME=server3 my-server-image


# docker run -it --cap-add=NET_ADMIN --name server2 --net server_net --ip 192.168.20.101 -e SERVER_NAME=server1 my-server-image
