from sqlalchemy import create_engine
from sqlalchemy.types import String
import pandas as pd


engine = create_engine('postgresql://tiAversa:saltlake@localhost:5432/netflix_listing')

archived_netflix_listing = pd.read_csv(r'netflix_titles.csv')

archived_netflix_listing.head()

dir_staging = {"show_id": String(), "type": String(), "title": String(), "director": String(), "cast": String(), "country": String(), "date_added": String(), "release_year": String(), "rating": String(), "duration": String()}

archived_netflix_listing.to_sql('stat_staging', engine, if_exists='append', index=False, dtype=dir_staging)