import streamlit as st                      # Python library for dashboard
import plotly.express as px                 # Python library for more affective visualizations
import plotly.graph_objects as go
import pandas as pd                         # Python library for data manipulation
import matplotlib.pyplot as plt
import warnings
warnings.filterwarnings('ignore')


st.title(":bar_chart: :orange[Overview] Of Data")
df = pd.read_csv("Shopping_V1.csv")             # Loading CSV file

# row a
a1, a2,a3, a4= st.columns(4)

# a1
total_purchase_amount = df['IQR_Purchase Amount (USD)'].sum()                   # Calculate the total Purchase Amount (USD)
formatted_total_purchase_amount = f"{total_purchase_amount / 1e5:.2f} K"        # Format the total Purchase Amount

# a2
gender_counts = df['Gender'].value_counts()                                     # Create a DataFrame with the counts of each gender
percentage_count_female = (gender_counts['Female'] / len(df) * 100).round(2)    # Calculate the percentage count for the 'Female' category
formatted_women_percentage = f"{percentage_count_female:.1f}%"                  # Format the total percentage

# a3"
total_clothing = df[df['Category'] == 'Clothing'].shape[0]              # Calculate the total number in the 'Clothing' category
percentage_count_clothes = round((total_clothing / len(df) * 100), 2)   # Calculate the percentage count for the 'Clothing' category
formatted_total_clothes = f"{percentage_count_clothes:.1f}%"            # Format the total percentage

# a4
avrg_previous_purchases= df['IQR_Previous Purchases'].mean().round(2)
formatted_avrg_previous_purchases = f"$ {avrg_previous_purchases:.1f} "

# Display the formatted 
a1.metric("Total Purchase Amount", formatted_total_purchase_amount)
a2.metric("Total Purchase by Women", formatted_women_percentage)
a3.metric("Total Clothing", formatted_total_clothes)
a4.metric("Averge Previous Purchases", formatted_avrg_previous_purchases)


# Sidebar for additional information
st.sidebar.title(':orange[Shopping Dashboard]')

st.sidebar.write("This dashboard is using Consumer Behavior and Shopping Habits Dataset [Kaggle](https://www.kaggle.com/datasets/zeesolver/consumer-behavior-and-shopping-habits-dataset) for educational purposes.\n\nBasic Python Data Analysis [HAMK](https://www.hamk.fi/).")
st.sidebar.write("")

# Filter options
st.sidebar.header("Choose your filter: ")
# Create for Location
Location = st.sidebar.multiselect("Pick Location", df["Location"].unique())
if not Location:
    df2 = df.copy()
else:
    df2 = df[df["Location"].isin(Location)]

# Create for Category
Category = st.sidebar.multiselect("Pick the Category", df2["Category"].unique())
if not Category:
    df3 = df2.copy()
else:
    df3 = df2[df2["Category"].isin(Category)]

# Create for Item Purchased
Item = st.sidebar.multiselect("Pick the Item Purchased",df3["Item Purchased"].unique())

# Filter the data based on Location, Category and Item Purchased
if not Location and not Category and not Item:
    filtered_df = df
elif not Category and not Item:
    filtered_df = df[df["Location"].isin(Location)]
elif not Location and not Item:
    filtered_df = df[df["Category"].isin(Category)]
elif Category and Item:
    filtered_df = df3[df["Category"].isin(Category) & df3["Item Purchased"].isin(Item)]
elif Location and Category:
    filtered_df = df3[df["Location"].isin(Location) & df3["Category"].isin(Category)]
elif Location and Item:
    filtered_df = df3[df["Location"].isin(Location) & df3["Item Purchased"].isin(Item)]
elif Category:
    filtered_df = df3[df3["Category"].isin(Category)]
else:
    filtered_df = df3[df3["Location"].isin(Location) & df3["Category"].isin(Category) & df3["Item Purchased"].isin(Item)]

col1, col2 = st.columns((2))
with col1:
    category_purchase = (filtered_df.groupby(by = ['Category'], as_index= False)['IQR_Purchase Amount (USD)'].sum()).round(2)

# Create a bar plot using Plotly Express
    st.subheader("Category vs. Total Purchase Amount")
    fig = px.bar(category_purchase, 
                 x='Category', 
                 y='IQR_Purchase Amount (USD)',
            #  title='Category in Terms of Total Purchase Amount',
             labels={'Category': 'Category', 'IQR_Purchase Amount (USD)': 'Total Purchase Amount'},
             text=['${:,.2f}'.format(x) for x in category_purchase['IQR_Purchase Amount (USD)']],
             template="seaborn",
             color='Category' )
    st.plotly_chart( fig, use_container_width=True,height=600)


with col2:
    st.subheader("Location vs. Purchase Amount")
    category_counts = filtered_df['Location'].value_counts()
    fig = px.pie(category_counts,
                  names=category_counts.index, 
                  values=category_counts.values)
    fig.update_traces(textinfo='percent+label', 
                      pull=[0.1, 0.1, 0.1])
    st.plotly_chart(fig, use_container_width=True,)


def view_and_download_data(data, download_filename, download_label):
    st.write(data.style.background_gradient(cmap="Blues"))
    csv = data.to_csv(index=False).encode('utf-8')
    st.download_button(download_label, 
                       data=csv, 
                       file_name=download_filename, 
                       mime="text/csv", 
                       help=f'Click here to download the {download_label} as a CSV file')

