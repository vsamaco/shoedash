import pandas as pd
from adapters.base_data_adapter import BaseDataAdapter, get_gear
from processors.activity_processor import ActivityProcessor
from processors.shoe_processor import ShoeProcessor


class GearSyncService():
    def __init__(self, activity_processor: ActivityProcessor, shoe_processor: ShoeProcessor, data_adapter: BaseDataAdapter):
        self.activity_processor = activity_processor
        self.shoe_processor = shoe_processor
        self.data_adapter = data_adapter

    def get_retired_shoes(self):
        df_shoes = self.shoe_processor.get_dataframe()
        return self.activity_processor.get_missing_gear_ids(
            df_shoes)

    def sync_retired_shoes(self):
        df_shoes = self.shoe_processor.get_dataframe()
        missing_gear_ids = self.activity_processor.get_missing_gear_ids(
            df_shoes)

        if not missing_gear_ids:
            return

        missing_shoes = []
        mode = self.data_adapter.get_mode()

        for gear_id in missing_gear_ids:
            gear_data = get_gear(self.data_adapter, mode, gear_id)
            if gear_data:
                missing_shoes.append(gear_data)

        df_missing_shoes = pd.DataFrame(missing_shoes)
        df_missing_shoes.rename(columns={
            'id': 'gear_id', 'converted_distance': 'total_distance_mi'}, inplace=True)

        self.shoe_processor.merge_retired_shoes(df_missing_shoes)

        return missing_shoes
