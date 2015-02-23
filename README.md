Uploader
=========
Due to increasingly clients requesting to upload course archives, I decided to implement a new and improved script to fully automated and send the archives as needed.

Help?
===========
The script has a help option that you can invoke and learn how to use it as needed. this can be done with the -h option or with --help.

To note that -d (–debug) or -l (--log-file) have not been implemented at this stage.

Generic Help
    # python archive_uploader.py -h
    usage: archive_uploader.py [-h] [-V] {local,remote} ...

    Upload Blackboard Logs to SFTP

    positional arguments:
      {local,remote}  Select which Option File or CLI in order to do it correctly
        local         Use this to move archives from $BBHOME/Content/ to the
                      tempstore location
        remote        Use this to move archives from tempstore to the SFTP
                      location

    optional arguments:
      -h, --help      show this help message and exit
      -V, --version   show program's version number and exit

    

For Remote Help

    # archive_uploader.py remote -h
      usage: archive_uploader.py remote [-h] --configfile CONFIGFILE --courselist
                                        COURSELIST

      optional arguments:
        -h, --help            show this help message and exit
        --configfile CONFIGFILE
                              Configuration File
        --courselist COURSELIST
                              List of courses in a txt file to move the courses


For Local Help
    # archive_uploader.py local -h
    usage: archive_uploader.py local [-h] --destination DESTINATION --courselist
                                     COURSELIST

    optional arguments:
      -h, --help            show this help message and exit
      --destination DESTINATION
                            Location to move the archives to.
      --courselist COURSELIST
                            List of courses in a txt file to move the courses

The idea
============
The idea behind this script is to 
1. If chosen the local option to find from a list of courses all the archives and move them to a temp location
2. If chosen remote, to upload all the files (hopefully archives) from the location specified to the SFTP


This is done via Public / Private keys which needs to be generated from the Blackboard side. 

How to generate a Public an Private Key
========================================
1. First run `ssh-keygen -t rsa`
2. Enter where you would like to save the private and public key. Usually I stored it in a centralized location
3. You can enter the passphrase afterwards.
4. Now you are going to copy the public key to the server. You need at this point to have the User, the Host and the Password. Perform the following command: ssh-copy-id -i /path/to/newly/created/key.pub user@host.com
5. The password will be required, so you will enter it at this time
6. You are done!

More info on:
* How to create Public and Private keys: https://help.github.com/articles/generating-ssh-keys
* If they don't work, I would suggest you troubleshoot this: http://inderpreetsingh.com/2011/08/04/ssh-privatepublic-key-auth-not-working/

How to execute it (Remote)?
===========================
After you have installed and configured the Public and Private keys, my recommendation are the following:

1. Create a directory under $BBHOME/content/vi/<schema>/plugins directory. In my case I like to name it the same archive_uploader. 
2. In the same directory, I copy the files from the tempstore and the keys that were just created.
3. Create / Modify the remoteconfig.txt file for your specifications
4. Create a list of courses

How to execute it (Local)?
===========================
For local you don't need keys, since you are moving information from your own paths probably to mount folders
You only need to specify the folders where you want them to be moved with the --destination option

How does it work?
=================
* This script uses RSYNC to move information around, since it helps to debug and connect correctly to the system.
* At this time we are not using and don't need the option to have a database of the RSYNC so it might be an overkill for the tool that we are currently using, but found it was the easiest option to implement base on experience
* We read and parse the course list file and depending on the selecton (local or remote) we navigate to the path and start moving files around. If chosen local, we go into the course on the list and then into the archive folder to then find if there is an A*.zip file. This is the format for the Archives.  We then move it accordingly.
* For the remote, we actually are a bit different, since we actually want to move everything inside the folder. So we just point the local folder, this can contain any information inside, only archives or all the course information and then upload it to the desired path to the SFTP.

Example of Use
===============
    #local example
    python /home/evalenzuela/archiveUploader.py local --destination /tmp/evalenzuela/ --courselist /home/evalenzuela/cursos.txt 

    # remote example
    python /home/evalenzuela/archiveUploader.py remote --configfile /home/evalenzuela/remoteconfig.txt --courselist /home/evalenzuela/cursos.txt 

Please look that it contains a full path for safety measures. Also it is run as root and it should be in the cron of root. This is because of permissions on the /tmp location.



New features?
==============

If you need any additional features, please let me know. At this time, the server should work for most cases and it should be fairly simple to implement without any problem.

Requirements
=============

The main requirements at this time are:
* Create the Public and Private key
* Client Server needs to be UNIX - no windows!
* Client Server needs to have the Private key installed with correct permissions
