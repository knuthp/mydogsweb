import dropbox
from os import environ
from datetime import datetime
from dropbox.exceptions import ApiError
import logging
import re



class ImageService:
    def __init__(self):
        self.dbx = dropbox.Dropbox(environ['DROPBOX_ACCCESS_TOKEN'])

    def getLatest(self):
        datesSorted = sorted(self.getAvailableDates(), reverse=True);
        latestDay = datesSorted[0]
        files = self.dbx.files_list_folder('/' + self.__dateToIsoString(latestDay)).entries
        sortedList = sorted(files, key=lambda r: r.name, reverse=True)
        latestFileMeta = sortedList[0]
        res = self.dbx.files_download(latestFileMeta.path_lower)[1]
        return {'name' : latestFileMeta.name,
                'path' : latestFileMeta.path_lower,
                'content' : res.content}



    def getForDay(self, day):
        dayString = self.__dateToIsoString(day)
        try :
            files = self.dbx.files_list_folder('/' + dayString).entries
            filenames = [x.path_lower for x in files]
            return filenames
        except ApiError:
            logging.warn("Not a valid day: %s", dayString)
            return []
        
        
    def getAvailableDates(self):
        dateRegex = '\d\d\d\d-\d\d-\d\d'
        files = self.dbx.files_list_folder('').entries
        dateStrings = [entry.name for entry in files if re.match(dateRegex, entry.name)]
        dates = [datetime.strptime(dateString, "%Y-%m-%d") for dateString in dateStrings]
        return dates
    
    def getImage(self, path):
        res = self.dbx.files_download(path)[1]
        return res.content
        


    def __dateToIsoString(self, day):
        return str(day.year) + '-' + str(day.month).zfill(2) + '-' + str(day.day).zfill(2)
    
if __name__ == '__main__':
    imageService = ImageService()
    print(imageService.getLatest()['path'])
