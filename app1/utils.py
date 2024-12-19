import logging
from .models import ErrorLog

class DatabaseHandler(logging.Handler):
    """
    Un manejador personalizado de logging que guarda los registros de errores en la base de datos.

    - Extiende la clase 'logging.Handler' para manejar registros de log.
    - Guarda los logs en el modelo 'ErrorLog'.
    - Maneja errores como tipo, mensaje y trazas de error si están disponibles.

    Methods:
        emit(record):
            Recibe un registro de log y lo guarda en la base de datos como una instancia de ErrorLog.
    """
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

