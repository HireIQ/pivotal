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


class Project(object):
    '''
    A connection to the pivotal api.
    '''
    def __init__(self, project, token):
        self.project = project
        self.token = token

    def _get(self, uri):
        url = "%s/%d/%s" % (PIVOTAL_BASE_URL, self.project, uri)
        result = requests.get(url, headers={"X-TrackerToken": self.token})
        result.raise_for_status()
        return etree.fromstring(result.content)

    def filter_stories(self, filter_string):
        response = self._get("stories?filter=%s" % filter_string)
        stories = []
        for story_xml in response.iterchildren(tag="story"):
            story = Story()
            for field in story_xml:
                if field.tag == 'id':
                    story.story_id = int(field.text)
                elif hasattr(story, field.tag):
                    setattr(story, field.tag, field.text)
            stories.append(story)
        return stories
