<h3> <a href="https://movierec-sv.herokuapp.com/"> Movie Recommendations Website </a> </h3>

What to expect: This website lets you rate movies and accordingly generates recommendations for you.

How it works:
\n 1. Login/Register your account through "Sign In"
- 2. Find a movie from the "Movies" section or use the "Search" feature
- 3. Add review (rating &/ comment) on a movie page
- 4. Repeat steps 2 and 3, if needed.
- 5. Hit "Movie Suggestions" on the bar and view your recommendations (Refreshing the page provides a new list everytime).

How the Recommendations feature works: It's a Machine Learning algorithm which groups (clusters) you with users who have rated similarly as you.

Other Features:
- CRUD operations (Add/Edit/Delete Review, with user authentication)
- User Management (Login, Registration)
- KMeans Clustering algorithm (Recommendations feature with Collaborative Filtering)
- Search Suggestions and Sort By options (Movies)
- Responsive Layout (Device-compatible)
- Batch process for updating clusters (/reviews/management/commands/runUpdClusters.py)
                   
Technologies:
- Python 2.7 with Django Framework
- Web Templates: HTML, JavaScript, CSS, Bootstrap
- Database: PostgreSQL (Migrated from SQLite)
- Deployment: Heroku
- Data Load: Pandas

Dataset (CSV): <a href="https://grouplens.org/datasets/movielens/"> MovieLens (ml-latest-small) </a>
- 100,000 ratings and 1,300 tag applications applied to 9,000 movies by 700 users. Last updated 10/2016.
- Files (/data): Users, Movies, Reviews, Genres
