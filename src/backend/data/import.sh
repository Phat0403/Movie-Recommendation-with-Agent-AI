#!/bin/bash

echo "Importing data into MongoDB..."

mongoimport --host mongo \
  --username root \
  --password example \
  --authenticationDatabase admin \
  --db movie_db \
  --collection movies \
  --type csv \
  --headerline \
  --file /scripts/movies_2020_new.csv

echo "Movies data imported successfully!"

mongoimport --host mongo \
--username root \
--password example \
--authenticationDatabase admin \
--db movie_db \
--collection name_basics \
--type csv \
--headerline \
--file /scripts/new_name_basics.csv

echo "Name basics data imported successfully!"

mongoimport --host mongo \
--username root \
--password example \
--authenticationDatabase admin \
--db movie_db \
--collection ratings \
--type csv \
--headerline \
--file /scripts/new_title_ratings.csv

echo "Ratings data imported successfully!"

mongoimport --host mongo \
--username root \
--password example \
--authenticationDatabase admin \
--db movie_db \
--collection crew \
--type csv \
--headerline \
--file /scripts/new_title_crew.csv

echo "Title crew data imported successfully!"

mongoimport --host mongo \
--username root \
--password example \
--authenticationDatabase admin \
--db movie_db \
--collection principals \
--type csv \
--headerline \
--file /scripts/new_title_principals.csv

echo "Title principals data imported successfully!"

echo "Data imported successfully!"