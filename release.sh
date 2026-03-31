cp ./.env ./.env.local

cp .docker/prod/Dockerfile ./Dockerfile

docker buildx build --no-cache -f Dockerfile -t django-project:0.0.1 --platform linux/amd64 .

cp ./.env.local ./.env

rm ./Dockerfile