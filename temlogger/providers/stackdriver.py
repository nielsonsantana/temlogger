from google.cloud.logging.handlers import CloudLoggingHandler
from .base import FormatterBase


class StackDriverFormatter(FormatterBase):

    def format(self, record):
        message = super().format(record)
        return message


class StackDriverLoggingHandler(CloudLoggingHandler):

    def ensure_transport_worker_is_running(self):
        """
        Ensures that transport worker is running when any log is done
        """
        if not self.transport.worker.is_alive:
            self.transport.worker.start()

    def emit(self, record):
        self.ensure_transport_worker_is_running()
        message = super(CloudLoggingHandler, self).format(record)
        self.transport.send(record, message, resource=self.resource, labels=self.labels)
