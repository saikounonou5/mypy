import os
import yum
import imp


#Automate the installation and configuration of nginx web server
def is_installed(package_name):
     yb = yum.YumBase()
     if yb.rpmdb.searchNevra(name=package_name):
          print package_name + ' is installed...'
          return True
     else:
          print 'No'
          return False

print '\n################ OS PACKAGES #################'
#Install Nginx
if not is_installed('epel-release'):
     os.system('sudo yum -y install epel-release')

if not is_installed('nginx'):
     os.system('sudo yum -y install nginx')

if not is_installed('wget'):
     os.system('sudo yum -y install wget')

print '\n################ GIT ######################'
#Install git
if not is_installed('git'):
     os.system('sudo yum -y install git')
     os.system('sudo git config --global user.name\'AutoUser\'')
#Clone repo
if os.path.isdir('/exercise-webpage'):
     print '\nGetting most updated version of /exercise-webpage'
     owd = os.getcwd()
     os.chdir('/exercise-webpage')
     os.system('sudo git pull --ff-only upstream master')
     os.chdir(owd)
else:
     os.chdir('/')
     os.system('sudo git clone https://github.com/saikounonou5/exercise-webpage')
     owd = os.getcwd()
     os.chdir('/exercise-webpage')
     os.system('sudo git remote add upstream https://github.com/saikounonou5/exercise-webpage.git')
     os.chdir(owd)

print '\n############## NGINX PARSER ##############'
#nginxparser
if os.path.isdir('/nginxparser'):
     print 'nginx parser already cloned from repo'
else:
     os.system('sudo git clone https://github.com/saikounonou5/nginxparser')
#Check if nginxparser installed
try:
     imp.find_module('nginxparser')
     found = True
     print 'nginxparser is installed...'
except ImportError:
     found = False
     print 'nginxparser is not installed...'
     print 'Installing now...'
     os.chdir('/')
     owd = os.getcwd()
     os.chdir('/nginxparser')
     os.system('sudo python setup.py install')
     os.chdir(owd)
#Check if pyparsing installed
try:
     imp.find_module('pyparsing')
     found = True
     print 'pyparsing is installed...'
except ImportError:
     found = False
     print 'pyparsing is not installed...'
     print 'Installing now...'
     print os.getcwd()
     os.system('sudo rpm -ivh pyparsing-*.rpm')
    
from nginxparser import load,dump,dumps
import pyparsing
#Configure root and listener in nginx.config
j= load(open('/etc/nginx/nginx.conf'))


#Loop down to server config vars
for line in j:
     for l in line:
          for v in l:
               for g in v:
                    for t in g:
                         if 'listen' in t:
                              if t[1] != '8000 default_server':
                                   t[1]= '8000 default_server'
                                   print 'Listener port set to 8000'
                              else:
                                   print 'Listener port already set to 8000'
                                   print t
                         if 'root' in t:
                             print t
                             if t[1] !='/exercise-webpage':
                                   t[1]='/exercise-webpage'
                                   print 'root set to /exercise-webpage'
                             else:
                                  print 'root already set to /exercise-webpage'
with open("/etc/nginx/nginx.conf",'w') as new_conf:
     dump(j,new_conf)

#Temporarily switch to SELinux to permissive mode
os.system('setenforce permissive')

#Get machine's external IP
ext_ip = os.popen('ip addr show eth0').read().split("inet ")[1].split("/")[0]

print ext_ip + '\n'
#Start Nginx
os.system('sudo systemctl start nginx')

#Call gitpage
print ext_ip+':8000'
os.system('sudo curl '+ext_ip +':8000')
