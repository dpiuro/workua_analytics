import pandas as pd
from collections import Counter
import matplotlib.pyplot as plt


def load_data(file_path):
    data = pd.read_csv("../data.csv")
    return data


def count_technologies(data):
    technology_list = data['technologies'].dropna().str.split(',').sum()
    technology_list = [tech.strip() for tech in technology_list if tech.strip()]

    technology_counts = Counter(technology_list)
    return pd.DataFrame(technology_counts.items(), columns=['Technology', 'Count']).sort_values(by='Count',
                                                                                                ascending=False)


def plot_technologies(tech_counts_df):
    plt.figure(figsize=(10, 6))
    plt.bar(tech_counts_df['Technology'], tech_counts_df['Count'], color='skyblue')
    plt.xlabel('Technology')
    plt.ylabel('Count')
    plt.title('Popularity of Technologies in Job Descriptions')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()


if __name__ == "__main__":
    file_path = '../scraper/data/data.csv'
    data = load_data(file_path)
    tech_counts_df = count_technologies(data)

    plot_technologies(tech_counts_df)
