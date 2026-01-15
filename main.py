import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv("netflix_titles.csv")
df = df[df['release_year'] >= 2010].dropna(subset=['date_added'])

# convert to date time
df['date_added'] = df['date_added'].str.strip()
df['date_added'] = pd.to_datetime(df['date_added'])
df['date_added'] = df['date_added'].dt.year

df_sample = df.sample(n=min(5000, len(df)), random_state=42)
# count titles added per year
yearly_count = df.groupby('date_added').size().reset_index(name='count')
# year with highest number
max_year = yearly_count.loc[yearly_count['count'].idxmax()]
# visualize yearly count
plt.bar(yearly_count['date_added'], yearly_count['count'])
plt.xlabel('Year Added')
plt.ylabel('Number of Titles')
plt.title('Netflix Titles Added per Year')
plt.show()

# movie vs show
movies = df[df['type'] == 'Movie'].copy()
tv_show = df[df['type'] == 'TV Show'].copy()

# Movies duration clean-up
movies['duration_num'] = (
    movies['duration']
      .str.extract(r'(\d+)\s*min$')[0]
      .astype(float)
)
movies = movies.dropna(subset=['duration_num'])
movies['duration_num'] = movies['duration_num'].astype(int)

# TV shows seasons clean-up
tv_show['seasons'] = (
    tv_show['duration']
      .str.extract(r'(\d+)\s*Season')[0]
      .astype(float)
)
tv_show = tv_show.dropna(subset=['seasons'])
tv_show['seasons'] = tv_show['seasons'].astype(int)

# Highlight most common values in plots
movie_mode = movies['duration_num'].mode()[0]
tv_mode = tv_show['seasons'].mode()[0]

plt.hist(movies['duration_num'], bins=20, color='skyblue', edgecolor='black')
plt.axvline(movie_mode, color='red', linestyle='--', linewidth=2,
            label=f'Most Common: {movie_mode} min')
plt.title('Movie Duration Distribution')
plt.xlabel('Duration (minutes)')
plt.ylabel('Count')
plt.legend()
plt.show()

plt.hist(tv_show['seasons'], bins=range(1, tv_show['seasons'].max()+2),
         color='lightgreen', edgecolor='black', align='left')
plt.axvline(tv_mode, color='blue', linestyle='--', linewidth=2,
            label=f'Most Common: {tv_mode} seasons')
plt.title('TV Show Seasons Distribution')
plt.xlabel('Number of Seasons')
plt.ylabel('Count')
plt.legend()
plt.show()

# --- New: Extract and count genres ---
# 1. Split the 'listed_in' column into lists
genre_series = df['listed_in'].str.split(', ')

# 2. Explode the lists into a single series
all_genres = genre_series.explode()

# 3. Count occurrences of each genre
genre_counts = all_genres.value_counts()

# 4. Select the top five genres
top_five_genres = genre_counts.head(5)

# Print results
print("Top 5 Genres:\n", top_five_genres)