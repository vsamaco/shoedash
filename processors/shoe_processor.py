import pandas as pd


class ShoeProcessor():
    def __init__(self, df_shoes: pd.DataFrame):
        self.df = df_shoes.copy()

    def get_dataframe(self):
        return self.df

    def get_shoe_name_list(self):
        return sorted(self.df['name'].unique().tolist())

    def filter_shoes_by_name(self, shoe_names):
        if len(shoe_names) > 0:
            self.df = self.df[self.df['name'].isin(shoe_names)]
        return self
