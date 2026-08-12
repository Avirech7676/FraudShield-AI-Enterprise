class TimelineService:

    @staticmethod
    def sort(timeline):

        return sorted(

            timeline,

            key=lambda x:

            x["timestamp"]

        )

    @staticmethod
    def latest_event(case):

        if len(case["timeline"]) == 0:

            return None

        return sorted(

            case["timeline"],

            key=lambda x:

            x["timestamp"],

            reverse=True

        )[0]
