# Based on this https://github.com/WJDigby/hashms 

import argparse
import configparser
import time
from os import path, environ
from subprocess import Popen, PIPE
import psutil
import pygame


PROCESS_NAME = 'hashcat.exe'
pygame.mixer.init()
sound = pygame.mixer.Sound('hack-keyword.wav')


def check_pid(process_name):
    """Return pid of hashcat process."""
    for proc in psutil.process_iter():
        if process_name in proc.name():
            pid = proc.pid
            break
    if pid:
        return pid
    return False


def check_file(hashcat_outfile):
    """Check number of lines in designated outfile."""
    if not path.isfile(hashcat_outfile):
        return False
    with open(hashcat_outfile) as file:
        i = 0
        for i, lines in enumerate(file):
            pass
    return i + 1




def main():
    """Take user input to setup notifications. Print status updates to terminal."""
    parser = argparse.ArgumentParser(description='Periodically check hashcat cracking progress and notify of success.')
    parser.add_argument('-o', '--outfile', dest='hashcat_outfile', required=True,
                        help='hashcat outfile to monitor.')
    parser.add_argument('-i', '--interval', dest='check_interval', required=False, type=float,
                        default=15, help='Interval in minutes between checks. Default 15.')
    parser.add_argument('-n', '--notification-count', dest='notification_count', required=False,
                        type=int, default=5, help='Cease operation after N notifications. Default 5.')
    parser.add_argument('-t', '--test', dest='test', required=False, action='store_true',
                        help='Send test notificagtion'
                        'Does not count against notifications.')
    args = parser.parse_args()

    hashcat_outfile = args.hashcat_outfile
    check_interval = args.check_interval
    notification_count = args.notification_count
    test = args.test
    
    
    if test:
        print('[*] Conducting test. This does not count against notifications.')
        print('[*] Playing notification.')
        sound.play()

    starting_pid = check_pid(PROCESS_NAME)
    if not starting_pid:
        print('[-] hashcat is not running. Exiting.')
        exit()
    print('[*] hashcat PID: {}'.format(starting_pid))

    starting_outfile = check_file(hashcat_outfile)
    if starting_outfile:
        print('[*] Outfile exists and is {} lines long.'.format(starting_outfile))


    i = 1
    try:
        while i < notification_count + 1:
            current_pid = check_pid(PROCESS_NAME)
            current_outfile = check_file(hashcat_outfile)
            current_time = time.strftime('%A %d %B %Y at %H:%M')
            if starting_pid != current_pid:
                print('[-] Original hashcat process stopped. Exiting.')
                exit()
            elif not current_outfile:
                print('[-] File does not exist. Monitoring for file creation.'
                      'Checked on {}'.format(current_time))
            elif starting_outfile == current_outfile:
                print('[-] No more hashes cracked yet. Checked on {}'.format(current_time))
            elif starting_outfile != current_outfile:
                print('[+] Additional hashes cracked! Checked on {}'.format(current_time))
                message = ('{} hashes have been cracked.'
                           'Notification {} of {}.'.format(current_outfile, i, notification_count))
                print('[*] Playing notification.')
                sound.play()
                
                i += 1
                if i == notification_count + 1:
                    print('[*] Notification limit reached. Happy hunting.')
                    exit()
                starting_outfile = current_outfile
                print('[*] Sent {} out of {} notifications.'.format(i - 1, notification_count))
            print('[*] Sleeping for {} minutes...'.format(check_interval))
            time.sleep(float(check_interval) * 60)
    except KeyboardInterrupt:
        print('[-] Ctrl+C detected. Exiting.')
        exit()


if __name__ == '__main__':
    main()
