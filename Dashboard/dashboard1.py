import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
import calendar
import matplotlib.dates as mdates
from babel.numbers import format_currency
sns.set(style='dark')

#Pivot table untuk melihat rata rata polutan udara di steiap station tagun 2013 - 2017
def create_air_quality_pivot_df(df):
    station_year_df = df.groupby(by=["station", "year"]).agg({
        "PM2.5": "mean",
        "PM10": "mean",
        "SO2": "mean",
        "NO2": "mean",
        "CO": "mean",
        "O3": "mean"
    }).round()
    
    return station_year_df

#Pivot table untuk melihat rata rata polutan udara tahun 2013 - 2017
def create_air_quality_yearly_df(df):
    year_df = df.groupby(by=["year"]).agg({
        "PM2.5": "mean",
        "PM10": "mean",
        "SO2": "mean",
        "NO2": "mean",
        "CO": "mean",
        "O3": "mean"
    }).round()
    
    return year_df


#Pivot table untuk melihat rata rata polutan udara BULANAN
# def get_month_name(month):
#     return calendar.month_name[month]

def create_air_quality_monthly_pivot_df(df):
    # Create monthly pivot table
    month_df = df.groupby(by=["month"]).agg({
        "PM2.5": "mean",
        "PM10": "mean",
        "SO2": "mean",
        "NO2": "mean",
        "CO": "mean",
        "O3": "mean"
    }).round()

    # Convert the index from numeric month to month names
    # month_df.index = month_df.index.map(get_month_name)
    
    return month_df


#Pivot table untuk melihat rata rata polutan udara berdasarkan station 
def create_air_quality_station_pivot_df(df):
    # Create station-wise pivot table
    station_df = df.groupby(by=["station"]).agg({
        "PM2.5": "mean",
        "PM10": "mean",
        "SO2": "mean",
        "NO2": "mean",
        "CO": "mean",
        "O3": "mean"
    }).round()

    return station_df

# Melakukan PIVOT pengelompokan dan menghitung rata-rata polutan HARIAN
def create_air_quality_daily_pivot_df(df):
    # Ekstrak hari dalam seminggu dari kolom tanggal
    df['day_of_week'] = df['day'].dt.dayofweek

    # Mendefinisikan fungsi untuk mengonversi hari numerik menjadi nama hari
    def get_day_name(day):
        return calendar.day_name[day]

    # Mengelompokkan berdasarkan hari dalam seminggu dan menghitung rata-rata harian polutan
    day_df = df.groupby(by=["day_of_week"]).agg({
        "PM2.5": "mean",
        "PM10": "mean",
        "SO2": "mean",
        "NO2": "mean",
        "CO": "mean",
        "O3": "mean"
    }).round()

    # Mengonversi indeks dari hari numerik menjadi nama hari
    day_df.index = day_df.index.map(get_day_name)

    return day_df



#Pivot table untuk melihat rata rata polutan udara di steiap station tagun 2013 - 2017 berdasarkan jam
def create_air_quality_hourly_pivot_df(df):
    # Group by hour and calculate hourly average pollutants
    hour_df = df.groupby(by=["hour"]).agg({
        "PM2.5": "mean",
        "PM10": "mean",
        "SO2": "mean",
        "NO2": "mean",
        "CO": "mean",
        "O3": "mean"
    }).round()

    return hour_df


#import data air quality
air_df = pd.read_csv("air_quality.csv")

# Fungsi untuk mengonversi kolom tanggal dari string ke format datetime
def convert_to_datetime(df, date_cols=["year", "month", "day", "hour"]):
    for col in date_cols:
        df[col] = pd.to_datetime(df[col], errors='coerce')
    df["datetime"] = pd.to_datetime(df[date_cols])
    return df

# Data awal
# Misalnya, air_df adalah DataFrame awal sebelumnya
# (pastikan sudah di-import dan di-preprocess jika diperlukan)
air_df = convert_to_datetime(air_df)

# Sidebar untuk filter data
with st.sidebar:
    # Menambahkan logo perusahaan
    st.image("https://github.com/dicodingacademy/assets/raw/main/logo.png")
    
    # Mengambil start_date & end_date dari date_input
    start_date, end_date = st.date_input(
        label='Rentang Waktu',
        min_value=air_df["datetime"].min().date(),
        max_value=air_df["datetime"].max().date(),
        value=[air_df["datetime"].min().date(), air_df["datetime"].max().date()]
    )

# Menerapkan filter ke DataFrame
filtered_df = air_df[
    (air_df["datetime"].dt.date >= start_date) &
    (air_df["datetime"].dt.date <= end_date)
]

