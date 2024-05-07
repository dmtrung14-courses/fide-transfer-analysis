import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import matplotlib.cm as cm
from scipy.stats import gaussian_kde, norm

data = pd.read_csv('data_rated.csv')
data = data.iloc[:, 1:]
data = data.dropna()
data = data.reset_index(drop=True)

def number_of_transfers(data):
    plt.figure(figsize=(10, 6))

    # Number of transfers TO each federation in the top 10
    federation_counts = data['Federation'].value_counts().head(20)
    federation_counts.plot(kind='bar')
    plt.xlabel('Federation')
    plt.ylabel('Number of Entries')
    plt.title('Number of Entries for Each Federation')
    plt.savefig('./output/federation_counts.png')
def number_of_transfers(data):    
    # Number of transfers in the USA Federation
    usa_transfers = data[data['Federation'] == 'USA'].shape[0]
    print("Number of transfers to the USA Federation:", usa_transfers)
    # Number of transfers overall
    total_transfers = data.shape[0]
    print("Number of transfers overall:", total_transfers)

def top_20_average_ratings(data):
    plt.figure(figsize=(10, 6))

    # Average rating of players in each federation
    top_10_average_rating = data.groupby('Federation')['Rating'].apply(lambda x: x.nlargest(5).mean()).nlargest(30)
    top_10_average_rating.plot(kind='bar')
    plt.xlabel('Federation')
    plt.ylabel('Average Rating')
    plt.title('Average Rating of Top 5 Players in Each Federation (Top 30 Federations)')
    plt.ylim(2300, plt.ylim()[1])
    plt.savefig('./output/top_30_average_rating.png')

def top_20_players(data):
    # Rating of the top 20 players, grouped by Federation
    top_20_players = data.nlargest(20, 'Rating')
    unique_federations = top_20_players['Federation'].unique()
    num_federations = len(unique_federations)
    colors = cm.rainbow(np.linspace(0, 1, num_federations))
    federation_colors = dict(zip(unique_federations, colors))

    colors = [federation_colors[x] for x in top_20_players['Federation']]

    fig, ax = plt.subplots(figsize=(8,5))  # Adjust the figure size as needed
    top_20_players.plot(x='Name', y='Rating', kind='bar', ax=ax, color=colors)
    ax.set_xlabel('Player')
    ax.set_ylabel('Rating')
    ax.set_title('Rating of Top 20 Players (Grouped by Federation)')
    ax.set_ylim(2500, ax.get_ylim()[1])

    # Rotate x-axis labels for better visibility
    plt.xticks(rotation=90, ha='center')  # Rotate labels by 90 degrees

    # Create legend
    legend_elements = [plt.Line2D([0], [0], marker='o', color=federation_colors[fed], label=fed, linestyle='', markersize=10) for fed in unique_federations]
    ax.legend(handles=legend_elements, bbox_to_anchor=(1.02, 1), loc='upper left')

    plt.tight_layout()  # Adjust layout to prevent labels from being cut off
    plt.savefig('./output/top_20_players.png', bbox_inches='tight')

def usa_vs_rest_of_world(data):
    # Average rating of players from USA Federation vs other Federations
    usa_average_rating = data[data['Federation'] == 'USA']['Rating'].mean()
    all_federations_average_rating = data['Rating'].mean()
    print("Average Rating - USA Federation:", usa_average_rating)
    print("Average Rating - All Federations:", all_federations_average_rating)
    plt.figure(figsize=(10, 6))
    plt.bar(['USA', 'All Federations'], [usa_average_rating, all_federations_average_rating])
    plt.xlabel('Federation')
    plt.ylabel('Average Rating')
    plt.title('Average Rating of Players from USA Federation vs Other Federations')
    plt.ylim(2100, plt.ylim()[1])
    plt.savefig('./output/usa_vs_other_federations.png')

def standard_deviation(data):
    # Standard deviation of ratings of players from USA Federation vs other Federations
    usa_ratings = data[data['Federation'] == 'USA']['Rating']
    other_ratings = data['Rating']
    usa_std = usa_ratings.std()
    other_std = other_ratings.std()
    print("std of Ratings - USA Federation:", usa_std)
    print("std of Ratings - All Federations:", other_std)


def kde_rating(data):
    plt.figure(figsize=(10, 6))
    sns.kdeplot(data['Rating'], fill=True)
    normal_mean = data['Rating'].mean()
    normal_std = data['Rating'].std()
    x_range = np.linspace(data["Rating"].min(), data["Rating"].max(), 1000)
    normal_dist = norm.pdf(x_range, loc=normal_mean, scale=normal_std)
    plt.plot(x_range, normal_dist, 'r-', label='Normal Distribution')

    # Plot vertical lines for mean and mean +/- std
    plt.axvline(normal_mean, color='g', linestyle='--', label='Data Mean')
    # plt.axvline(normal_mean + normal_std, color='b', linestyle='--', label='Data Mean + Std')
    # plt.axvline(normal_mean - normal_std, color='b', linestyle='--', label='Data Mean - Std')
    plt.xlabel('Rating')
    plt.ylabel('Density')
    plt.title('Kernel Density Estimation of Player Ratings')
    plt.savefig('./output/kde_rating.png')

if __name__=="__main__":
    number_of_transfers(data)
    top_20_average_ratings(data)
    top_20_players(data)
    usa_vs_rest_of_world(data)
    standard_deviation(data)
    kde_rating(data)