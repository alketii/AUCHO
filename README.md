AUCHO
=====

AUCHO Upload Changes Only - version 0.1-dev

## CAUTION
THIS IS AN EXPERIMENTAL VERSION , USE FOR TESTING PURPOSES ONLY ! This means it may work ,but it also may surprise you.

I'm still learning pyQt. Many things are missing , and many aren't done right.

### Description
Upload only your modified and new files on FTP.
It uses MD5 (in next version will be changed to CRC-32) to store hash in sqlite db and will compare them with another db which stores uploaded data.

### Download Binaries
* AUCHO for Linux x64 https://github.com/alketii/AUCHO/blob/master/BIN/AUCHO_Linux_x64.zip?raw=true
* AUCHO for Windows x86 https://github.com/alketii/AUCHO/blob/master/BIN/AUCHO_Windows_x86.zip?raw=true

### DONE
* Create Project
* Compare files for changes
* Upload modified or new files
* Many other small things

### TODO
* Send DELETE command for files and folders
* Edit Project Form
* Remove Project
* More polish
* Multi-language support
* Make QtreeWidget with children
* From MD5 to CRC-32 (for faster checksum)
* FTP checksum for syncing possibilities

### Screenshots
###### Creating new project
![alt tag](https://i.imgur.com/1KmpYE5.png)
###### Comparing files
![alt tag](https://i.imgur.com/PiCHB4L.png)
###### Providing password (if password field in projects creation is left blank)
![alt tag](https://i.imgur.com/KQtGaKu.png)
###### Comparing files (after some modifications)
![alt tag](https://i.imgur.com/7fcpp2e.png)

