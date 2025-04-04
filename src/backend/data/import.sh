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
  --file /scripts/movies.csv

echo "Movies data imported successfully!"

mongoimport --host mongo \
--username root \
--password example \
--authenticationDatabase admin \
--db movie_db \
--collection name_basics \
--type csv \
--headerline \
--file /scripts/name_basics.csv

echo "Name basics data imported successfully!"

mongoimport --host mongo \
--username root \
--password example \
--authenticationDatabase admin \
--db movie_db \
--collection ratings \
--type csv \
--headerline \
--file /scripts/ratings.csv

echo "Ratings data imported successfully!"

echo "Data imported successfully!"