# Menampilkan DataFrame yang telah difilter
st.title("Data visualization dashboard for 8 stadiums in China ")


# Menyiapkan berbagai dataframe
station_year_df = create_air_quality_pivot_df(filtered_df)
year_df = create_air_quality_yearly_df(filtered_df)
month_df = create_air_quality_monthly_pivot_df(filtered_df)
station_df = create_air_quality_station_pivot_df(filtered_df)
day_df = create_air_quality_daily_pivot_df(filtered_df)
hour_df = create_air_quality_hourly_pivot_df(filtered_df)





# Inisialisasi aplikasi Streamlit
st.header('Air Quality Station-wise Analysis')
station_df_sorted = station_df.sort_values(by='PM2.5', ascending=False)

# Visualisasi plot dengan menggunakan matplotlib dan seaborn
plt.figure(figsize=(10, 6))
sns.barplot(data=station_df_sorted, x='PM2.5', y=station_df_sorted.index, color='blue')  # Sesuaikan dengan variabel dan warna yang diinginkan
plt.xlabel('Average PM2.5 Level')
plt.ylabel('Station')
plt.title('Average PM2.5 Levels by Station')
st.pyplot(plt)


# st.header("Average PM2.5 Levels:")
# col1, col2 = st.columns(2)
# for index, row in station_df_sorted.iterrows():
#     with col1:
#         st.metric(label=index, value=row['PM2.5'])




# Konversi kolom 'year', 'month', 'day' menjadi tipe data datetime
filtered_df['date'] = pd.to_datetime(filtered_df[['year', 'month', 'day']])

# Agregasi data harian
daily_data = filtered_df.groupby('date').agg({'PM2.5': 'mean', 'PM10': 'mean', 'SO2': 'mean', 'NO2': 'mean', 'CO': 'mean', 'O3': 'mean'})
st.header('Daily Air Quality Variation')

# Visualisasi data harian dengan menggunakan line chart
fig, ax = plt.subplots(figsize=(12, 6))

# Plot data
for column in daily_data.columns:
    ax.plot(daily_data.index, daily_data[column], label=column)

# Format sumbu y
ax.yaxis.set_major_locator(plt.MaxNLocator(integer=True))  # Menampilkan angka integer pada sumbu y
ax.xaxis.set_major_formatter(plt.matplotlib.dates.DateFormatter('%Y-%m'))  # Format tahun-bulan

plt.title('Daily Variations in Air Quality')
plt.xlabel('Date/Day')
plt.ylabel('Average Value')
plt.legend()
plt.xticks(rotation=45)  # Rotasi label tanggal untuk kejelasan
st.pyplot(fig)





# Pastikan 'month' tidak ada dalam indeks DataFrame
filtered_df.reset_index(drop=True, inplace=True)

# Konversi kolom 'year', 'month', 'day' menjadi tipe data datetime
filtered_df['date'] = pd.to_datetime(filtered_df[['year', 'month', 'day']])

# Agregasi data bulanan
annual_data = filtered_df.groupby(filtered_df['date'].dt.month).agg({
    'PM2.5': 'mean',
    'PM10': 'mean',
    'SO2': 'mean',
    'NO2': 'mean',
    'CO': 'mean',
    'O3': 'mean'
})

# Inisialisasi aplikasi Streamlit
st.header('Monthly Air Quality Variation')

# Visualisasi data bulanan dengan menggunakan line chart
fig, ax = plt.subplots(figsize=(12, 6))

# Plot data
for column in annual_data.columns:
    ax.plot(calendar.month_name[1:], annual_data[column], label=column, linewidth=3)

plt.title('Monthly Variations in Air Quality')
plt.xlabel('Month')
plt.ylabel('Average Value')
plt.legend()
st.pyplot(fig)


# Misalnya, kita menggunakan filter untuk tahun 2013-2017
filtered_df = filtered_df[(filtered_df['datetime'] >= '2013-01-01') & (filtered_df['datetime'] <= '2017-12-31')]

# Ubah kolom datetime menjadi tipe data datetime
filtered_df['datetime'] = pd.to_datetime(filtered_df['datetime'])

# Ekstrak tahun dari kolom datetime
filtered_df['year'] = filtered_df['datetime'].dt.year

# Agregasi data tahunan
annual_data = filtered_df.groupby('year').agg({'PM2.5': 'mean', 'PM10': 'mean', 'SO2': 'mean', 'NO2': 'mean', 'CO': 'mean', 'O3': 'mean'})

# Streamlit app
st.header('Yearly Air Quality Variation')

