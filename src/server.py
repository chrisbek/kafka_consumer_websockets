import json
from aiokafka import AIOKafkaConsumer
import asyncio
import socketio
from src.utils.config_utils import ConfigUtils
from src.utils.log_service import LogService

config = ConfigUtils.get_config()
logger = LogService.get_logger(config.log_level)
sio = socketio.AsyncServer(async_mode='asgi', ping_timeout=60, cors_allowed_origins='*')
app = socketio.ASGIApp(sio)

one_min_aggregations_consumer = AIOKafkaConsumer(
    config.one_minute_aggregations_topic_name,
    bootstrap_servers=config.kafka_broker_url,
    auto_offset_reset='earliest',  # If committed offset not found, start from beginning
    enable_auto_commit=True,
    group_id=config.kafka_group_id,
    value_deserializer=lambda x: json.loads(x.decode()))

five_min_aggregations_consumer = AIOKafkaConsumer(
    config.five_minute_aggregations_topic_name,
    bootstrap_servers=config.kafka_broker_url,
    auto_offset_reset='earliest',
    enable_auto_commit=True,
    group_id=config.kafka_group_id,
    value_deserializer=lambda x: json.loads(x.decode()))

ten_min_aggregations_consumer = AIOKafkaConsumer(
    config.ten_minute_aggregations_topic_name,
    bootstrap_servers=config.kafka_broker_url,
    auto_offset_reset='earliest',
    enable_auto_commit=True,
    group_id=config.kafka_group_id,
    value_deserializer=lambda x: json.loads(x.decode()))

loop = asyncio.get_running_loop()
loop.create_task(one_min_aggregations_consumer.start())
loop.create_task(five_min_aggregations_consumer.start())
loop.create_task(ten_min_aggregations_consumer.start())


@sio.event
async def connect(sid: str, environ: dict):
    logger.info(f'{sid} connected')


@sio.event
def connect_error(e):
    logger.info(f'Server connect failed: {e}')


@sio.event
async def disconnect(sid):
    logger.info(f'Disconnected {sid}')


@sio.event
async def register_room(sid: str, data):
    for room_id in data['rooms']:
        logger.info(f'rooms registered: {room_id}')
        sio.enter_room(sid, room_id)


@sio.event
async def consume_1_min_aggregations(sid: str, data):
    async for record in one_min_aggregations_consumer:
        logger.info(f'Reporting for 1\': {record}')
        await sio.emit(
            config.one_minute_aggregations_event_name,
            {
                'id': record.value['video_uid'],
                'count': record.value['count']
            },
            to=record.value['video_uid']
        )


@sio.event
async def consume_5_min_aggregations(sid: str, data):
    async for record in five_min_aggregations_consumer:
        logger.info(f'Reporting for 5\': {record}')
        await sio.emit(
            config.five_minute_aggregations_event_name,
            {
                'id': record.value['video_uid'],
                'count': record.value['count']
            },
            to=record.value['video_uid']
        )


@sio.event
async def consume_10_min_aggregations(sid: str, data):
    async for record in ten_min_aggregations_consumer:
        logger.info(f'Reporting for 10\': {record}')
        await sio.emit(
            config.ten_minute_aggregations_event_name,
            {
                'id': record.value['video_uid'],
                'count': record.value['count']
            },
            to=record.value['video_uid']
        )
