from processors.ShoeProcessor import ShoeProcessor


class AthleteRepository():
    def __init__(self, athlete_data):
        self.athlete_data = athlete_data
        self.shoe_processor = ShoeProcessor(self.athlete_data)

    def get_profile(self):
        return self.athlete_data or {}

    def get_shoes_names(self):
        return self.shoe_processor.get_shoe_name_list()

    def get_shoes_df(self, selected_shoes=[]):
        return self.shoe_processor.filter_shoes_by_name(selected_shoes).get_dataframe()
