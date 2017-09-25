



# Set up and build the docker instance

docker pull dockerfile/ubuntu


docker build -t particlestats_docker .


docker run --name particlestats_docker -i -t ubuntu




# View the available images on the system

docker images

docker ps -l