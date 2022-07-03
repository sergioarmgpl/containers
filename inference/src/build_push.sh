docker login
docker buildx build --platform linux/arm/v7 -t $1/inference --push .