class VersionManager:

    @staticmethod
    def next_version(existing):

        if len(existing) == 0:

            return "v1.0"

        latest = existing[-1]["version"]

        major, minor = latest.replace("v", "").split(".")

        major = int(major)

        minor = int(minor) + 1

        return f"v{major}.{minor}"