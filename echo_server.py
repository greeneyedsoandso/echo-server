import socket
import sys
import traceback


def server(log_buffer=sys.stderr):
    # set an address for our server
    address = ('127.0.0.1', 10000)
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM, socket.IPPROTO_TCP)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    # log that we are building a server
    print("making a server on {0}:{1}".format(*address), file=log_buffer)
    sock.bind(address)
    sock.listen(1)

    try:
        # the outer loop controls the creation of new connection sockets. The
        # server will handle each incoming connection one at a time.
        while True:
            print('waiting for a connection', file=log_buffer)
            conn, addr = sock.accept()
            try:
                print('connection - {0}:{1}'.format(*addr), file=log_buffer)

                # the inner loop will receive messages sent by the client in
                # buffers.  When a complete message has been received, the
                # loop will exit
                while True:
                    buffer = 16
                    data = conn.recv(buffer)
                    print('received "{0}"'.format(data.decode('utf8')))
                    sock.sendall(data)
                    print('sent "{0}"'.format(data.decode('utf8')))
                    # if len(data) == 0:
                    #     break

            except Exception as e:
                traceback.print_exc()
                sys.exit(1)
            # finally:
            #     # TODO: When the inner loop exits, this 'finally' clause will
            #     #       be hit. Use that opportunity to close the socket you
            #     #       created above when a client connected.
            #     print(
            #         'echo complete, client connection closed', file=log_buffer
            #     )
            #     sock.close()
    except KeyboardInterrupt:
        print('quitting echo server', file=log_buffer)
        sock.close()


if __name__ == '__main__':
    server()
    sys.exit(0)
