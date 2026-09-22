#upload the silver data to adls
data = spark.read.table('finrisk360.default.slv_bank_transactions')
data.write.mode('overwrite').option('mergeSchema', 'true').save('abfss://project-dataset@finrisk3605359934826.dfs.core.windows.net/.bank_transactions_processed')

#uploading the gold data to adls
url = 'abfss://project-dataset@finrisk3605359934826.dfs.core.windows.net/final_datasets'
datasets = ['train','val', 'test']
for dataset in datasets:
    data = spark.read.table(f"finrisk360.gold_datasets.{dataset}")
    data.write.mode('overwrite').option('mergeSchema', 'true').save(f'{url}/{dataset}')