# Define the layout of columns
cl1, cl2 = st.columns(2)

# Category Data
with cl1:
    with st.expander("Category_ViewData"):
        Category_data = category_purchase
        view_and_download_data(Category_data, "Category.csv", "Download Category Data")

# Location Data
with cl2:
    with st.expander("Location_ViewData"):
        country = filtered_df.groupby(by = "Location", as_index = False)["IQR_Purchase Amount (USD)"].sum().round(2)

        Location_data = country
        view_and_download_data(Location_data, "Location.csv", "Download Location Data")

# Sidebar layout
st.sidebar.header("Date Range Filters:")
start_date = st.sidebar.date_input("Start Date", pd.to_datetime('2020-01-01'))
end_date = st.sidebar.date_input("End Date", pd.to_datetime('2023-12-31'))

# Date range validation
start_date = pd.to_datetime(start_date)     # Convert start_date to datetime
end_date = pd.to_datetime(end_date)         # Convert end_date to datetime
if start_date > end_date:
    st.error("Start date should be before the end date.")
else:
    # Data preprocessing
    df['Date'] = pd.to_datetime(df['Date'])
    filtered_data = df[(df['Date'] >= start_date) & (df['Date'] <= end_date)]

    # Time series data aggregation
    time_series_data = filtered_data.groupby(filtered_data['Date'].dt.strftime("%Y-%b"))['IQR_Purchase Amount (USD)'].sum().reset_index()

    # Create time series chart
    st.subheader("Time Series Analysis of Purchase Amount")
    st.markdown("This dashboard allows you to analyze Sales data over a specified date range.")
    fig2 = px.line(time_series_data, 
                   x='Date', 
                   y="IQR_Purchase Amount (USD)", 
                   markers=True, 
                   labels={"IQR_Purchase Amount (USD)": "Amount"})
    
    fig2.update_xaxes(type='category')  # To ensure proper sorting on the x-axis
    fig2.update_layout(height=500, 
                       width=1000, 
                       template="plotly_white")

    # Add a trendline
    trendline = go.Scatter(x=time_series_data['Date'], 
                           y=time_series_data['IQR_Purchase Amount (USD)'],
                           mode='lines', 
                           line=dict(color='red'), 
                           name='Trendline')
    fig2.add_trace(trendline)

    # Add an annotation
    fig2.add_annotation(x="2021-Feb", 
                        y=7000, 
                        text="Significant Decrease", 
                        showarrow=True, 
                        arrowhead=1,
                        arrowsize=1.5, 
                        arrowwidth=2)

    st.plotly_chart(fig2, use_container_width=True)


chart1, chart2 = st.columns((2))
with chart1:

    # Create a Pie Chart for Promo Code Used
    st.subheader('Promo Code Used')
    fig1 = px.pie(filtered_df, 
                  values='IQR_Purchase Amount (USD)', 
                  names='Promo Code Used')
    st.plotly_chart(fig1, use_container_width=True)
    

with chart2:
# Data Preprocessing for Gender Distribution
    gender_list = df['Gender'].str.split(', ').explode()
    gender_counts = gender_list.value_counts()

# Create a Pie Chart for Borrower Gender Distribution
    st.subheader('Gender Distribution')
    fig2 = px.pie(names=gender_counts.index, 
                  values=(gender_counts / gender_counts.sum()) * 100)
    st.plotly_chart(fig2, use_container_width=True)

with st.expander("View Data"):
    st.write(filtered_df.iloc[:500,1:20:2].style.background_gradient(cmap="Oranges"))

# Download orginal DataSet
    csv = df.to_csv(index = False).encode('utf-8')
    st.download_button('Download Data', 
                   data = csv, 
                   file_name = "Data.csv",
                   mime = "text/csv")

st.subheader("Hierarchical view of Shopping")
filtered_df = df[df['IQR_Purchase Amount (USD)'] > 0]   # Filter out rows with zero IQR_Purchase Amount (USD)

# Create the treemap figure
fig3 = px.treemap(filtered_df, 
                  path=["Location", "Category", "Item Purchased"],
                  values="IQR_Purchase Amount (USD)",
                  hover_data=["IQR_Purchase Amount (USD)"],
                  color="IQR_Purchase Amount (USD)",  # Adjust the color based on IQR_Purchase Amount (USD)
                  color_continuous_scale='rdylbu',)  # Choose a color scale
                  

# Customize the layout
fig3.update_layout(
    width=800,
    height=650,
    margin=dict(l=0, r=0, b=0, t=30),)  # Adjust margin to make space for subheader

# Add more interactivity
fig3.update_traces(
    hoverinfo="label+value+percent parent",
    textinfo="label+value",)

# Set the title and axis labels
fig3.update_layout(
    title="Purchase Amount, Category, and Item Purchased",
    xaxis_title="IQR_Purchase Amount (USD)",
    yaxis_title="Category",)

st.plotly_chart(fig3, use_container_width=True)

# Signature
st.sidebar.write("")
st.sidebar.markdown("Made with :green_heart: by :orange[Sawsan Abdulbari, Linda Marin, Sonja Lahti, Olga Hakasuo and Sofia Rots]")