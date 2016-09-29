import os

CONTENT_RANGE_HEADER = 'Content-Range'

ALLOWED_MIMETYPES = [
    'video/x-msvideo',
    'image/x-ms-bmp',
    'application/msword',
    'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
    'video/x-flv',
    'image/gif',
    'image/jpeg',
    'video/quicktime',
    'audio/mpeg',
    'video/mp4',
    'application/vnd.oasis.opendocument.formula',
    'application/vnd.oasis.opendocument.graphics',
    'application/vnd.oasis.opendocument.presentation',
    'application/vnd.oasis.opendocument.spreadsheet',
    'application/vnd.oasis.opendocument.text',
    'application/pdf',
    'image/png',
    'application/vnd.ms-powerpoint',
    'application/vnd.openxmlformats-officedocument.presentationml.presentation',
    'text/plain',
    'text/rtf',
    'image/tiff',
    'audio/x-wav',
    'video/x-ms-asf',
    'application/vnd.ms-excel',
    'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
]