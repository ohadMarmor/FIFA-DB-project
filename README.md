
# FIFA DB Project


This project aims to simulate a social network app centered around creating and managing soccer squads using data from the FIFA video game. The project involves normalizing a large dataset, setting up a MySQL server, and developing a desktop application using Python's Tkinter library.

Demonstration: demostration:
 https://www.youtube.com/watch?v=-cp6M_iSXKA





## Dataset Selection and Normalization

The dataset for this project was sourced from Kaggle and consisted of records from the FIFA video game spanning eight years (2015-2022) - https://www.kaggle.com/datasets/stefanoleone992/fifa-22-complete-player-dataset. To ensure data integrity and eliminate redundancies, the dataset was preprocessed to handle duplicates before undergoing normalization. Techniques such as deduplication based on unique identifiers or combination of attributes were employed to identify and remove duplicate entries.

After the duplicate handling process, the dataset was normalized to 2NF, 3NF, and BCNF using appropriate techniques such as identifying functional dependencies and removing transitive dependencies. These normalization steps ensured efficient organization of the data, eliminating redundancy and maintaining data integrity.
![image](https://github.com/ohadMarmor/fifa-DB-project/assets/92535416/fd22ab65-e810-4c4c-bde6-b10adb14c980)

## MySQL Server Setup

 A MySQL server was selected as the backend for storing the normalized dataset. The server was set up on a local machine or a remote host, providing a reliable and scalable solution for data storage and retrieval. The choice of MySQL was based on its wide adoption, robust features, and compatibility with the desktop application
## Desktop Application Development

The desktop application was developed using Python's Tkinter library, which offers a simple and intuitive way to create graphical user interfaces (GUIs). The application allows users to search for players based on criteria such as overall rating, age, and nationality. Users can also create their soccer squads, add friends, view and like other users' squads, and track popularity metrics. The GUI was designed to provide a user-friendly experience with intuitive controls and informative displays.


![image](https://github.com/ohadMarmor/fifa-DB-project/assets/92535416/a6b518e6-069a-491d-8235-6d5e2af34941)

![image](https://github.com/ohadMarmor/fifa-DB-project/assets/92535416/38114e13-dd8a-492b-8b33-f8a6ebdd7478)

![image](https://github.com/ohadMarmor/fifa-DB-project/assets/92535416/ced61880-23d9-4053-9e98-3f387a5b4113)

![image](https://github.com/ohadMarmor/fifa-DB-project/assets/92535416/735dafa3-38c4-4701-abb6-d2cfa3937d2b)


The desktop application relies on complex MySQL queries to retrieve relevant player data based on user searches, calculate popularity metrics, and perform database operations efficiently. Examples of complex queries include retrieving players from a specific team, filtering players based on multiple criteria, aggregating popularity statistics, and managing friend relationships.
