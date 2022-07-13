docker login
#docker buildx build --platform linux/arm64 -t $1/traffic_map --push .
docker buildx build --platform linux/arm/v7 -t $1/traffic_map --push .