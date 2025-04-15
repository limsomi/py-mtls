# # 3. 서버 컨테이너 실행
docker run -d --name server1 --net my_spa_net --ip 192.168.100.100 -e SERVER_NAME=server1 my-server-image
docker run -d --name server2 --net my_spa_net --ip 192.168.100.101 -e SERVER_NAME=server2 my-server-image
docker run -d --name server3 --net my_spa_net --ip 192.168.100.102 -e SERVER_NAME=server3 my-server-image
# docker run --rm -it \
#   --net my_spa_net \
#   --ip 192.168.100.123 \
#   --name debug-server \
#   my-server-image \
#   bash