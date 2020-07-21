# Summary

A python3 script that calls `obs` record the screen programmatically.

When starting the script saves:

    - time and date when it was started
    - commit hash
    
Once we stop the recording the script will update the video generated with the following name:

    {date time}_{title}_{start}:{end}.mkv
    
## Rational
The rational for this is to be able to easily record videos while writing software.

## Setup
Download the script and place inside a git repository.

Open OBS Studio and setup all the recording as wished. These options will be the used ones when triggered through the script.
  
## Usage
```
python obs [start|stop] "download_folder/"
```

to start:
```
python obs.py start "~/screencasts/"
```
    
to stop:
```
python obs.py stop "~/screencasts/"
```


TODO: export gifs from a time + duration parameter
