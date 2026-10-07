from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]
DATA_PATH = PROJECT_ROOT / 'data' / 'raw'
PROCESSED_PATH = PROJECT_ROOT / 'data' / 'processed'

PP_FILENAME = 'ppd_data*.csv'
EPC_FILENAME = 'EDC_OXFORDSHIRE_2015_2025.csv'
EPC_COLS = [
    'certificate_number', 'address1', 'address2', 'address3', 'postcode',
    'posttown', 'address', 'local_authority', 'local_authority_label',
    'built_form', 'construction_age_band', 'current_energy_efficiency',
    'current_energy_rating', 'energy_consumption_current', 'extension_count', 'floor_height', 'heating_cost_current',
    'inspection_date', 'lodgement_date', 'number_habitable_rooms',
    'number_heated_rooms', 'potential_energy_efficiency', 'property_type',
    'tenure', 'total_floor_area', 'transaction_type', 'uprn', 'uprn_source'
]
TARGET_LOCAL_AUTHORITIES = ['E07000177', 'E07000178', 'E07000180', 'E07000179', 'E07000181']
PP_ADDRESS_COLS = ['paon', 'saon', 'street', 'locality', 'postcode']
EPC_ADDRESS_COLS = ['address1', 'address2', 'address3', 'postcode']
FINAL_COLS = ['unique_id', 'price_paid', 'deed_date', 'address_x', 'saon', 'paon', 'street', 'locality', 'town', 'district',  
                'postcode', 'property_type_x', 'new_build', 'estate_type',  'transaction_category',  'certificate_number', 
                'built_form', 'construction_age_band', 'current_energy_efficiency', 'current_energy_rating', 
                'energy_consumption_current', 'extension_count', 'floor_height', 'heating_cost_current', 
                'inspection_date', 'lodgement_date', 'number_habitable_rooms', 'number_heated_rooms', 
                'potential_energy_efficiency', 'property_type_y', 'tenure', 'total_floor_area', 
                'transaction_type', 'uprn', 'uprn_source', 'inspection_to_sale']
RENAME_MAP = {'property_type_x':'property_subtype', 'property_type_y':'property_type', 'address_x': 'address'}
AGE_BINS = [0, 365, 1095, 1825, 3650, float('inf')]
AGE_LABELS = ['0-1 years', '1-3 years', '3-5 years', '5-10 years', '10 years+']
EPC_VALIDITY_YEARS = 10
THRESHOLDS = {'min_floor_area': 9, # exclude floor areas <=9 sqm
              'large_floor_area': 2000, # exclude floor areas > 2000 sqm and <= 7 rooms or rooms missing
              'large_floor_area_rooms':7, # exclude floor areas > 2000 sqm and <= 7 rooms or rooms missing
              'min_floor_height':1.5, # values < 1.5 m converted to null (not excluded)
              'eff_cutoff':110, # exclude efficiency > 110 and consumption > 200 for flats/maisonettes
              'consump_cutoff':200, # exclude efficiency > 110 and consumption > 200 for flats/maisonettes
              'eff_cutoff_types':['Flat', 'Maisonette'], # exclude efficiency > 110 and consumption > 200 for flats/maisonettes
               'const_age_len_min': 4 } # exclude construction age band values < 4 characters
PLACEHOLDERS = {'property_type': 'Not Recorded', 'built_form': 'Not Recorded', 'tenure': 'unknown'}
PROCESSED_FILENAME = 'pp_epc_oxfordshire_2015_2025.parquet'

