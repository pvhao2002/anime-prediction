class Movie:
    def __init__(self):
        self.rank = None
        self.name = None
        self.japanese_name = None
        self.type = None
        self.episodes = None
        self.studio = None
        self.release_season = None
        self.tags = None
        self.rating = None
        self.release_year = None
        self.end_year = None
        self.description = None
        self.content_warning = None
        self.related_manga = None
        self.related_anime = None
        self.voice_actors = None
        self.staff = None

    def set_rank(self, rank) -> 'Movie':
        self.rank = rank
        return self

    def set_name(self, name) -> 'Movie':
        self.name = name
        return self

    def set_japanese_name(self, japanese_name) -> 'Movie':
        self.japanese_name = japanese_name
        return self

    def set_type(self, type) -> 'Movie':
        self.type = type
        return self

    def set_episodes(self, episodes) -> 'Movie':
        self.episodes = episodes
        return self

    def set_studio(self, studio) -> 'Movie':
        self.studio = studio
        return self

    def set_release_season(self, release_season) -> 'Movie':
        self.release_season = release_season
        return self

    def set_tags(self, tags) -> 'Movie':
        self.tags = tags
        return self

    def set_rating(self, rating) -> 'Movie':
        self.rating = rating
        return self

    def set_release_year(self, release_year) -> 'Movie':
        self.release_year = release_year
        return self

    def set_end_year(self, end_year) -> 'Movie':
        self.end_year = end_year
        return self

    def set_description(self, description) -> 'Movie':
        self.description = description
        return self

    def set_content_warning(self, content_warning) -> 'Movie':
        self.content_warning = content_warning
        return self

    def set_related_manga(self, related_manga) -> 'Movie':
        self.related_manga = related_manga
        return self

    def set_related_anime(self, related_anime) -> 'Movie':
        self.related_anime = related_anime
        return self

    def set_voice_actors(self, voice_actors) -> 'Movie':
        self.voice_actors = voice_actors
        return self

    def set_staff(self, staff) -> 'Movie':
        self.staff = staff
        return self

    def to_dict(self):
        return {
            'Rank': self.rank,
            'Name': self.name,
            'Japanese_name': self.japanese_name,
            'Type': self.type,
            'Episodes': self.episodes,
            'Studio': self.studio,
            'Release_season': self.release_season,
            'Tags': self.tags,
            'Rating': self.rating,
            'Release_year': self.release_year,
            'End_year': self.end_year,
            'Description': self.description,
            'Content_Warning': self.content_warning,
            'Related_Mange': self.related_manga,
            'Related_anime': self.related_anime,
            'Voice_actors': self.voice_actors,
            'Staff': self.staff
        }
