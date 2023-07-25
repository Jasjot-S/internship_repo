"""
"""
import dateparser
from datetime import datetime
from youtubesearchpython.core.channel import ChannelCore
from youtubesearchpython.core.componenthandler import getValue, getVideoId


class ChannelDetails(ChannelCore):
    """
    """
    REQUEST_PARAMS = {
        "videos": "EgZ2aWRlb3PyBgQKAjoA",
        "about": "EgVhYm91dPIGBAoCEgA%3D"
    }

    def __init__(self, channel_id: str, with_videos: bool):
        if with_videos:
            super().__init__(channel_id=channel_id, request_params=self.REQUEST_PARAMS["videos"])
        else:
            super().__init__(channel_id=channel_id, request_params=self.REQUEST_PARAMS["about"])
        self.prepare_request()
        self.data = self.syncPostRequest()
        self.with_videos = with_videos
        self.parse_response()

    def convert_to_number(self, value=None):

        multipliers = {
            'k': 1000,
            'K': 1000,
            'M': 1000000,
            'B': 1000000000,
            'T': 1000000000000
        }
        if ' ' in value:
            value = value.split(' ')
            value = ''.join(value[0])
        suffix = value[-1]
        if suffix in multipliers:
            number = int(float(value[:-1]) * multipliers[suffix])
        else:
            number = int(float(value))
     
        return number
    
    def to_seconds(self, timestr):
        seconds= 0
        try:
            for part in timestr.split(':'):
                seconds= seconds*60 + int(part, 10)
            return seconds
        except Exception as e:
            print("VIDEO IS LIVE NOW")
            return seconds

    def join_date(self, date):
        date_obj = datetime.strptime(date, "%b %d, %Y")
        output_date = date_obj.strftime("%Y-%m-%d")
        return output_date

    def _getVideoComponent(self, data):
        publishedat = getValue(data, ["publishedTimeText", "simpleText"])
        publishedat = dateparser.parse(publishedat)
        publishedat = publishedat.strftime("%Y-%m-%d")
        component = {
            "ytvideos":True,
            "vid": getValue(data, ["videoId"]),
            "title": getValue(data, ["title", "runs", 0, "text"]),
            "description": getValue(data, ["descriptionSnippet", "runs", 0, "text"]),
            "publishedat": publishedat,
            "duration": self.to_seconds(getValue(data, ["lengthText", "simpleText"])),
            "viewcount": ''.join(filter(str.isdigit, getValue(data, ["viewCountText", "simpleText"]))),
            "thumbnails": getValue(data, ['thumbnail', 'thumbnails', 0, "url"])
        }
        return component

    def _getChannelComponent(self, data):
        channel = {
            "ytchannels":True,
            "channelid": getValue(data, ["header", "c4TabbedHeaderRenderer", "channelId"]),
            "title": getValue(data, ["header", "c4TabbedHeaderRenderer", "title"]),
            "description": getValue(data, ["metadata", "channelMetadataRenderer", "description"]),
            "thumbnail": getValue(data, ["header", "c4TabbedHeaderRenderer", "banner", "thumbnails", 0, "url"]),
            "subscriber": self.convert_to_number(value=getValue(data, ["header", "c4TabbedHeaderRenderer", "subscriberCountText", "simpleText"])),
            "username": getValue(data, ["header", "c4TabbedHeaderRenderer", "channelHandleText", "runs", 0, "text"]),
            "video_count": self.convert_to_number(getValue(data, ["header", "c4TabbedHeaderRenderer", "videosCountText", "runs", 0, "text"])),
            "isFamilySafe": getValue(data, ["metadata", "channelMetadataRenderer", "isFamilySafe"]),
            "facebookProfileId": getValue(data, ["metadata", "channelMetadataRenderer", "facebookProfileId"]),
            "brands_keywords": getValue(data, ["microformat", "microformatDataRenderer", "tags"])
        }
        return channel


    def parse_response(self):
        response = self.data.json()

        result = self._getChannelComponent(response)

        for param in getValue(response, ["responseContext", "serviceTrackingParams", 0, "params"]):
            if param["key"] == "is_monetization_enabled":
                result["is_monetization_enabled"] = param["value"]
                break
        videos = []

        for tab in getValue(response, ["contents", "twoColumnBrowseResultsRenderer", "tabs"]):

            title = getValue(tab, ["tabRenderer", "title"])


            if title == "Videos" and self.with_videos:
                contents = getValue(tab,
                    ["tabRenderer", "content", "richGridRenderer", "contents"]
                )

                for content in contents:
                    try:
                        videoRenderer = getValue(content, ["richItemRenderer", "content", "videoRenderer"])
                        videos.append(self._getVideoComponent(videoRenderer))
                    except:
                        pass
                break
            elif title == "About" and not self.with_videos:
                channelMetadata = getValue(tab,
                    ["tabRenderer", "content", "sectionListRenderer", "contents", 0, "itemSectionRenderer", "contents", 0, "channelAboutFullMetadataRenderer"]
                )

                result["country"] = getValue(channelMetadata, ["country", "simpleText"])
                result["publishedat"] = self.join_date(date=getValue(channelMetadata,[ "joinedDateText", "runs", 1, "text"]))

        result['videos'] = videos

        self.result = result
        return result

