docker login
#docker buildx build --platform linux/arm64 -t $1/inference --push .
#docker buildx build --platform linux/arm/v7 -t $1/inference --push .
docker build -t $1/inference
docker push $1/inference
