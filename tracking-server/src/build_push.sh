docker login
docker buildx build --platform linux/x86_64 -t $1/tracking_server --push .
