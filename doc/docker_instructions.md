



# Set up and build the docker instance

git clone https://github.com/darogan/ParticleStats

cd ParticleStats

docker build -t particlestats_docker .

docker run -it particlestats_docker


# View the available images on the system

docker images

docker ps -l
