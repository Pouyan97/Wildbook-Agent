# Requires Google api client library
# pip install --upgrade google-api-python-client

from googleapiclient.discovery import build

class YouTube:
    def __init__(self, KEY, db=None):
        self._YOUTUBE_API_SERVICE_NAME = 'youtube'
        self._YOUTUBE_API_VERSION = 'v3'
        self._KEY = KEY
        self.youtube = build(self._YOUTUBE_API_SERVICE_NAME, self._YOUTUBE_API_VERSION, 
                             developerKey=self._KEY)
        self.db = db
        self.nextPageToken = None
        self.page = 1
    
    # Uses youtube.search() API method
    def search(self, q, limit=1, saveTo=False):
        ''' 
        q - search query, (ex. "Whale Shark")
        limit - number of results (ex. 10 or 100)
        fields - Retrieve only selected fields (ex. True, False)
        save - Saves all retrieved videos to database (ex. True, False)
        '''
        if (saveTo and not self.db):
            saveTo = False
            print("Please provide 'db' argument with an instance to database to save video(s).")
            
        # Going through pages in result
        self.results = []
        while(limit > 0):
            print("Working with page", self.page)
            
            # Quering the result
            searchResult = self.youtube.search().list(
                q=q,
                part='snippet',
                fields='nextPageToken,items(id,snippet(publishedAt,title))',
#                 fields='nextPageToken,pageInfo(totalResults),items(id,snippet(publishedAt,channelId,title,description))' if fields else '*',
                type='video',
                maxResults=50 if limit>50 else limit,
                pageToken=self.nextPageToken if self.nextPageToken else ''
            ).execute()
            items = searchResult['items']
            
            self.nextPageToken = searchResult['nextPageToken']
            self.page += 1
            limit -= 50

            # Going through each result
            modifiedResult = []
            for item in items:

                # Quering more details for this result
                details = self.videos(item['id']['videoId'], fields=True)
                for prop in details[0]:
                    try:
                        item[prop].update(details[0][prop])
                    except KeyError:
                        item[prop] = details[0][prop]

                # WILDBOOK FORMAT
                # try:
                newItem = {
                    "_id": item['id']['videoId'],
                    "videoID": item['id']['videoId'],
                    "title": {
                        "original": item['snippet'].get('title', None),
                        "eng": None, #[Microsoft translate]
                    },
                    "tags": {
                        "original": item['snippet'].get('tags', []),
                        "eng": [], #[Microsoft translate]
                    },
                    "description": {
                        "original": item['snippet'].get('description', None),
                        "eng": None, #[Microsoft translate]
                    },
                    "OCR": {
                        "original": [], #[Azure]
                        "eng": [], #[Azure, Microsoft translate]
                    },
                    "url": 'https://youtu.be/' + item['id']['videoId'],
                    "animalsID": [], #[Wildbook]
                    "curationStatus": None, #[Wildbook]
                    "curationDecision": None, #[Wildbook]
                    "publishedAt": item['snippet'].get('publishedAt', None),
                    "uploadedAt": None, #[YouTube]
                    "duration": None, #[YouTube]
                    "regionRestriction": None, #[YouTube]
                    "viewCount": item['statistics'].get('viewCount', None),
                    "likeCount": item['statistics'].get('likeCount', None),
                    "dislikeCount": item['statistics'].get('dislikeCount', None),
                    "recordingDetails": {
                        "location": None, #[YouTube]
                        "date": None, #[YouTube]
                    },
                    "encounter": {
                        "locationIDs": [], #[Wildbook]
                        "dates": [], #[Wildbook]
                    },
                    "fileDetails": None, #[YouTube]
                    "relevant": None,
                    "wild": None
                }
                # except:
                #     print(item)

                # Saving item in database
                if (saveTo):
                    self.db.addVideo(newItem, saveTo)

                modifiedResult.append(newItem)
            
            # Appeding result to all previous search results
            self.results += modifiedResult
        
        print("Done!")
        return self.results
    
        
    
    # Retrueve info about specific video(s)
    def videos(self, id, fields=False):
        searchResult = self.youtube.videos().list(
            part='snippet,statistics',
            fields='items(snippet(title,description,tags))' if fields else '*',
            id=id
        ).execute()

        return searchResult['items']
    
# from Youtube import Youtube
# yt = Youtube(<KEY>)
# yt.videos(<video_id>, True)