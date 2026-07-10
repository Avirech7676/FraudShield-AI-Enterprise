class VersionManager:

    @staticmethod
    def next_version(models):

        if len(models) == 0:

            return "v1.0"

        latest = models[-1]["version"]

        major, minor = latest.replace(

            "v",

            ""

        ).split(".")

        return f"v{major}.{int(minor)+1}"