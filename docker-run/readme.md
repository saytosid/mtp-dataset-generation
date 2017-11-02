## Requirements  
- gnlpy  
- docker (python lib)

## Usage  
- Run as many docker containers of `saytosid/myubuntu` image as:  
`docker run -it -v (pwd):/working_dir --cpus="2" --memory="1000m" saytosid/myubuntu`  
- Run `python container-stress-all.py` to begin randomly stressing containers  
- Run `python collect-container-metrics.py` to begin collection  

### Data collected  
Following metrics are collected:
- USER
- PID
- %CPU
- %MEM
- VSZ
- RSS
- TTY
- STAT
- START
- TIME
- COMMAND
- Timestamp
- OOM_Score
- io_read_count
- io_write_count
- io_read_bytes
- io_write_bytes
- io_read_chars
- io_write_chars
- num_fds
- num_ctx_switches_voluntary
- num_ctx_switches_involuntary
- mem_rss
- mem_vms
- mem_shared
- mem_text
- mem_lib
- mem_data
- mem_dirty
- mem_uss
- mem_pss
- mem_swap
- num_threads
- cpu_time_user
- cpu_time_system
- cpu_time_children_user
- cpu_time_children_system
- container_nr_sleeping
- container_nr_running
- container_nr_stopped
- container_nr_uninterruptible
- container_nr_iowait
- cpu_loadavg_simulated
- container_under_oom
