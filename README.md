# Example code to create TCP communication for control of `psychopy` stimuli
_Yevgeniy B. Sirotin_

This is example code how to control `psychopy` stimuli, namely gratings.  This code goes off the original non-working code in:

`basic_fixedDuration_w_def_2019_08_06.py`

# Files
The file contents are as follows:
* `requirements.txt`  - a dump of `pip list` for my environment
* `tcp_send.py` - a simple CLI to send a TCP message
* `tcp_receive.py` - contains a classes for working with TCP messages
* `run_tcp.py` - runs a basic `psychopy` stimulus controlled by TCP messages 

## Testing functionality
To test the code, open two shell windows.  In the first window, run: `python run_tcp.py`.  This should generate a window with a fixation point and a drifting grating.  Ensure that the direction of the grating can be controlled by `l` and `r` keys.

Now in the second shell run: 
* `python tcp_send l` to change the direction of the grating to the left
* `python tcp_send r` to change the direction of the grating to the right
* `python tcp_send q` to shut down the `run_tcp.py` process

The server will respond to multiple messages on each connection.  To test sending multiple messages run:
* `python tcp_send -D 1 l r l r l r` to have the grating shift several times with a delay of 1 second in between
* `python tcp_send -D 0.5 l r l r l r` to have the grating shift several times with a delay of 0.5 seconds in between

You can also try out a CLI to send keyboard hits to the server using `tcp_send_keyboard.py`:
* run `python tcp_send_keyboard`
* all keyboard hits will be sent to server
* hit the `q` key to stop and shutdown the server
* hit `Ctrl+C` to quit without shutting down the server

## How it works
### Message format
In this example, the message format is always a 2-byte header that specifies the data payload size (in bytes) and then the data payload.  The header is in little endian format.

### `tcp_send.py`
This CLI is very simple and running `tcp_send.py -h` should explain how it works.

### `tcp_receive.py`
The basic approach I took here is to use threading to process TCP requests in a background thread even as `psychopy` display updates can happen via a loop in the main thread.  

The class `ServerThread` is a thread that processes TCP messages arriving on a listening socket and executes a custom function whenever new data arrives. 

The class `ServerSocket` creates the socket and manages starting and stopping the `ServerThread`.

### `run_tcp.py`
This shows how to use `ServerSocket` within a `psychopy` application.  It draws and updates a grating stimulus based on messages received from either the keyboard via `event` or from a TCP source.  The messages are translated into making the grating move to the left, to the right, or quitting the application.

## TO DO:
Managing sockets manually is cumbersome and likely inefficient.  Code should be rewritten using `zmq`, however, this may require `zmq` to be used in both client and server and so may not work well with legacy code.
