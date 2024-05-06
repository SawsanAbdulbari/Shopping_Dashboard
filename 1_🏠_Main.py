import streamlit as st
import warnings
warnings.filterwarnings('ignore')

st.set_page_config(page_title='Shopping Dashboard ', 
                   page_icon=":bar_chart:",
                   layout="wide")


st.title(":bar_chart: :orange[Consumer Behavior and Shopping Habits] EDA Dashboard")

# Sidebar for additional information
st.sidebar.title(':orange[Shopping] Dashboard')

image ="dataset-cover.jpg"
st.sidebar.image(image, caption='Image', use_column_width=True)

st.sidebar.write("This dashboard is using Consumer Behavior and Shopping Habits Dataset [Kaggle](https://www.kaggle.com/datasets/zeesolver/consumer-behavior-and-shopping-habits-dataset) for educational purposes.\n\nBasic Python Data Analysis [HAMK](https://www.hamk.fi/).")
st.sidebar.write("")
                        
st.subheader("Exploration and Analysis")

st.markdown('''
**Welcome to the Consumer Behavior and Shopping Habits Dashboard (2020-2022)**

*Your gateway to in-depth exploration and analysis of Consumer Behavior and Shopping Habits Dataset.*

**Overview:**
\nThis interactive dashboard empowers you to delve into Consumer Behavior and Shopping Habits Dataset from 2020 to 2022. Our goal is to display the data research and analysis by offering insightful information on the Consumer Behavior and Shopping Habits handled through [Kaggle](https://www.kaggle.com/datasets/zeesolver/consumer-behavior-and-shopping-habits-dataset).
            
**Features:**
1. **Insights:** Explore crucial statistics and metrics related to Consumer Behavior and Shopping Habits Dataset, including Purchase Amount (USD), Category with Item Purchased, Location and Time series ...etc.

2. **Navigation:** The left-hand sidebar menu makes it easy to navigate through various sections, including "Overview" and "Data Exploration & Analysis."

3. **Filtering:** The left-hand sidebar menu has a wide variety of data filtering options for desired specific insights.      

            
**Data Exporting:** 
\nThe unfiltered and filtered data can be downloaded in .csv and .xls formats.

**Data Sources:**
\nWe source data meticulously from Kaggle, ensuring data integrity and reliability.

**Conclusion and Summary:**
\nIn this dashboard, we have presented key insights from the Consumer Behavior and Shopping Habits data analysis. We observed trends in Purchase Amount, explored Previous Purchase Amount, and analyzed the distribution of Purchase Amount by Location, Category and Item Purchased.


**Acknowledgment:**

A lot of gratitude to :orange[Prof. Elina Kulmala] For guidance through out the project. 

''', unsafe_allow_html=True)


# Signature
st.sidebar.write("")
st.sidebar.markdown("Made with :green_heart: by :orange[Sawsan Abdulbari & Linda Marin] ")
