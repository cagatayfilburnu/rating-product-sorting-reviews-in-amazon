# Rating Product & Sorting Reviews in Amazon  
![6505894](https://user-images.githubusercontent.com/95078183/224841001-b28ebb49-ba17-40a3-a39d-9d6d4fc4eeba.jpg)

---
### **Business Problem**

One of the most important problems in **e-commerce** is the correct calculation of the points given to the products after sales. The solution to this problem means providing greater customer satisfaction for the e-commerce site, prominence of the product for the sellers and a seamless shopping experience for the buyers.

On the other hand, another problem is the correct ordering of the comments given to the products. Since misleading comments will directly affect the sale of the product, it will cause both financial loss and loss of customers.

*For example:*

When one user gives 5 points and the other user 5 points, are their contributions to **The Wisdom of Crowds** actually equal?

---
### **Story of Dataset**
amazon_review.csv is a dataset that contains Amazon product data, includes product categories and various metadata. The product with the most reviews in the electronics category has user ratings and reviews.

    
<p align="center">
  <img src= "https://user-images.githubusercontent.com/95078183/224845474-5e0f32ce-dbe0-4298-8152-ba74f6ea7c44.png" />
</p>

---

### **Variables in Dataset**

- **reviewerID**: User ID
- **asin**: Product ID
- **reviewerName**: User Name 
- **helpful**: Helpful Review Ranking
- **reviewText**: Review
- **overall**: Product's Rating
- **summary**: Summary of Review
- **unixReviewTime**: Time of Review
- **reviewTime**: Time of Review (Raw)
- **day_diff**: Number of Days Since Review
- **helpful_yes**: The Number of the Review was Found Beneficial
- **total_vote**: Total Review Vote
---
### **Goal of the Project**
This study aims to calculate Average Rating with current reviews and specify 20 reviews for the product to be displayed on the product detail page.

1-) According to calculations;

```ruby
df["overall"].mean()  # 4.587589013224822

time_based_weighted_average(df)  # 4.593847825464406
```
There is a minimal difference between **normal mean** and **time-based weighted mean**.

2-) **time_based_weighted_average()** function is;
```ruby
def time_based_weighted_average(dataframe, w1=28, w2=26, w3=24, w4=22):
    return dataframe.loc[dataframe["day_diff"] <= dataframe["day_diff"].quantile(0.25), "overall"].mean() * w1/100 + \
           dataframe.loc[(dataframe["day_diff"] > dataframe["day_diff"].quantile(0.25)) & (dataframe["day_diff"] <= dataframe["day_diff"].quantile(0.55)), "overall"].mean() * w2/100 + \
           dataframe.loc[(dataframe["day_diff"] > dataframe["day_diff"].quantile(0.50)) & (dataframe["day_diff"] <= dataframe["day_diff"].quantile(0.75)), "overall"].mean() * w3/100 + \
           dataframe.loc[dataframe["day_diff"] > dataframe["day_diff"].quantile(0.75), "overall"].mean() * w4/100
```
In this part, the score of current users was held more important. Scores can be adjustable according to analysis comments.

3-) Last part, there is a comparison some methods about to examine reviews. Wilson Lower Bound (WLB) is more useful to specify 20 reviews for the product.
```ruby
df["score_pos_neg_diff"] = df.apply(lambda x: score_up_down_diff(x["helpful_yes"],
                                                                 x["helpful_no"]), axis=1)

df["score_average_rating"] = df.apply(lambda x: score_average_rating(x["helpful_yes"],
                                                                     x["helpful_no"]), axis=1)

df["wilson_lower_bound"] = df.apply(lambda x: wilson_lower_bound(x["helpful_yes"],
                                                                 x["helpful_no"]), axis=1)
```
---
**Conclusion:** As a result of the study, the table sorted according to the wilson lower bound variable can be seen below.

<p align="middle">
  <img src="https://user-images.githubusercontent.com/95078183/225131083-519a87be-93d1-4f4b-9913-b40d1072c48b.png" />
</p>


