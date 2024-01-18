# hashcatnotify
 Plays a sound when new hashes are cracked by hashcat 
 
**Currently, hashcat.exe as process_name and hack-keyword.wav as sound are hardcoded in the file. **

```
> python .\hashcatnotify.py -h
pygame 2.5.2 (SDL 2.28.3, Python 3.10.5)
Hello from the pygame community. https://www.pygame.org/contribute.html
usage: hashcatnotify.py [-h] -o HASHCAT_OUTFILE [-i CHECK_INTERVAL] [-n NOTIFICATION_COUNT] [-t]

Periodically check hashcat cracking progress and notify of success.

options:
  -h, --help            show this help message and exit
  -o HASHCAT_OUTFILE, --outfile HASHCAT_OUTFILE
                        hashcat outfile to monitor.
  -i CHECK_INTERVAL, --interval CHECK_INTERVAL
                        Interval in minutes between checks. Default 15.
  -n NOTIFICATION_COUNT, --notification-count NOTIFICATION_COUNT
                        Cease operation after N notifications. Default 5.
  -t, --test            Send test notificagtionDoes not count against notifications.
```

