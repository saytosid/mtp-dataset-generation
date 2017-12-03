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
docker stop cont5
docker rm cont5
docker stop cont6
docker rm cont6
docker stop cont7
docker rm cont7
docker stop cont8
docker rm cont8
docker stop cont9
docker rm cont9
docker stop cont10
docker rm cont10
echo "All containers killed"

# Remove prev data
rm -r data
echo "prev data removed"

# Kill all tmux sessions
tmux kill-session -t stress
tmux kill-session -t collect
echo "Prev tmux sessions killed"

# Run new containers in tmux sessions
tmux new-session -d -s cont1 'docker run -it -v (pwd):/working_dir --cpus="2" --memory="1000m" --name=cont1 saytosid/myubuntu'
tmux new-session -d -s cont2 'docker run -it -v (pwd):/working_dir --cpus="2" --memory="1000m" --name=cont2 saytosid/myubuntu'
tmux new-session -d -s cont3 'docker run -it -v (pwd):/working_dir --cpus="2" --memory="1000m" --name=cont3 saytosid/myubuntu'
tmux new-session -d -s cont4 'docker run -it -v (pwd):/working_dir --cpus="2" --memory="1000m" --name=cont4 saytosid/myubuntu'

tmux new-session -d -s cont5 'docker run -it -v (pwd):/working_dir --cpus="4" --memory="2000m" --name=cont5 saytosid/myubuntu'
tmux new-session -d -s cont6 'docker run -it -v (pwd):/working_dir --cpus="4" --memory="2000m" --name=cont6 saytosid/myubuntu'
tmux new-session -d -s cont7 'docker run -it -v (pwd):/working_dir --cpus="4" --memory="2000m" --name=cont7 saytosid/myubuntu'
tmux new-session -d -s cont8 'docker run -it -v (pwd):/working_dir --cpus="4" --memory="2000m" --name=cont8 saytosid/myubuntu'
tmux new-session -d -s cont9 'docker run -it -v (pwd):/working_dir --cpus="4" --memory="2000m" --name=cont9 saytosid/myubuntu'
tmux new-session -d -s cont10 'docker run -it -v (pwd):/working_dir --cpus="4" --memory="2000m" --name=cont10 saytosid/myubuntu'
sleep 2
echo "Containers started in tmux sessions"

# start data collection
tmux new-session -d -s collect 'fish'
tmux send -t collect 'sleep 2' ENTER
tmux send -t collect 'source virtenv/sid/bin/activate.fish' ENTER
tmux send -t collect 'sleep 2' ENTER
tmux send -t collect 'python collect-container-metrics.py' ENTER

echo "Data collection started"

# start stresses
tmux new-session -d -s stress 'fish'
tmux send -t stress 'sleep 2' ENTER
tmux send -t stress 'source virtenv/sid/bin/activate.fish' ENTER
tmux send -t stress 'sleep 2' ENTER
tmux send -t stress 'python container-stress-all.py' ENTER
echo "Stress started"

