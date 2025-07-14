#!/usr/bin/env python
# coding: utf-8
# %%
# ETL notebook for HDI time series

# %%
import pandas as pd
import re


# %%
source_file = '../source/HDR25_Composite_indices_complete_time_series.csv'


# %%
# !head ../source/HDR25_Composite_indices_complete_time_series.csv


# %%
medadata_cols = ["iso3", "country", "hdicode", "region"]
data = pd.read_csv(source_file, encoding='latin1', na_values=['..'],
                   usecols=lambda col: col in medadata_cols or (re.match(r'hdi_\d+', col) is not None))


# %%
data.head()


# %%
data = data.dropna(how='all', axis=1).dropna(how='all')


# %%
data


# %%
data_ = data.drop(['hdicode','iso3','region'], axis=1).set_index('country').stack()


# %%
data_ = data_.reset_index()
data_.columns = ['country', 'year', 'hdi']


# %%
data_


# %%
data_['country'] = data_['country'].str.strip()


# %%
data_['year'] = data_['year'].map(lambda x: x[4:]).astype(int)


# %%
from ddf_utils.str import to_concept_id


# %%
country = data_[['country']].drop_duplicates().copy()

country['name'] = country['country'].copy()
country['country'] = country['country'].map(to_concept_id)


# %%
country.to_csv('../../ddf--entities--country.csv', index=False)


# %%

# %%
data_['country'] = data_['country'].map(to_concept_id)


# %%

data_.dropna(how='any').to_csv('../../ddf--datapoints--hdi--by--country--year.csv', index=False)


# %%

# %%
concepts = pd.DataFrame([['hdi', 'Human Development Index', 'measure'],
                         ['country', 'Country', 'entity_domain'],
                         ['year', 'Year', 'time'],
                         ['name', 'Name', 'string']])


# %%
concepts.columns = ['concept', 'name', 'concept_type']


# %%
concepts


# %%
concepts.to_csv('../../ddf--concepts.csv', index=False)


# %%





# %%





# %%





# %%
