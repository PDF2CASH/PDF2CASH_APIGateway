echo "$DOCKER_PASSWORD" | docker login -u "$DOCKER_USERNAME" --password-stdin
docker tag pdf2identity pdf2cash/pdf2identity:latest
docker push pdf2cash/pdf2identity:latest
