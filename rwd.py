#!/usr/bin/env python
# -*- coding: utf8 -*-
# Created in 21/04/2012 - by Danillo Costa (hellnux)

# MIT License
#
# Copyright (c) 2018 Danillo Costa Ferreira
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

import os
import sys
import time
import datetime
import threading
import socket
import subprocess
import ConfigParser
import signal
import traceback
import urllib2

#####################################################################################
#                               Classes
#####################################################################################

class sleep_lock(threading.Thread):
        def __init__(self):
                threading.Thread.__init__(self)
        def run(self):
                time.sleep(delay_restart)

class sleep_lock_swap(threading.Thread):
        def __init__(self):
                threading.Thread.__init__(self)
        def run(self):
                time.sleep(delay_restart)

#####################################################################################
#                               Functions
#####################################################################################

def get_semi_constants():
        global hostname, ip_server, num_cpu, sender, subject, subject_top
        global subject_fail, pid_file_mysql
        hostname        = socket.gethostname()
        ip_server       = socket.gethostbyname(hostname)
        num_cpu         = detect_cpu()
        sender          = "root@" + hostname 
        subject         = "[" + script_name + " - " + ip_server + "]"
        subject_top     = subject + " Top"
        pid_file_mysql  = "/var/lib/mysql/" + hostname + ".pid"

def date_now_mail():
        '''Return date in mail format for smtplib. Not used. '''
        return time.strftime("%a, %d %b %Y %T %Z", time.localtime())

def date_now_log():
        return datetime.datetime.now().strftime("%Y/%m/%d %H:%M:%S") 

def read_file(archive):
        ''' Read first line '''
        arq = open(archive,'r')
        txt = arq.readline()
        arq.close()
        return str(txt)

def write_file(archive, msg):
        arq = open(archive,'a')
        arq.write(msg)
        arq.close()

def out(msg): 
        ''' Write "error" in stdout/file '''
        msg = '[' + date_now_log() + '] ' + msg + "\n"
        print msg
        write_file(out_file, msg)

def out_tmp(msg): # 4debug
        msg = '[' + date_now_log() + '] ' + msg + "\n"
        write_file(tmp_file, msg)

def send_mail(msg, subj): # smtplib fails
        cmd = "echo \"" + msg + "\" | mail -s \"" + subj + "\" \"" + emails_string + "\""
        os.system(cmd)

def get_loadavg():
        '''Return load average of last minute.'''
        return os.getloadavg()[0]

def detect_cpu():
        ncpus = os.sysconf("SC_NPROCESSORS_ONLN")
        if isinstance(ncpus, int) and ncpus > 0:
                return ncpus

def ConfigSectionMap(section):
        '''Transforms values from configuration file into dictionary'''
        dict1 = {}
        options = Config.options(section)
        for option in options:
                try:
                        dict1[option] = Config.get(section, option)
                        if dict1[option] == -1:
                                DebugPrint("skip: %s" % option)
                except:
                        print("exception on %s!" % option)
                        dict1[option] = None
        return dict1

def get_validate_config_file():
        global emails
        global emails_string
        global load_max_allow
        global swap_max_allow
        global delay_check
        global delay_restart
        global send_top
        global send_emails
        num_cpu = detect_cpu() # load_max_allow need
        flag = 0
        if ConfigSectionMap('Default')['load_max_allow'].split():
                try:
                        load_max_allow  = int(ConfigSectionMap('Default')['load_max_allow'].split()[0])
                except:
                        out("Error: 'load_max_allow' value is not a integer")
                        flag = 1
                if load_max_allow < num_cpu:
                        out("Error: 'load_max_allow' minimum value permitted is " + str(num_cpu))
                        flag = 1
        else:
                load_max_allow  = num_cpu * 3 # set default value if empty
        #
        #
        if ConfigSectionMap('Default')['swap_max_allow'].split():
                try:
                        swap_max_allow  = int(ConfigSectionMap('Default')['swap_max_allow'].split()[0])
                except:
                        out("Error: 'swap_max_allow' value is not a integer")
                        flag = 1
        else:
                out("Error: 'swap_max_allow' is not defined")
                flag = 1
        #
        #
        if ConfigSectionMap('Default')['delay_check'].split():
                try:
                        delay_check     = int(ConfigSectionMap('Default')['delay_check'].split()[0])
                except:
                        out("Error: 'delay_check' value is not a integer")
                        flag = 1
                if delay_check < 10:
                        out("Error: 'delay_check' minimum value permitted is 10 seconds")
                        flag = 1
        else:
                out("Error: 'delay_check' is not defined")
                flag = 1
        #
        #
        if ConfigSectionMap('Default')['delay_restart'].split():
                try:
                        delay_restart   = int(ConfigSectionMap('Default')['delay_restart'].split()[0])
                except:
                        out("Error: 'delay_restart' value is not a integer")
                        flag = 1
                if delay_restart < 60:
                        out("Error: 'delay_restart' minimum value permitted is 60 seconds")
                        flag = 1
        else:
                out("Error: 'delay_restart' is not defined")
                flag = 1
        #
        #
        if ConfigSectionMap('Default')['send_top'].split():
                send_top        = ConfigSectionMap('Default')['send_top'].split()[0]
                if send_top != "on" and send_top != "off":
                        out("Error: 'send_top' possible value is \"on\" or \"off\"")
                        flag = 1
        else:
                out("Error: 'send_top' is not defined")
                flag = 1
        #
        #
        if ConfigSectionMap('Default')['send_emails'].split():
                send_emails     = ConfigSectionMap('Default')['send_emails'].split()[0]
                if send_emails != "on" and send_emails != "off":
                        out("Error: 'send_emails' possible value is \"on\" or \"off\"")
                        flag = 1
        else:
                out("Error: 'send_emails' is not defined")
                flag = 1
        #
        #
        if ConfigSectionMap('Default')['emails'].split():
                emails          = ConfigSectionMap('Default')['emails'].split()
                emails_string   = ""
                for email in emails:
                        emails_string += email.strip('\'"')
        else:
                send_emails = "off"
                send_top = "off"
        #
        #
        if flag == 1:
                sys.exit(2)

