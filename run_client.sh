# docker network create \
#   --subnet=192.168.100.0/24 \
#   --gateway=192.168.100.1 \
#   my_spa_net

# 2. 클라이언트 컨테이너 실행
count=1
for i in $(seq 2 51); do
  docker run --rm \
    --name client$count \
    --net my_spa_net \
    --ip 192.168.100.$i \
    -e CLIENT_NAME=client$count \
    my-client-image
  count=$((count + 1))
done

# docker run --rm -it \
#   --name debug-client \
#   --net my_spa_net \
#   --ip 192.168.100.123 \
#   -e CLIENT_NAME=client1 \
#   my-client-image bash


