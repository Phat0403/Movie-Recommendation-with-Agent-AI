1. Download the data and put it inside ***./data*** folder 
2. Following the instruction inside ***src/data_preprocessing/README.md*** 
3. Run docker service:
```
docker compose up -d
```
4. For next time you run docker compose remember to comment the **mongo-import** service
5. Install dependencies: 
```
pip install -e .
```
6. Insert data into elastic search:
```
python data/insert_elastic_search_data.py
```
7. Run the backend server:
```
python main.py
```