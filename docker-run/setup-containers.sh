#!/bin/bash

# Stop and remove previous containers
docker stop cont1
docker rm cont1
docker stop cont2
docker rm cont2
docker stop cont3
docker rm cont3
docker stop cont4
docker rm cont4

# Run new containers in tmux sessions
tmux new-session -d -s cont1 'docker run -it -v (pwd):/working_dir --cpus="2" --memory="1000m" --name=cont1 saytosid/myubuntu'
tmux new-session -d -s cont2 'docker run -it -v (pwd):/working_dir --cpus="2" --memory="1000m" --name=cont2 saytosid/myubuntu'
tmux new-session -d -s cont3 'docker run -it -v (pwd):/working_dir --cpus="4" --memory="2000m" --name=cont3 saytosid/myubuntu'
tmux new-session -d -s cont4 'docker run -it -v (pwd):/working_dir --cpus="4" --memory="2000m" --name=cont4 saytosid/myubuntu'
