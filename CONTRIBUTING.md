# Contributors

[SoftHost](https://softhost.com.br/) : Bug report, choice of software name.

# Search Sources #
Get numbers of processor  
http://stackoverflow.com/questions/1006289/how-to-find-out-the-number-of-cpus-in-python 2.6+  
http://stackoverflow.com/questions/4929961/cpuinfo-in-python-2-4-for-windows 2.4+  

Send mail  
http://blog.krix.com.br/2009/07/enviando-email-em-python/  

Get Date  
http://www.saltycrane.com/blog/2008/06/how-to-get-current-date-and-time-in/  

Get IP of server = ping $(hostname) in shell  
http://stackoverflow.com/questions/166506/finding-local-ip-addresses-using-pythons-stdlib  

Check pid  
http://stackoverflow.com/questions/38056/how-do-you-check-in-linux-with-python-if-a-process-is-still-running  

stdout of shell on the fly  
http://blog.kagesenshi.org/2008/02/teeing-python-subprocesspopen-output.html  

chek pid is running  
http://stackoverflow.com/questions/568271/check-if-pid-is-not-in-use-in-python  

Threading  
http://python.6.n6.nabble.com/Threads-Python-X-Threads-Java-Round-2-td2037643.html  
http://medeubranco.wordpress.com/2008/07/10/threads-em-python/  
http://stackoverflow.com/questions/8600161/executing-periodic-actions-in-python  

timeout_command  
http://howto.pui.ch/post/37471155682/set-timeout-for-a-shell-command-in-python  

Get only http code
http://superuser.com/questions/272265/getting-curl-to-output-http-status-code
```
curl -s -o /dev/null -w \"%{http_code}\" http://site.com
```
4 python >= 2.6
```
urllib2.urlopen('http://site.com/').getcode()
lynx -dump -head http://site.com
curl -sI http://site.com
```

Maybe help  
https://www.crybit.com/semaphores-linux/  
