import logging


class BaseError(Exception):
    def __init__(self, message, status_code):
        self.message = message
        self.status_code = status_code
        logging.error(self.message)
    
    def __str__(self):
        return f'error: {self.message}\t code: {self.status_code}'


class ServiceUnavailableError(BaseError):
    def __init__(self):
        super().__init__(message='Image provider service is unavailable', status_code=503)


class InvalidImageIdError(BaseError):
    def __init__(self):
        super().__init__(message = 'Invalid image id', status_code = 400)
        

class ImageNotFoundError(BaseError):
    def __init__(self):
        super().__init__(message = 'Image not found', status_code = 404)
        
        
class InvalidImageError(BaseError):
    def __init__(self):
        super().__init__(message = 'Invalid image', status_code = 400)
        
        
class DownloadTimeoutError(BaseError):
    def __init__(self):
        super().__init__(message = 'Download request timed out', status_code = 408)
        
        
class NoIdsProvidedError(BaseError):
    def __init__(self):
        super().__init__(message = 'No image IDs were provided', status_code = 400)
