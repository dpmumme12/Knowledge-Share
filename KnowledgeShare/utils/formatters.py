import logging
from xml.sax.saxutils import escape

class XMLLogFormatter(logging.Formatter):
    """
    Custom formatter overwritting the default logging.Formatter class.
    Overrides the Formatter.format() function to provide structured
    XML log.
    """

    def format(self, record):
        super().format(record)
        log_time = self.formatTime(record)
        log = (F'<log><level>{record.levelname}</level>'
               F'<time>{log_time}</time>'
               F'<module>{record.module}</module>'
               F'<process>{record.process:d}</process>'
               F'<thread>{record.thread:d}</thread>'
               F'<message>{escape(record.message)}</message>')
        if record.exc_text:
            log = ''.join([log, '<traceback>', escape(record.exc_text), '</traceback>'])
        log += '</log>'

        return log
