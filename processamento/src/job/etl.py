from delta.tables import *
from DeltaProcessing import DeltaProcessing
from variables import bronze_dict, silver_dict, gold_list, gold_dict

if __name__ == "__main__":
    delta = DeltaProcessing(landing_zone_bucket = "lrfaws-landing-zone-dev-521738873930", 
                            bronze_bucket = "lrfaws-bronze-layer-dev-521738873930",
                            silver_bucket = "lrfaws-silver-layer-dev-521738873930",
                            gold_bucket= "lrfaws-gold-layer-dev-521738873930")

    for table_name, columns in bronze_dict.items():
        delta.write_to_bronze(
                                prefix = f"mysql/lrfawsmysql/{table_name}",
                                format = "parquet",
                                cols = [*columns])

    for table_name, query in silver_dict.items():
        delta.write_to_silver(
                                prefix = f"mysql/lrfawsmysql/{table_name}",
                                sql = query,      
                                upsert = False)

    for table_name, query in gold_dict.items():
        delta.write_to_gold(
                                prefix_list = gold_list,
                                prefix = f"delivery/{table_name}",
                                sql = query,
                                upsert = False)
