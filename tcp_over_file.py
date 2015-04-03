#!/usr/bin/env python

# Original script file_comm.py comes from --
# https://labs.mwrinfosecurity.com/tools/
#
# Updated version author: Oleg Mitrofanov
# The updated version is tested to work on Python 2.7 and 3.2
#


import base64
import signal
import socket
import sys
import threading as th
import time


# Usage
if len(sys.argv) != 6:
    print("Usage:\t{0} server ip_address tcp_port in_file out_file\n"
          "\t{0} client ip_address tcp_port out_file in_file\n".format(__file__))
    sys.exit(1)


# Assign program arguments
mode = sys.argv[1]
ip_address = sys.argv[2]
port = int(sys.argv[3])
in_stream_filename = sys.argv[4]
out_stream_filename = sys.argv[5]


# Initialize global variables
lock = th.Lock()
buffered_data = {}

# Clear files
open(in_stream_filename, "w").close()
open(out_stream_filename, "w").close()


# Open files to be used as in/out streams
in_stream = open(in_stream_filename, "r")
out_stream = open(out_stream_filename, "w")


# Interrupt signal handler
def sig_handler(signum, frame):
    print("Signal caught, exiting...")
    sys.exit(1)


# Register interrupt signal with handle
signal.signal(signal.SIGABRT, sig_handler)
print("[*] Press ^Break (Windows) or ^\ (Linux) to quit...\n")


# Loop listening for new socket connections
def listener_loop():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((ip_address, port))
    conn_id = 0

    while True:
        server_socket.listen(5)
        s, client = server_socket.accept()

        conn_id += 1
        print("[*] Connection received (ID = {}) "
              "from {}:{}".format(conn_id, client[0], client[1]))

        lock.acquire()

        out_stream.write("{} #CONNECT#$".format(conn_id))
        out_stream.flush()
        buffered_data[conn_id] = []

        lock.release()
        
        th.Thread(
            target=socket_reader_thread,
            name="t{}".format(conn_id),
            args=(conn_id, s)
        ).start()

        th.Thread(
            target=socket_writer_thread,
            name="t{}".format(conn_id),
            args=(conn_id, s)
        ).start()

        
# Read from file and process connections IDs + data
def file_reader():
    packet_buffer = ""
    while True:
        packet = in_stream.read(1024)
        if packet != '':
            packet_buffer += packet
            while True:
                part_before, part_sep, part_after = packet_buffer.partition("$")
                if part_sep == '':
                    break
                process_packet(part_before)
                packet_buffer = part_after
        else:
            time.sleep(0.001)    


# Read from socket/Write to file
def socket_reader_thread(conn_id, s):
    while True:
        if conn_id in buffered_data:
            try:
                data = s.recv(768)
            except socket.error as e:
                print("[*] (ID = {}): {} {}"
                      .format(conn_id, e.errno, e.strerror))

                lock.acquire()

                out_stream.write("{} #DISCONNECT#$".format(conn_id))
                out_stream.flush()
                del buffered_data[conn_id]
                s.close()

                lock.release()
                break
                
            lock.acquire()

            if data != '':
                b64encoded_data = base64.b64encode(data)
                str_data = b64encoded_data.decode(encoding="ascii")
                out_stream.write("{} {}$".format(conn_id, str_data))
                out_stream.flush()

                # print("Data read from socket ({})".format(len(encoded_data)))
                # print("Data read from socket ({})".format(encoded_data))

            lock.release()
        else:
            s.close()
            break


# Read from connection buffer/Write to socket
def socket_writer_thread(conn_id, s):
    global buffered_data

    while True:
        if conn_id in buffered_data:
            if len(buffered_data[conn_id]) > 0:
                lock.acquire()

                try:
                    data = buffered_data[conn_id].pop(0)
                except KeyError:
                    lock.release()
                    break
                
                lock.release()
                
                s.send(data)

                # print("Data read from socket ({})".format(len(data)))
                # print("Data read from socket ({})".format(data))

            else:
                time.sleep(0.001)
        else:
            break


# Process file packet
def process_packet(packet):
    conn_id, data = packet.split(" ")
    conn_id = int(conn_id)

    lock.acquire()

    if data == "#CONNECT#":
        print("[*] Connection request received (ID = {}). "
              "Connecting to {} on port {}".format(conn_id, ip_address, port))
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((ip_address, port))
            
        buffered_data[conn_id] = []

        th.Thread(
            target=socket_reader_thread,
            name="r{}".format(conn_id),
            args=(conn_id, s)
        ).start()

        th.Thread(
            target=socket_writer_thread,
            name="w{}".format(conn_id),
            args=(conn_id, s)
        ).start()
    elif data == "#DISCONNECT#":
        print("[*] Disconnect request received (ID = {}). "
              "Connection terminated.".format(conn_id))
        del buffered_data[conn_id]
    else:
        bytes_data = bytearray(data, encoding="ascii")
        decoded_data = base64.b64decode(bytes_data)
        try:
            buffered_data[conn_id].append(decoded_data)
        except KeyError:
            pass
        
        # print("Data written to socket ({})".format(len(data)))
        # print("Data written to socket ({})".format(data))
    
    lock.release()


# Mode specific configuration
if mode == "server":
    th.Thread(
        target=listener_loop,
        name="listener_loop_thread"
    ).start()
elif mode == "client":
    pass
else:
    print("Error: Invalid mode. Mode can be server or client.\n")
    sys.exit(1)


# Fire off file reader thread
th.Thread(
    target=file_reader,
    name="file_reader_thread"
).start()

while True:
    time.sleep(0.1)