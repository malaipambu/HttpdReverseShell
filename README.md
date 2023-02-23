# HttpdReverseShell

HttpdReverseShell is a Python script that allows you to obtain a reverse shell. This runs a httpd server on a attackers machine which will give a shell access when the clinet connects to the server via a script.
I coded this from a attacker perspective so just the HTTP protocol is highly likely to be opened on the outbound or egress firewall rules, since it's used for web surfing. Also, a lot of HTTP traffic is required in every network, which makes monitoring much harder and the chances of us slipping up are high.


## Prerequisites

- Python 3.x
- An Apache HTTP server vulnerable to CVE-2019-0211

## Installation

Clone the repository:

`git clone https://github.com/malaipambu/HttpdReverseShell.git`


## Usage

Run the script with the following command:

`python main.py
`

main.py it will start the httpd server and creates target.py on the ip you specified (or it takes the default IP) and once the target.py is executed on the target machine you will be promted with a shell. It is important the attacker and the target must be in the same network (I will improve this in near furture). you can execute command in the shell you can upload files to target using "upload " this file must be in the uploads folder you can steal data from the target using the "download <filename/filepath>" the downloaded files will be in the downloads folder these upload and download folder will be created at the main.py execution in the script's working directory.

The script will prompt you for the following information:

- Your IP address
- The port on which the reverse shell should listen
- The name of the python file to be generated
- The location where the python file should be saved


## Disclaimer

This script is provided for educational purposes only. The author is not responsible for any illegal use of this script.
