from processors.ActivityProcessor import ActivityProcessor


class ActivityRepository():
    def __init__(self, activity_json):
        self.activity_json = activity_json
        self.activity_processor = ActivityProcessor(activity_json)

    def get_activity_years(self):
        return self.activity_processor.get_activities_years()

    def get_activities_df(self, df_shoes, start_year=None, end_year=None):
        return self.activity_processor.merge_with_shoes(df_shoes).filter_by_year_range(
            start_year, end_year).get_dataframe()

    def get_cumulative_shoe_distance_df(self):
        return self.activity_processor.get_cumulative_shoe_distance()
