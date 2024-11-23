import logging
from .models import ErrorLog

class DatabaseHandler(logging.Handler):
    def emit(self, record):
        try:
            log_entry = self.format(record)
            ErrorLog.objects.create(
                error_type=record.levelname,
                error_message=log_entry,
                stack_trace=str(record.exc_info)
            )
        except Exception as e:
            pass  # Si ocurre un error al guardar el log, no lo registramos de nuevo

