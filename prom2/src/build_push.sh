docker login
docker buildx build --platform linux/arm64 -t $1/app2prom --push .
