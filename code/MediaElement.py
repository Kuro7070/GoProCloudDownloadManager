
class MediaElement:
    def __init__(self, id, filename, date, fileSize, fileExtension):
        self.id = id
        self.filename= filename
        self.date = date
        self.fileSize = fileSize
        self.fileExtension = fileExtension
        self.thumbnail = None

    def setThumbnail(self, url):
        self.thumbnail = url
