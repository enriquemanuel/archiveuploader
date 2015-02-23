#!/usr/local/bin/python # if local
## if in MH Servers #!/mnt/asp/python/bin/python

#### 
### Made by Enrique Valenzuela <enrique.valenzuela@blackboard.com>
### Version 0.1
### Connects only to UNIX Servers
### Local version rsyncs from one directory to a temp location
### Remote version rsyncs from temp location to sftp
### Use it at your own discretion and at your risk


import logging, sys, argparse, gzip, os, datetime, socket


def get_args():
  # Define the parser
  parser = argparse.ArgumentParser(description='Upload Blackboard Logs to SFTP')
  parser.add_argument('-V', '--version', action='version', version="%(prog)s (version 0.1)")

  # Configuring subparsers for actions
  subparsers = parser.add_subparsers(help='Select which Option File or CLI in order to do it correctly')

  # Local - to move archives from Blackboard Content to a temporal location
  local_parser = subparsers.add_parser('local', help='Use this to move archives from $BBHOME/Content/ to the tempstore location')
  local_parser.add_argument('--destination', required=True,  help='Location to move the archives to.', type=str)
  local_parser.add_argument('--courselist', required=True, type=str, help='List of courses in a txt file to move the courses')
  
  # Remote - to move archives from temporal location to remote server (sftp)
  remote_parser = subparsers.add_parser('remote', help='Use this to move archives from tempstore to the SFTP location')
  remote_parser.add_argument('--configfile', required=True,  help='Configuration File', type=str)
  remote_parser.add_argument('--courselist', required=True, type=str, help='List of courses in a txt file to move the courses')
  
  args = parser.parse_args()
  

  # Set all the Vars
  return localorremote(args)


def localorremote(args):
  try:
    args.destination
  except AttributeError: # is not local, is remote
    remote(args)    
  else:
    local(args)


def local(args):
  schema=os.listdir("/usr/local/blackboard/content/vi")[0]
  bbcontent="/usr/local/blackboard/content/vi/"+schema+"/courses/1/"

  # need to read the course list and then feed it to the rsync to be moved
  with open(args.courselist) as courses:
    for course in courses:
      course= course.rstrip('\n')
      os.system("rsync -azPL  " + bbcontent + course + "/archive/Ar*.zip " + args.destination )



def remote(args):
  try:
    args.configfile
  except AttributeError:
      print "We can't open the configuration file"
  else:
    with open(args.configfile) as configfile:
      configdict = {}
      for line in configfile:
        items = line.split('=', 1)
        configdict[items[0]] = items[1].rstrip('\n')
  try:
    args.courselist
  except AttributeError:
      print "We can't open the course list file"
  else:
    with open(args.courselist) as courselist:
      coursearray = []
      for course in courselist:
        course= course.rstrip('\n')
        coursearray.append(course)

  #we have everything stored correctly now lets execute it
  uploadFiles(configdict,coursearray)


def uploadFiles(configdict,coursearray):
  print "Upload Starting "+curDate2
  print "uploading "+ str(len(coursearray)) +" course archives"
  for course in coursearray:
    #print course
    #print ("rsync -azP --bwlimit="+str(configdict['bwlimit']) +" -e 'ssh -p " + str(configdict['port']) + " -i " + str(configdict['idpath']) + "' "+ str(configdict['localpath']) +"/"+course +" " + str(configdict['user']) + "@" + str(configdict['sftp']) + ":" + str(configdict['destinationpath']))
    os.system("rsync -azP --bwlimit="+str(configdict['bwlimit']) +" -e 'ssh -p " + str(configdict['port']) + " -i " + str(configdict['idpath']) + "' "+ str(configdict['localpath']) +"/"+course +" " + str(configdict['user']) + "@" + str(configdict['sftp']) + ":" + str(configdict['destinationpath']))
  

  
  
  


####################
### GLOBAL VARS ####
####################
today = datetime.datetime.now()
curDate2 = today.strftime("%Y-%m-%d")
schema=os.listdir("/usr/local/blackboard/content/vi")[0]
bbcontent="/usr/local/blackboard/content/vi/"+schema+"/courses/1/"
hostname = socket.gethostname()
appnum = hostname[-5:]


# Call the function get_args to define all the arguments
get_args()

