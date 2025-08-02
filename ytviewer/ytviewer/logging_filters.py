import logging
from yt_dlp import DownloadError


class InfoOnlyFilter(logging.Filter):
    def filter(self, record):
        return record.levelno == logging.INFO


class ExcludeUnavailableVideoFilter(logging.Filter):
    def filter(self, record):
        if record.exc_info is not None:
            exception = record.exc_info[1]

            return not (isinstance(exception, DownloadError)
                        and 'Video unavailable' in str(exception))

        return True
