"""
You will need a .env file for passing connection parameters for connection to PostGIS/PostGres database.
Update your schema name on line 20
Usage:
    python geojson_to_postgis.py --source_file <path to your geojson file --table <table_name> --tag <optional table tag>
"""
import json
import geopandas as gpd
from sqlalchemy import *
from dotenv import load_dotenv
import argparse
import os
import sys

load_dotenv()
# Set up database connection engine
db_connection_url = os.getenv('sandboxurl')
engine = create_engine(db_connection_url)

schema_name = '<your_schema_here>'


def custom_usage_message():
    return """Do the things to insert geojson into PostGIS"""


def process_options():
    parser = argparse.ArgumentParser(usage=custom_usage_message())
    parser.add_argument('--source_file', action='store', help='Full path of file to insert into table')
    parser.add_argument('--table', action='store', help='Name of table to create/append')
    parser.add_argument('--tag', default='', action='store', help='Add a tag to the table (optional); ie. --tag test will append $test to table name')
    return parser.parse_args()


def geojson_to_geopandas(source_file):
    # data = json.load(open(prod_source))

    if source_file.endswith(('.geojson')):
        data = json.load(open(source_file))
        # print(data)
        # prod_gdf = gpd.read_file(data)
        gdf = gpd.GeoDataFrame.from_features(data["features"])
        # print(prod_gdf)
        return gdf
    else:
        sys.exit("Incorrect file type: prod_source file must be geojson")


def gpd_to_postgis(gdf, table_name, table_tag, schema_name):
    db_schema = f'{schema_name}'
    if table_tag:
        output_table = f'{table_name}${table_tag}'
    else:
        output_table = f'{table_name}'
    gdf.to_postgis(output_table, engine, db_schema, if_exists='replace')


def main(args):
    source_file = args.source_file
    table_name = args.table
    table_tag = args.tag
    gdf = geojson_to_geopandas(source_file)
    gpd_to_postgis(gdf, table_name, table_tag)


if __name__ == "__main__":
    args = process_options()
    main(args)
