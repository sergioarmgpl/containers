docker login
#docker buildx build --platform linux/arm64 -t $1/proxy --push .
docker buildx build --platform linux/arm/v7 -t $1/proxy --push .