# CS_331_Assignment_1

## Instructions for Running the Code
1. Clone the repository. You can use the command:
```console
git clone https://github.com/jeet1248/CS_331_Assignment_1.git
```
This will create a replica of the repository on you local machine.

2. Navigate to the repository folder.
```console
cd CS_331_Assignment_1
```

3. Set up the Environment:
If you don't have python installed on your system, you can download the latest version of python from the [Python's](https://www.python.org) official website, or on Linux/Debian systems, using the command
```console
sudo apt install python3
```

Once python is installed, get the required packages using `pip`, python's package manager. The required packages are already listed in the file `requirements.txt`. You can use the command
```console
python3 -m pip install -r requirements.txt
```
This will download all the required packges for running the python scripts.

3. Start the server on your machine so that you can process the packet capture files using the pre-defined rules. Use the command.
```console
python server.py
```
This would show something like
```console
...\CS_331_Assignment_1> python server.py
[SERVER] Listening on 127.0.0.1:53535...
```
This indicates that the server is now up and listening on the url `127.0.0.1` on port `53535`.

4. Once the server is up, you can run the file `client.py` using the command `python client.py`. But ensure that the pcap file `0.pcap` is present in the same directory as the client. Otherwise, it won't be able to find the file and give errors. 
If you want to use a `pcap` file other than `0.pcap`, replace the `0.pcap` in the file `client.py` with the path of your `pcap` file. If you want to use the `0.pcap` file used in this assignment, you can access it using this [link](https://drive.google.com/file/d/1_emB74liOV9wxidbkCy3G_rZ2xS-KGWg/view?usp=sharing).