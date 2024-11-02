import pandas as pd
import matplotlib.pyplot as plt
from wordcloud import WordCloud
import numpy as np
plt.rcParams['font.sans-serif'] = ['SimHei']

# 读取数据
file_path = 'data/Dcar.csv'
df = pd.read_csv(file_path)

# 定义颜色
colors_pie = ['#ff9999','#66b3ff','#99ff99','#ffcc99']
colors_bar = ['#c2c2f0','#ffb3e6','#c4e17f','#76ddfb']
colors_line = ['#fc8d62','#66c2a5','#8da0cb','#e78ac3']
colors_wordcloud = ['#c2c2f0','#ffb3e6','#c4e17f','#76ddfb','#fc8d62','#66c2a5','#8da0cb','#e78ac3']

# 1. 汽车品牌销量饼图
brand_sales_data = df.groupby('brand_name')['count'].sum().reset_index()
# 排序并选择前10个品牌
top_brands_data = brand_sales_data.nlargest(10, 'count')

plt.figure(figsize=(8, 8))
plt.pie(top_brands_data['count'], labels=top_brands_data['brand_name'], autopct='%1.1f%%', colors=colors_pie, startangle=140)
plt.title('汽车品牌销量饼图')
plt.savefig('./Chart/brand_sales_pie_chart.png')
plt.close()


# 2. 中国汽车销量占比
unique_brands = df['brand_name'].unique()
# print(unique_brands)
# ['五菱汽车' '长安' '吉利汽车' '奇瑞新能源' '零跑汽车' '荣威' '凌宝汽车' '北汽制造' '长安欧尚' '宝骏' '东风风光'
#  '江铃集团新能源' '电动屋' '思皓' '小虎' '比亚迪' '欧拉' '本田' '大众' '江淮钇为' '起亚' '日产' '埃安' '丰田'
#  '别克' '现代' '雪佛兰' '捷达' '奔驰' '奥迪' '奇瑞' '领克' '东风风神' '广汽传祺' '名爵' '曹操汽车' '北京汽车'
#  '马自达' '吉利几何' '小鹏汽车' '凯翼' '启辰' '标致' '国金汽车' '斯柯达' '东风风行' '东风富康' '广汽集团' '东南'
#  '宝马' '特斯拉' '凯迪拉克' '红旗' '深蓝汽车' '福特' '蔚来' '奔腾' '雪铁龙' '沃尔沃' '林肯' '捷豹' '英菲尼迪'
#  '合创汽车' 'DS' '极氪' '飞凡汽车' '哪吒汽车' 'ARCFOX极狐' '高合' '岚图' '智己汽车' '东风纳米' 'smart'
#  '大运' '一汽' '思铭' '理念' '哈弗' '坦克' '捷途' '北京' '海马' 'SWM斯威汽车' '星途' '魏牌' 'AITO'
#  '路虎' '创维汽车' '蓝电' '中国重汽VGV' '睿蓝汽车' '理想汽车' '阿维塔' '上汽大通MAXUS' '江淮瑞风' '腾势']

chinese_brands = [
    "五菱汽车", "长安", "吉利汽车", "奇瑞新能源", "零跑汽车", "荣威", "凌宝汽车", "北汽制造",
    "长安欧尚", "宝骏", "东风风光", "江铃集团新能源", "电动屋", "思皓", "小虎", "比亚迪", "欧拉",
    "埃安", "广汽传祺", "名爵", "曹操汽车", "北京汽车", "吉利几何", "小鹏汽车", "启辰",
    "东风风行", "东风富康", "广汽集团", "红旗", "深蓝汽车", "蔚来", "奔腾", "ARCFOX极狐",
    "高合", "岚图", "智己汽车", "东风纳米", "大运", "一汽", "哈弗", "坦克", "捷途", "北京",
    "海马", "SWM斯威汽车", "星途", "魏牌", "AITO", "蓝电", "中国重汽VGV", "睿蓝汽车",
    "理想汽车", "阿维塔", "上汽大通MAXUS", "江淮瑞风", "腾势"
]

# 使用更新后的中国品牌列表来计算中国品牌汽车的销量占比
china_brand_sales = df[df['brand_name'].isin(chinese_brands)]['count'].sum()
total_sales = df['count'].sum()
china_sales_percentage = (china_brand_sales / total_sales) * 100
other_sales_percentage = 100 - china_sales_percentage

# 绘制中国汽车销量占比柱状图
plt.figure(figsize=(6, 4))
plt.bar(['中国品牌', '其他品牌'], [china_sales_percentage, other_sales_percentage], color=colors_bar[:2])
plt.title('中国汽车销量占比')
plt.savefig('./Chart/china_sales_percentage_chart.png')
plt.close()

# 3. 汽车品牌销量柱状图 (Top 10)
plt.figure(figsize=(10, 6))
top_brands = df.groupby('brand_name')['count'].sum().nlargest(10)
top_brands.plot(kind='bar', color=colors_bar)
plt.title('汽车品牌销量柱状图 (Top 10)')
plt.xlabel('品牌名称')
plt.ylabel('销量')
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig('./Chart/top_brands_sales_chart.png')
plt.close()

# 4. 汽车销量前10排行柱状图
plt.figure(figsize=(10, 6))
top_series = df.nlargest(10, 'count')[['series_name', 'count']]
top_series.plot(kind='bar', x='series_name', color=colors_bar)
plt.title('汽车销量前10排行柱状图')
plt.xlabel('汽车系列')
plt.ylabel('销量')
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig('./Chart/top_series_sales_chart.png')
plt.close()

# 5. 汽车厂商销量折线图 (Top 10)
plt.figure(figsize=(10, 6))
top_brands_line = df.groupby('brand_name')['count'].sum().nlargest(10)
top_brands_line.plot(kind='line', marker='o', color=colors_line)
plt.title('汽车品牌销量折线图 (Top 10)')
plt.xlabel('品牌名称')
plt.ylabel('销量')
plt.xticks(rotation=45, ha='right')
plt.tight_layout()
plt.savefig('./Chart/top_brands_line_chart.png')
plt.close()

# 6. 汽车销量词云图
wordcloud_text = ' '.join(df['series_name'].astype(str))
wordcloud = WordCloud(width=800, height=400, background_color='white', 
                      color_func=lambda *args, **kwargs: colors_wordcloud[np.random.randint(0, len(colors_wordcloud))],
                      font_path='C:\Windows\Fonts\STCAIYUN.TTF').generate(wordcloud_text)
plt.figure(figsize=(10, 5))
plt.imshow(wordcloud, interpolation='bilinear')
plt.axis('off')
plt.title('汽车销量词云图')
plt.savefig('./Chart/wordcloud_chart.png')
plt.close()

# 7. 汽车型型销量
plt.figure(figsize=(10, 6))
type_sales = df.groupby('type')['count'].sum()
type_sales.plot(kind='bar', color=colors_bar)
plt.title('汽车车型销量')
plt.xlabel('车型')
plt.ylabel('销量')
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig('./Chart/type_sales_chart.png')
plt.close()

image_paths = [
    './Chart/brand_sales_pie_chart.png',
    './Chart/china_sales_percentage_chart.png',
    './Chart/top_brands_sales_chart.png',
    './Chart/top_series_sales_chart.png',
    './Chart/top_brands_line_chart.png'
    './Chart/wordcloud_chart.png'
    './Chart/type_sales_chart.png'
]





