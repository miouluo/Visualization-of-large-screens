import pandas as pd

file_path = 'data/Dcar.csv'
data = pd.read_csv(file_path)
data.head()

# top_brands = data.nlargest(10, 'count')[['brand_name', 'count']]
# top_series = data.nlargest(10, 'count')[['series_name', 'count']]
# top_manufacturers = data.nlargest(10, 'count')[['brand_name', 'count']]

# brands_file_path = './data/top_brands.csv'
# series_file_path = './data/top_series.csv'
# manufacturers_file_path = './data/top_manufacturers.csv'

# top_brands.to_csv(brands_file_path, index=False)
# top_series.to_csv(series_file_path, index=False)
# top_manufacturers.to_csv(manufacturers_file_path, index=False)


def save_data_to_csv(data, file_name):
    file_path = f'../data/{file_name}.csv'
    data.to_csv(file_path, index=False)
    return file_path


brand_sales = data.groupby('brand_name').sum().reset_index()[['brand_name', 'count']]
data_1_path = save_data_to_csv(brand_sales, 'data_1')

china_sales = data[data['brand_name'] == '中国'].groupby('month').sum().reset_index()[['month', 'count']]
data_2_path = save_data_to_csv(china_sales, 'data_2')

top_brand_sales = data.groupby('brand_name').sum().reset_index().nlargest(10, 'count')[['brand_name', 'count']]
data_3_path = save_data_to_csv(top_brand_sales, 'data_3')

top_series_sales = data.groupby('series_name').sum().reset_index().nlargest(10, 'count')[['series_name', 'count']]
data_4_path = save_data_to_csv(top_series_sales, 'data_4')

top_manufacturer_sales = data.groupby('brand_name').sum().reset_index().nlargest(10, 'count')[['brand_name', 'count']]
data_5_path = save_data_to_csv(top_manufacturer_sales, 'data_5')

word_cloud_data = data.groupby('series_name').sum().reset_index()[['series_name', 'count']]
data_6_path = save_data_to_csv(word_cloud_data, 'data_6')

model_type_sales = data.groupby('type').sum().reset_index()[['type', 'count']]
data_7_path = save_data_to_csv(model_type_sales, 'data_7')

