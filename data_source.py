from datetime import datetime

class DataSource:

    def __init__(self):
        self.fields = ['trailText', 'headline', 'liveBloggingNow', 'standfirst', 'commentable', 'thumbnail', 'byline']
        self.tags = []
        self.content_type = 'article'
        self.page_size = 10
        self.show_media = None
        self.lead_content = None
        self.section_name = None
        self.from_date = None
        self.show_editors_pics = False
        self.show_most_viewed = False

    def fetch_data(self, client):
        criteria = self._build_criteria()
        data = client.search(**criteria)
        return list(data)

    def _build_criteria(self):
        criteria = {}

        if self.fields:
            criteria['show-fields'] = ','.join(self.fields)

        if self.section_name:
            criteria['section'] = self.section_name

        if self.content_type:
            self.tags.append('type/%s' % self.content_type)

        if self.tags:
            criteria['tag'] = ','.join(self.tags)

        if self.show_editors_pics:
            criteria['show-editors-picks'] = 'true'

        if self.show_most_viewed:
            criteria['show-most-viewed'] = 'true'

        if self.lead_content:
            criteria['lead-content'] = self.lead_content

        if self.page_size:
            criteria['page-size'] = self.page_size

        if self.show_media:
            criteria['show-media'] = self.show_media

        if self.from_date:
            criteria['from-date'] = self.from_date

        return criteria


class CultureDataSource(DataSource):
    def __init__(self):
        DataSource.__init__(self)
        self.section_name = 'culture'


class SportDataSource(DataSource):
    def __init__(self):
        DataSource.__init__(self)
        self.section_name = 'sport'


class PicOfDayDataSource(DataSource):
    def __init__(self):
        DataSource.__init__(self)
        self.content_type = 'picture'
        self.tags = ['artanddesign/series/picture-of-the-day']
        self.page_size = 1
        self.show_media = 'picture'


class MostViewedDataSource(DataSource):
    def __init__(self):
        DataSource.__init__(self)
        today = str(datetime.now().date())
        self.from_date = today
        self.show_most_viewed = True
