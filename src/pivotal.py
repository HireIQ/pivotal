from lxml import etree
import requests

PIVOTAL_BASE_URL = 'https://www.pivotaltracker.com/services/v3/projects/'


class Story(object):
    '''
    A story in pivotal.
    '''
    def __init__(self):
        self.story_id = None
        self.name = None
        self.url = None
        self.current_state = None

    @staticmethod
    def from_xml(xml):
        story = Story()
        for field in xml:
            if field.tag == 'id':
                story.story_id = int(field.text)
            elif hasattr(story, field.tag):
                setattr(story, field.tag, field.text)
        return story


class Project(object):
    '''
    A connection to the pivotal api.
    '''
    def __init__(self, project, token):
        self.project = project
        self.token = token

    def _request(self, method, uri, **kwargs):
        url = "%s/%d/%s" % (PIVOTAL_BASE_URL, self.project, uri)
        if 'headers' not in kwargs:
            kwargs['headers'] = {}
        kwargs['headers']['X-TrackerToken'] = self.token
        kwargs['headers']['Content-type'] = 'application/xml'
        result = requests.request(method, url, **kwargs)
        result.raise_for_status()
        return etree.fromstring(result.content)

    def update_story(self, story, **kwargs):
        '''Update a story in this projects'''
        if isinstance(story, Story):
            story = story.id
        root = etree.Element("story")
        for field, val in kwargs.items():
            el = etree.SubElement(root, field)
            el.text = val
        body = etree.tostring(root)
        return Story.from_xml(self._request('put', "stories/%d" % story, data=body))

    def filter_stories(self, filter_string):
        response = self._request('get', "stories?filter=%s" % filter_string)
        stories = []
        for story_xml in response.iterchildren(tag="story"):
            stories.append(Story.from_xml(story_xml))
        return stories
