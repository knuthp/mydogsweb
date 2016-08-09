import dropbox
from os import environ



class ImageService:
    def __init__(self):
        self.dbx = dropbox.Dropbox(environ['DROPBOX_ACCCESS_TOKEN'])

    def getLatest(self):
        files = self.dbx.files_list_folder('/2016-08-06').entries
        for entry in files:
            print(entry.name)
        sortedList = sorted(files, key=lambda r: r.name, reverse=True)
        latestFileMeta = sortedList[0]
        md, res = self.dbx.files_download(latestFileMeta.path_lower)
        return { 'name' : latestFileMeta.name,
                'content' : res.content}

    
if __name__ == '__main__':
    imageService = ImageService()
    imageData = imageService.getLatest()
    
    print("Last image=" + imageData['name'])
    print("Size=" + str(len(imageData['content'])))
