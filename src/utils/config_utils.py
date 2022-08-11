from dotenv import dotenv_values


class ConfigUtils:
    def __init__(self):
        config = dotenv_values("config/.env")
        self.log_level = config.get('LOG_LEVEL')
        self.kafka_broker_url = config.get('KAFKA_BROKER_URL')
        self.kafka_group_id = config.get('KAFKA_GROUP_ID_FOR_CONSUMER')
        self.one_minute_aggregations_topic_name = config.get('LIKES_1_MIN_AGGREGATION_TOPIC_NAME')
        self.five_minute_aggregations_topic_name = config.get('LIKES_5_MIN_AGGREGATION_TOPIC_NAME')
        self.ten_minute_aggregations_topic_name = config.get('LIKES_10_MIN_AGGREGATION_TOPIC_NAME')
        self.one_minute_aggregations_event_name = config.get('ONE_MINUTE_AGGREGATIONS_EVENT_NAME')
        self.five_minute_aggregations_event_name = config.get('FIVE_MINUTE_AGGREGATIONS_EVENT_NAME')
        self.ten_minute_aggregations_event_name = config.get('TEN_MINUTE_AGGREGATIONS_EVENT_NAME')

    @staticmethod
    def get_config() -> 'ConfigUtils':
        return ConfigUtils()
