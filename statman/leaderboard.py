

class Leaderboard:

    @staticmethod
    def place(i):
        try:
            return ["🥇", "🥈", "🥉"][i]
        except IndexError:
            return "▫️"

    def __init__(self, profiles):
        profiles.sort(reverse=True, key=lambda profile: profile.damage_per_game)
        self.profiles = profiles

    def __str__(self):
        return "\n".join([
            f"{Leaderboard.place(i)} {profile.username} - {profile.damage_per_game:.2f} dpg"
            for i, profile in enumerate(self.profiles)
        ])

    def as_message(self):
        return str(self).replace("_", "\\_")