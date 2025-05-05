Put data in backend/data \
Run spark to preprocess data:
```
bash script.sh process_name_basics.py
bash script.sh process_principal.py
bash script.sh process_title_crew.py
bash script.sh process_title_episodes.py
bash script.sh process_title_ratings.py
```
Then convert spark csv folder into csv file:
```
python convert_spark_folder_to_csv_file.py
```
Then run prepare data for Elastic Search by running **prepare_data_for_es.ipynb**