def get_pid(file):
        if os.path.isfile(file):
                f = open(file,'r')
                pid = f.read().strip()
                f.close()
                return pid
        else:
                return "00" # Not running, but is down, not get this value

def check_pid(pid, cmdline_part):
        '''Check for the existence of a pid. cmdline_part is optional'''
        if pid != "00":
                try:
                        os.kill(int(pid), 0)
                except OSError:
                        return False
                else:
                        if cmdline_part:  #"None" not in
                                f = open("/proc/" + str(pid) +"/cmdline",'r')
                                cmdline = f.read()
                                f.close()
                                if cmdline_part not in cmdline:
                                        return False
                                else:
                                        return True
                        else:
                                return True
        else:
                return False

def get_swap(col):
        '''Return info of swap by argument (-3=size ; -2=used)'''
        total = 0
        f = open(swap_file,'r')
        c = f.readlines()[1:] #Ignore first line
        f.close()
        line = len(c)
        while line > 0:
                total = (total + int(c[line -1].split('\t')[col]))
                line = line - 1
        else:
                return total / 1024 # in MB

def get_stdout_shell(cmd):
        p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        stdout = []
        while True:
                line = p.stdout.readline()
                stdout.append(line)
                print line,
                if line == '' and p.poll() != None:
                        break
        return ''.join(stdout)

def get_exception_only(): 
        etype, value, tb = sys.exc_info()
        trace = traceback.format_exception_only(etype, value)
        trace[-1] = trace [-1].replace('\n','')
        return "".join(trace).replace("\n"," | ")

def kill_app(pid, app_name):
	trace_only = ""
        try:
                os.kill(int(pid), signal.SIGKILL) # Bug FUTEX (strace) 9
        except:
                trace_only = get_exception_only() #etype, value
	timestamp = date_now_log()
        if trace_only:
                msg = timestamp + ' - Warning: Unable to kill ' + app_name + ' - ' + trace_only + '\n' #canalgama aborta rwd aqui '.'   
        else:
                msg = timestamp + ' - ' + app_name + ' killed\n'
        write_file(log_file, msg)
        return msg

def timeout_cmd(cmd, timeout):
        ''' Make to use with a curl commmand '''
        start = datetime.datetime.now()
        process = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        while process.poll() is None:
                time.sleep(1) # Accept real number
                now = datetime.datetime.now()
                if (now - start).seconds > timeout:
                        os.kill(process.pid,signal.SIGKILL)
                        os.waitpid(-1, os.WNOHANG)
                        return [ 1, None ] # timeout
        return [ process.returncode, process.stdout.read() ] #list

