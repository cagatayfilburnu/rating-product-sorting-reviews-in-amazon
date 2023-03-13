#######################################################
# Rating Product & Sorting Reviews in Amazon Dataset
#######################################################
# 1- General Table of Amazon Dataset
# 2- Calculate Average Rating with Current Comments
# 3- Specifying 20 reviews for the product to be displayed on the product detail page
# #- Conclusion

# Packages and settings
import pandas as pd
import math
import scipy.stats as st

pd.set_option("display.max_columns", None)
pd.set_option("display.max_rows", None)
pd.set_option("display.width", 500)
pd.set_option("display.expand_frame_repr", False)
pd.set_option("display.float_format", lambda x: '%.3f' % x)

df = pd.read_csv("projects/amazon_review.csv")
df.head()
df.info()

#######################################################
# 1- General Table of Amazon Dataset
#######################################################
def check_df(dataframe, head=5):
    print("################ Shape ##################")
    print(dataframe.shape)
    print("################ Types ##################")
    print(dataframe.dtypes)
    print("################ Head ##################")
    print(dataframe.head(head))
    print("################ Tail ##################")
    print(dataframe.tail(head))
    print("################ NA ##################")
    if df.isnull().values.any():
        print(dataframe.isnull().sum())
    else:
        print("There is no NA")
    print("################ Quantiles ##################")
    print(dataframe.describe([0, 0.05, 0.50, 0.95, 0.99, 1]).T)
    print("################ Value Counts for Each Column ##################")
    for col in dataframe.columns:
        if dataframe[col].nunique() > 10:
            print("Too many elements for *{}*".format(col))
            continue
        else:
            print(f"{col}: {dataframe[col].value_counts()}")


check_df(df)

#######################################################
# 2- Calculate Average Rating with Current Comments
#######################################################
df.head()

# Average of "overall" variable.
df["overall"].mean()  # 4.587589013224822

# Time-Based Weighted Average
df.info()
print(df["day_diff"].describe().T)  # min: 1.000 - 25%: 281.000 - 50%: 431.000 - 75%: 601.000 - max: 1064.000

df.loc[df["day_diff"] < 281].count()
df.loc[df["day_diff"] > 900].count()
df.loc[(df["day_diff"] > 280) & (df["day_diff"] < 600)].count()

df["reviewTime"] = pd.to_datetime(df["reviewTime"])

def time_based_weighted_average(dataframe, w1=28, w2=26, w3=24, w4=22):
    return dataframe.loc[df["day_diff"] <= 100, "overall"].mean() * w1/100 + \
           dataframe.loc[df["day_diff"] > 280 & (df["day_diff"] <= 430), "overall"].mean() * w2/100 + \
           dataframe.loc[df["day_diff"] > 430 & (df["day_diff"] <= 600), "overall"].mean() * w3/100 + \
           dataframe.loc[df["day_diff"] > 600, "overall"].mean() * w4/100


time_based_weighted_average(df)  # 4.601822416778495

# Average Rating in the last 100 days:
df.loc[df["day_diff"] <= 100, "overall"].mean()

# Average Rating in between last 200 and 430 days:
df.loc[(df["day_diff"] > 280) & (df["day_diff"] <= 430), "overall"].mean()

# Average Rating in between last 430 and 600 days:
df.loc[(df["day_diff"] > 430) & (df["day_diff"] <= 600), "overall"].mean()

# Average Rating 600 days older:
df.loc[(df["day_diff"] > 600), "overall"].mean()

#######################################################
# 3- Specifying 20 reviews for the product to be displayed on the product detail page
#######################################################
df.head()
# Create "helpful_no" variable in dataset.
df["helpful_no"] = df["total_vote"] - df["helpful_yes"]


# Define necessary functions for sorting reviews

def score_up_down_diff(up, down):
    return up - down

def score_average_rating(up, down):
    if up + down == 0:
        return 0
    return up / (up + down)

# Wilson Lower Bound (WLB) is more reliable function for us.
def wilson_lower_bound(up, down, confidence=0.95):
    """
    Calculate the 'Wilson Lower Bound Score'

    - The lower limit of the CI to be calculated for the Bernoulli parameter (p) is accepted as the WLB score.
    - Score that will be calculated uses for the sorting product.

    Parameters
    ----------
    up: int
        up count
    down: int
        down count
    confidence: float
        confidence

    Returns
    -------
    wilson score: float

    """
    n = up + down
    if n == 0:
        return 0
    z = st.norm.ppf(1 - (1 - confidence) / 2)
    phat = 1.0 * up / n
    return (phat + z * z / (2 * n) - z * math.sqrt((phat * (1 - phat) + z * z / (4 * n)) / n)) / (1 + z * z / n)


df["score_pos_neg_diff"] = df.apply(lambda x: score_up_down_diff(x["helpful_yes"],
                                                                 x["helpful_no"]), axis=1)

df["score_average_rating"] = df.apply(lambda x: score_average_rating(x["helpful_yes"],
                                                                     x["helpful_no"]), axis=1)

df["wilson_lower_bound"] = df.apply(lambda x: wilson_lower_bound(x["helpful_yes"],
                                                                 x["helpful_no"]), axis=1)


#######################################################
#                   Conclusion
#######################################################
df.head()
df.sort_values("wilson_lower_bound", ascending=False).head(20)
