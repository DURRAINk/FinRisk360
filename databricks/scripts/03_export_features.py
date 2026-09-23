#uploading the gold data to adls
gld_url = 'abfss://azureml-blobstore-158438c9-9d7b-46f9-8cdd-abe002d5b885@finrisk3605359934826.dfs.core.windows.net/final-datasets'
datasets = ['train','val', 'test']
for dataset in datasets:
    data = spark.read.table(f"finrisk360.gold_datasets.{dataset}")
    data.write.format('csv').mode('overwrite').option('mergeSchema', 'true').save(f'{gld_url}/{dataset}')