def verify_swap():
        if "sleep_lock_swap" not in str(threading.enumerate()):
                swap_total = get_swap(-3)
                swap_used  = get_swap(-2)
                pid_apache = get_pid(pid_file_apache)
                pid_mysql  = get_pid(pid_file_mysql)
                if swap_used > ((swap_total * swap_max_allow) / 100):
                        # Write in log file
                        aux = "(" + str(swap_used) + '/' + str(swap_total) + ")"
                        msg = date_now_log() + ' - Initiated attempt to restart Apache/MySQL - swap ' + aux + '\n'
                        write_file(log_file, msg)
                        # Send mail
                        if send_emails == "on":
                                th = threading.Thread(target=send_mail, name="send_mail" ,args=(msg,subject,))
                                th.start()
                                # Generate output of top
                                if send_top == "on":
                                        top_output = get_stdout_shell(cmd_top)
                        # Restart Apache and MySQL
                        msg_ka = kill_app(pid_apache, "Apache")
                        msg_km = kill_app(pid_mysql, "MySQL")
                        return_apache = os.system('/scripts/restartsrv httpd')
                        timestamp_a = date_now_log()
                        return_mysql  = os.system('/scripts/restartsrv mysql')
                        timestamp_m = date_now_log()
                        if return_apache == 0:
                                msg_ra = timestamp_a + ' - Success to restart Apache\n'
                        else:
                                msg_ra = timestamp_a + ' - Failed to restart Apache\n'
                        if return_mysql == 0:
                                msg_rm = timestamp_m + ' - Success to restart MySQL\n'
                        else:
                                msg_rm = timestamp_m + ' - Failed to restart MySQL\n'
                        # Write in log
                        write_file(log_file, msg_ra)
                        write_file(log_file, msg_rm)
                        # Get swap after restart
                        swap_total_pos = get_swap(-3)
                        swap_used_pos  = get_swap(-2)
                        # Send mail
                        if send_emails == "on":
                                body = msg_ka + msg_km + msg_ra + msg_rm + '\nSwap: ' + str(swap_used_pos) + '/' + str(swap_total_pos)
                                if send_top == "off":
                                        send_mail(body, subject)
                                else: # top on
                                        body = body + '\n\n' + top_output
                                        send_mail(body, subject_top)
                        # Make dont restart in verify_apache if restarted here
                        if return_apache == 0 or return_mysql == 0:
                                d = sleep_lock()
                                d.start()
                                # If swap_used dont down with the restarts, this loop will be ignored in the next execution for a time
                                if (swap_used_pos >= swap_used):
                                        ls = sleep_lock_swap()
                                        ls.start() # "LockSwap.start"
                        time.sleep(1)

def verify_mysql():
        if os.path.isfile(lock_EA):
                return "abort"
        status_mysql = os.system('su root -c "/usr/bin/mysqladmin ping" > /dev/null 2>&1')
        if status_mysql != 0:
                msg = date_now_log() + ' - Initiated attempt to restart MySQL\n'
                write_file(log_file, msg)
                if send_emails == "on":
                        body = msg + '\nIP: ' + ip_server
                        th = threading.Thread(target=send_mail, name="send_mail", args=(body,subject,))
                        th.start()
                        # Generate output of top
                        if send_top == "on":
                                top_output = get_stdout_shell(cmd_top)
                # Restart
                return_mysql  = os.system('/scripts/restartsrv mysql')
                if return_mysql == 0:
                        msg = date_now_log() + ' - Success to restart MySQL\n'
                        write_file(log_file, msg)
                        d = sleep_lock() # delay restart
                        d.start()
                else:
                        msg = date_now_log() + ' - Failed to restart MySQL\n'
                        write_file(log_file, msg)
                # Send mail
                if send_emails == "on":
                        if send_top == "off":
                                send_mail(msg, subject)
                        else: # top on
                                msg = msg + '\n\n' + top_output
                                send_mail(msg, subject_top)
                time.sleep(1)

