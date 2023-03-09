import logging
from pythonjsonlogger import jsonlogger


class JsonFormatter(jsonlogger.JsonFormatter):
    def add_fields(self, log_record: dict[str, any], record: logging.LogRecord, message_dict: dict[str, any]) -> None:
        super(JsonFormatter, self).add_fields(log_record, record, message_dict)
        if not log_record.get('timestamp'):
            # Add timestamp field if it doesn't exist
            log_record['timestamp'] = record.created