# Update the file to include "movie category" as the last field
movies_with_category = [
    (1, "The Great Escape", "A group of Allied prisoners of war plan a daring escape from a Nazi prison camp during World War II.", "Steve McQueen, James Garner, Richard Attenborough", "John Sturges", "War"),
    (2, "Inception", "A skilled thief enters the subconscious minds of his targets to steal secrets, but his final job becomes his most dangerous.", "Leonardo DiCaprio, Joseph Gordon-Levitt, Ellen Page", "Christopher Nolan", "Sci-Fi, Thriller"),
    (3, "The Dark Knight", "Batman faces off against the Joker, a criminal mastermind who seeks to create chaos in Gotham City.", "Christian Bale, Heath Ledger, Aaron Eckhart", "Christopher Nolan", "Action, Crime"),
    (4, "Forrest Gump", "The life story of a slow-witted, kind-hearted man from Alabama who witnesses and unwittingly influences several historical events.", "Tom Hanks, Robin Wright, Gary Sinise", "Robert Zemeckis", "Drama, Romance"),
    (5, "The Shawshank Redemption", "Two prisoners form an unlikely friendship while serving time at Shawshank prison.", "Tim Robbins, Morgan Freeman, Bob Gunton", "Frank Darabont", "Drama"),
    (6, "Gladiator", "A betrayed Roman general seeks revenge against the corrupt emperor who murdered his family.", "Russell Crowe, Joaquin Phoenix, Connie Nielsen", "Ridley Scott", "Action, Drama"),
    (7, "Pulp Fiction", "Interwoven stories of crime and redemption in Los Angeles.", "John Travolta, Uma Thurman, Samuel L. Jackson", "Quentin Tarantino", "Crime, Drama"),
    (8, "The Godfather", "The aging patriarch of an organized crime dynasty transfers control of his clandestine empire to his reluctant son.", "Marlon Brando, Al Pacino, James Caan", "Francis Ford Coppola", "Crime, Drama"),
    (9, "Titanic", "A young couple from different social classes fall in love aboard the ill-fated R.M.S. Titanic.", "Leonardo DiCaprio, Kate Winslet, Billy Zane", "James Cameron", "Romance, Drama"),
    (10, "The Matrix", "A hacker learns that reality as he knows it is a simulation controlled by sentient machines.", "Keanu Reeves, Laurence Fishburne, Carrie-Anne Moss", "The Wachowskis", "Sci-Fi, Action"),
    (11, "The Lion King", "The journey of a young lion prince who must reclaim his throne after the murder of his father.", "Matthew Broderick, James Earl Jones, Jeremy Irons", "Roger Allers, Rob Minkoff", "Animation, Drama"),
    (12, "The Silence of the Lambs", "A young FBI agent seeks the help of imprisoned cannibalistic serial killer Hannibal Lecter to catch another killer.", "Jodie Foster, Anthony Hopkins, Lawrence A. Bonney", "Jonathan Demme", "Crime, Drama"),
    (13, "Schindler's List", "A German businessman saves the lives of more than a thousand Jewish refugees during the Holocaust.", "Liam Neeson, Ben Kingsley, Ralph Fiennes", "Steven Spielberg", "Biography, Drama, History"),
    (14, "Avatar", "A paraplegic ex-marine is sent to a distant planet where he becomes involved in a conflict between indigenous people and a corporate mining operation.", "Sam Worthington, Zoe Saldana, Sigourney Weaver", "James Cameron", "Sci-Fi, Adventure"),
    (15, "Fight Club", "An insomniac office worker forms an underground fight club as a form of male bonding, only to see it spiral into chaos.", "Edward Norton, Brad Pitt, Helena Bonham Carter", "David Fincher", "Drama"),
    (16, "Saving Private Ryan", "A group of soldiers are sent to find and bring home a paratrooper whose brothers have been killed in action during World War II.", "Tom Hanks, Matt Damon, Tom Sizemore", "Steven Spielberg", "Drama, War"),
    (17, "The Godfather Part II", "The sequel to The Godfather, following the rise of Michael Corleone as the head of the Corleone family and the flashbacks of his father's rise to power.", "Al Pacino, Robert De Niro, Diane Keaton", "Francis Ford Coppola", "Crime, Drama"),
    (18, "The Prestige", "Two magicians engage in a bitter rivalry, each trying to outdo the other in creating the ultimate illusion.", "Christian Bale, Hugh Jackman, Scarlett Johansson", "Christopher Nolan", "Drama, Mystery"),
    (19, "Interstellar", "A team of explorers travel through a wormhole in search of a new home for humanity as Earth faces environmental collapse.", "Matthew McConaughey, Anne Hathaway, Jessica Chastain", "Christopher Nolan", "Sci-Fi, Drama"),
    (20, "Back to the Future", "A teenager is sent 30 years into the past in a time-traveling DeLorean and must ensure his parents fall in love or risk altering the course of history.", "Michael J. Fox, Christopher Lloyd, Lea Thompson", "Robert Zemeckis", "Sci-Fi, Adventure"),
    (21, "Jurassic Park", "Scientists create a theme park with cloned dinosaurs, but things go awry when the creatures escape.", "Sam Neill, Laura Dern, Jeff Goldblum", "Steven Spielberg", "Adventure, Sci-Fi"),
    (22, "The Wolf of Wall Street", "The rise and fall of a corrupt stockbroker who manipulates the system to make millions.", "Leonardo DiCaprio, Jonah Hill, Margot Robbie", "Martin Scorsese", "Biography, Crime, Drama"),
    (23, "The Departed", "A cop and a gangster infiltrate each other's organizations in this crime thriller set in Boston.", "Leonardo DiCaprio, Matt Damon, Jack Nicholson", "Martin Scorsese", "Crime, Drama, Thriller"),
    (24, "The Grand Budapest Hotel", "A concierge and his protégé become embroiled in a heist involving a priceless painting at a famous European hotel.", "Ralph Fiennes, F. Murray Abraham, Tony Revolori", "Wes Anderson", "Comedy, Drama"),
    (25, "The Revenant", "A frontiersman fights for survival and seeks revenge after being left for dead.", "Leonardo DiCaprio, Tom Hardy, Domhnall Gleeson", "Alejandro González Iñárritu", "Adventure, Drama, Thriller"),
    (26, "The Social Network", "The story of the creation of Facebook and the legal battles that ensued.", "Jesse Eisenberg, Andrew Garfield, Justin Timberlake", "David Fincher", "Biography, Drama"),
    (27, "12 Angry Men", "A jury deliberates the fate of a young man accused of murder, with one juror pushing the others to reconsider the evidence.", "Henry Fonda, Lee J. Cobb, Martin Balsam", "Sidney Lumet", "Drama"),
    (28, "The Big Lebowski", "An eccentric man named Jeffrey 'The Dude' Lebowski is drawn into a kidnapping case due to a mistaken identity.", "Jeff Bridges, John Goodman, Julianne Moore", "Joel and Ethan Coen", "Comedy, Crime"),
    (29, "The Green Mile", "A death row prison guard forms a bond with a condemned man who has a miraculous gift.", "Tom Hanks, Michael Clarke Duncan, David Morse", "Frank Darabont", "Crime, Drama, Fantasy"),
    (30, "Whiplash", "A young jazz drummer's intense ambition and desire to be the best leads to a difficult relationship with his abusive music teacher.", "Miles Teller, J.K. Simmons, Melissa Benoist", "Damien Chazelle", "Drama, Music"),
    (31, "Mad Max: Fury Road", "In a post-apocalyptic wasteland, a lone wanderer and a rebellious woman fight to escape a tyrannical warlord.", "Tom Hardy, Charlize Theron, Nicholas Hoult", "George Miller", "Action, Adventure, Sci-Fi"),
    (32, "La La Land", "A jazz musician and an aspiring actress fall in love but struggle to maintain their relationship as their careers take off.", "Ryan Gosling, Emma Stone, John Legend", "Damien Chazelle", "Comedy, Drama, Music")
]

# Write to the file with the updated format
file_path_final = './data/movies_descriptions.txt'
with open(file_path_final, 'w') as file:
    for movie in movies_with_category:
        line = f"{movie[0]}_{movie[1]}_{movie[2]}_{movie[3]}_{movie[4]}_{movie[5]}\n"
        file.write(line)

file_path_final
