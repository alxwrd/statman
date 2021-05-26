

class Profile:

    def __init__(self, data):
        self.data = data

    @property
    def username(self):
        return self.data.get("username").split("#")[0]

    @property
    def weekly_properties(self):
        return self.data.get("weekly", {}).get("mode", {}).get("br_all", {}).get("properties", {})

    @property
    def games_played(self):
        return self.weekly_properties.get("matchesPlayed", 0.0)

    @property
    def damage_per_game(self):
        try:
            return (
                self.weekly_properties.get("damageDone", 0.0)
                / self.games_played
            )
        except ZeroDivisionError:
            return 0.0

    @property
    def kills(self):
        return self.weekly_properties.get("kills", 0.0)

    @property
    def headshots(self):
        return self.weekly_properties.get("headshots", 0.0)

    @property
    def assists(self):
        return self.weekly_properties.get("assists", 0.0)

    @property
    def kd(self):
        return self.weekly_properties.get("kdRatio", 0.0)

    @property
    def caches_opened(self):
        return self.weekly_properties.get("objectiveBrCacheOpen", 0.0)

    @property
    def revives(self):
        return self.weekly_properties.get("objectiveReviver", 0.0)

    @property
    def damage_done(self):
        return self.weekly_properties.get("damageDone", 0.0)
