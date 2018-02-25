import pandas as pd
import matplotlib.pyplot as plt


def plot(db, c):
    db[c].plot.hist(20)


if __name__ == "__main__":
    df = pd.read_csv('redacao_pas.csv', sep=';')
    df = df.drop('Unnamed: 0', axis=1)
    df['tot'] = df['n1'] + df['n_text']
    plot(df, 'tot')
    plot(df, 'n_text')
    plot(df, 'n1')
    plt.show()
    df['rank'] = df['tot'].rank(method='max', ascending=False)
    df['percentile'] = pd.qcut(df.tot, 100, labels=False, retbins=False, precision=3, duplicates='drop')


