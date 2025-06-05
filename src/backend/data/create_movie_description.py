import pandas as pd

def create_description_from_row(row):
    """
    Create a description for a movie based on its attributes.
    
    Args:
        row (pd.Series): A row from the DataFrame containing movie attributes.
    
    Returns:
        str: A description of the movie.
    """
    return f"{row["tconst"]}_{row["primaryTitle"]}_{row["genres"]}_{row["description"]}"

def create_movie_description(path, output_path):
    
    df = pd.read_csv(path)
    x = df.apply(create_description_from_row, axis=1)
    with open(output_path, 'w') as f:
        for i in range(len(x)):
            x[i] = x[i].replace("'", "")
            x[i] = x[i].replace('\n', "")
            x[i] = x[i].replace('\r', "")
            x[i] = x[i].replace('"', "")
            f.write(x[i] + "\n")
    print(f"Movie description created and saved to {output_path}")

if __name__ == "__main__":
    path = "data/movies_2020_new.csv"
    output_path = "data/movie_description.txt"
    create_movie_description(path, output_path)