fig, ax = plt.subplots(figsize=(12, 6))
# Menampilkan plot dengan tahun pada sumbu x

plt.figure(figsize=(12, 6))
for column in annual_data.columns:
    plt.plot(annual_data.index, annual_data[column], label=column, linewidth=3)

plt.xlabel('Year')
plt.ylabel('Average Value')
plt.xticks(annual_data.index)  # Menambahkan ini untuk menampilkan semua tahun pada sumbu x
plt.legend()

# Simpan gambar Matplotlib ke dalam variabel
fig = plt.gcf()

# Tampilkan gambar menggunakan st.pyplot() dengan menyertakan variabel fig
st.pyplot(fig)


#RATA-RATA POLUTAN PM2.5 
filtered_df['year'] = filtered_df['datetime'].dt.year
df = filtered_df[['PM2.5', 'year']].groupby(["year"]).mean().reset_index().sort_values(by='year', ascending=False)

# Streamlit app
st.header('Average PM2.5 per Year')

# Create a plot using Seaborn
fig, ax = plt.subplots(figsize=(10, 5))
sns.pointplot(x='year', y='PM2.5', data=df, ax=ax)

# Customize the plot
plt.title('Average PM2.5 per Year')
plt.xlabel('Year')
plt.ylabel('PM2.5')

# Display the plot using Streamlit
st.pyplot(fig)


#RATA-RATA POLUTAN PM10 
filtered_df['year'] = filtered_df['datetime'].dt.year
df = filtered_df[['PM10', 'year']].groupby(["year"]).mean().reset_index().sort_values(by='year', ascending=False)

# Streamlit app
st.header('Average PM10 per Year')

# Create a plot using Seaborn
fig, ax = plt.subplots(figsize=(10, 5))
sns.pointplot(x='year', y='PM10', data=df, ax=ax)

# Customize the plot
plt.title('Average PM10 per Year')
plt.xlabel('Year')
plt.ylabel('PM10')
# Display the plot using Streamlit
st.pyplot(fig)



#RATA-RATA POLUTAN SO2 
filtered_df['year'] = filtered_df['datetime'].dt.year
df = filtered_df[['SO2', 'year']].groupby(["year"]).mean().reset_index().sort_values(by='year', ascending=False)

# Streamlit app
st.header('Average SO2 per Year')

# Create a plot using Seaborn
fig, ax = plt.subplots(figsize=(10, 5))
sns.pointplot(x='year', y='SO2', data=df, ax=ax)

# Customize the plot
plt.title('Average SO2 per Year')
plt.xlabel('Year')
plt.ylabel('SO2')

# Display the plot using Streamlit
st.pyplot(fig)


#RATA-RATA POLUTAN NO2 
filtered_df['year'] = filtered_df['datetime'].dt.year
df = filtered_df[['NO2', 'year']].groupby(["year"]).mean().reset_index().sort_values(by='year', ascending=False)

# Streamlit app
st.header('Average NO2 per Year')

# Create a plot using Seaborn
fig, ax = plt.subplots(figsize=(10, 5))
sns.pointplot(x='year', y='NO2', data=df, ax=ax)

# Customize the plot
plt.title('Average NO2 per Year')
plt.xlabel('Year')
plt.ylabel('NO2')

# Display the plot using Streamlit
st.pyplot(fig)



#RATA-RATA POLUTAN CO 
filtered_df['year'] = filtered_df['datetime'].dt.year
df = filtered_df[['CO', 'year']].groupby(["year"]).mean().reset_index().sort_values(by='year', ascending=False)

# Streamlit app
st.header('Average CO per Year')

# Create a plot using Seaborn
fig, ax = plt.subplots(figsize=(10, 5))
sns.pointplot(x='year', y='CO', data=df, ax=ax)

# Customize the plot
plt.title('Average CO per Year')
plt.xlabel('Year')
plt.ylabel('CO')

# Display the plot using Streamlit
st.pyplot(fig)



#RATA-RATA POLUTAN O3 
filtered_df['year'] = filtered_df['datetime'].dt.year
df = filtered_df[['O3', 'year']].groupby(["year"]).mean().reset_index().sort_values(by='year', ascending=False)

# Streamlit app
st.header('Average O3 per Year')

# Create a plot using Seaborn
fig, ax = plt.subplots(figsize=(10, 5))
sns.pointplot(x='year', y='O3', data=df, ax=ax)

# Customize the plot
plt.title('Average O3 per Year')
plt.xlabel('Year')
plt.ylabel('O3')

# Display the plot using Streamlit
st.pyplot(fig)
