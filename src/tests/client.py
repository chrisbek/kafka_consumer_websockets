import socketio

sio = socketio.Client()
OBSERVED_VIDEO_IDENTIFIERS = ['93f98662-8907-4f43-bb4c-280501481046', '69e7266c-753e-4ed3-b7fc-9035133a293f']


def main():
    sio.connect('http://172.30.1.21:8000', wait=False)
    sio.wait()


@sio.event
def connect():
    print('Client connected')
    sio.emit('register_room', {'rooms': OBSERVED_VIDEO_IDENTIFIERS})
    print('Rooms registered')
    sio.emit('consume_1_min_aggregations', {})
    sio.emit('consume_5_min_aggregations', {})
    sio.emit('consume_10_min_aggregations', {})


@sio.event
def connect_error(e):
    print(f'Client connect failed: {e}')


@sio.event
def live_aggregations_1(data):
    print(f'Data reported after 1\': {data}')


@sio.event
def live_aggregations_5(data):
    print(f'Data reported after 5\': {data}')


@sio.event
def live_aggregations_10(data):
    print(f'Data reported after 10\': {data}')


if __name__ == '__main__':
    main()