def verify_apache():
        global load_avg_old
        if os.path.isfile(lock_EA):
                load_avg_old = get_loadavg() # actualize load for the next cycle
                return "abort"
        ## Pre tr.
        # load_avg info
        load_avg = get_loadavg()
        if (load_avg > load_max_allow) and (load_avg_old > load_max_allow):
                load_max_alarm = 1
                load_status = "overload (" + str(load_avg) + " " +  str(load_avg_old) + " " + str(load_max_allow) + "/" + str(num_cpu) + ")"
        else:
                load_max_alarm = 0
                load_status = "load ok"
        # Check Apache status
        curl_exec = timeout_cmd("curl -s -o /dev/null -w \"%{http_code}\" http://localhost", curl_timeout)
        curl_returncode = curl_exec[0]
        curl_stdout = curl_exec[1] # May be tuple or none
        if curl_stdout is None:
        	curl_stdout = "None"
        else:
        	curl_stdout = str(curl_stdout)
        if curl_returncode == 0:
                if curl_stdout != "200":
                        status_apache = "Down"
                else:
                        status_apache = "Up"
        elif curl_returncode == 1: # curl timeout
                status_apache = "Timeout"
        elif (curl_returncode == 7) and (curl_stdout == "000"): # service httpd down => returncode = 7, stdout = 000
                status_apache = "Down"
        curl_debug = " (" + str(curl_returncode) + ";" + curl_stdout + ")" # 4 debug
        if (status_apache == "Up") and ( "sleep_lock" in str(threading.enumerate()) ):
                return "abort" # Avoid multiple restart when machine is overloaded
        if (load_max_alarm == 1) or (status_apache == "Down") or (status_apache == "Timeout"):
                # Write in log file
                msg = date_now_log() + ' - Initiated attempt to restart Apache - ' + load_status + ', ' + status_apache + curl_debug + '\n'
                write_file(log_file, msg)
                # Send mail
                if send_emails == "on":
                        th = threading.Thread(target=send_mail, name="send_mail", args=(msg,subject,))
                        th.start()
                        # Generate output of top
                        if send_top == "on":
                                top_output = get_stdout_shell(cmd_top)
                # Restart
                if status_apache == "Up":
                        os.system('killall -9 httpd')
                else:
                        os.system('for i in `ps auwx | grep -i nobody | awk \'{print $2}\'`; do kill -9 $i; done ')
                        os.system('for i in `lsof -i :80 | grep http | awk \'{print $2}\'`; do kill -9 $i; done')
                        os.system('for i in `lsof -i :80  | awk \'{print $2}\'`; do echo $i; done')
                        os.system('for i in `ipcs -s | grep nobody | awk \'{print $2}\'`; do ipcrm -s $i; done')
                return_apache = os.system('/scripts/restartsrv httpd')
                if return_apache == 0:
                        msg = date_now_log() + ' - Success to restart Apache\n'
                        write_file(log_file, msg)
                        d = sleep_lock()
                        d.start()
                        #d.join() # wait a threading terminate
                else:
                        msg = date_now_log() + ' - Failed to restart Apache\n'
                        write_file(log_file, msg)
                # Send mail
                if send_emails == "on":
                        if send_top == "off":
                                send_mail(msg, subject)
                        else: # top on
                                msg = msg + '\n\n' + top_output
                                send_mail(msg, subject_top)
                time.sleep(1)
        load_avg_old = load_avg

#####################################################################################
#                                       Main
#####################################################################################

version         = "18.0220" # Date format YY.MMDD
script_name     = "rwd"
path            = "/root/scripts/" + script_name + "/"
conf_file       = path + script_name + ".conf"
log_file        = path + script_name + ".log"
out_file        = path + script_name + ".out"
tmp_file        = path + script_name + ".tmp" # used by debug
swap_file       = "/proc/swaps"
pid_file_apache = "/usr/local/apache/logs/httpd.pid"
lock_EA         = "/usr/local/apache/AN_EASYAPACHE_BUILD_IS_CURRENTLY_RUNNING"
pid_file_this   = path + "/" + script_name + ".pid"
cmd_top         = "export COLUMNS=300 ; top -cbn 1 | sed 's/ *$//g' | grep -v \"top -cbn 1\" | grep -v \"sed 's/ *$//g'\""
curl_timeout    = 6 # seconds

# Call function get_semi_constants
get_semi_constants()

# Check user is root
if os.getuid() != 0:
        print "Error: Need a root to execute."
        sys.exit(1)

# Check if rwd is already is running
pid = get_pid(pid_file_this)
if (check_pid(pid, script_name) == True):
        print "Error: " + script_name + " is already running."
        sys.exit(3)

# Write the pid of this software on file
f = open(pid_file_this, 'w')
f.write(str(os.getpid()) + '\n')
f.close()

# Check conf file is exist
if os.path.isfile(conf_file):
        Config = ConfigParser.ConfigParser()
        Config.read(conf_file)
        get_validate_config_file()
else:
        out("Error: Configuration file not found: " + conf_file)
        sys.exit(2)

# Write software start in log
msg_log = date_now_log() + " - " + script_name + " Started - version: " + version + "\n"
write_file(log_file, msg_log)

load_avg_old = get_loadavg()

while 1:
        # Verify Swap
	try:
        	verify_swap()
        except:
                msg_log =  date_now_log() + " Error: verify_swap():" + get_exception_only()
                write_file(log_file, msg_log)   
        # Verify Apache
	try:
        	verify_apache()
        except:
                msg_log =  date_now_log() + " Error: verify_apache():" + get_exception_only()
                write_file(log_file, msg_log)        
        # Verify MySQL
	try:        
        	verify_mysql()
        except:
                msg_log =  date_now_log() + " Error: verify_mysql():" + get_exception_only()
                write_file(log_file, msg_log)   
        #out_tmp(s+m+a) # 4debug
        time.sleep(delay_check)