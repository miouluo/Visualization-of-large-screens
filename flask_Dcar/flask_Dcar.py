from flask import Flask, render_template, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # 允许跨域请求
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:123456@localhost/car'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class CarSales(db.Model):
    __tablename__ = 'car_sales_copy1'
    id = db.Column(db.Integer, primary_key=True)
    series_name = db.Column(db.String(255))
    image = db.Column(db.String(255))
    rank = db.Column(db.Integer)
    count = db.Column(db.Integer)
    brand_name = db.Column(db.String(255))
    type = db.Column(db.String(255))
    sub_brand_name = db.Column(db.String(255))
    min_price = db.Column(db.Float)
    max_price = db.Column(db.Float)
    month = db.Column(db.String(255))

# 根路径
@app.route('/')
def index():
    return render_template('index.html')

# 获取品牌销量饼图数据
@app.route('/api/brand-sales', methods=['GET'])
def brand_sales():
    try:
        data = db.session.query(CarSales.brand_name, db.func.sum(CarSales.count)).group_by(CarSales.brand_name).order_by(db.func.sum(CarSales.count).desc()).limit(10).all()
        return jsonify([{ 'brand_name': brand, 'total_count': count } for brand, count in data])
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/api/china-sales', methods=['GET'])
def china_sales():
    try:
        # 先查询所有汽车品牌及其销量
        total_sales_data = db.session.query(
            CarSales.brand_name,
            db.func.sum(CarSales.count).label('total_count')
        ).group_by(CarSales.brand_name).all()

        # 将查询结果转换为字典
        total_sales = {brand_name: count for brand_name, count in total_sales_data}

        # 计算中国品牌和其他品牌的销量
        chinese_brands = [
            "五菱汽车", "长安", "吉利汽车", "奇瑞新能源", "零跑汽车", "荣威", "凌宝汽车", "北汽制造",
            "长安欧尚", "宝骏", "东风风光", "江铃集团新能源", "电动屋", "思皓", "小虎", "比亚迪", "欧拉",
            "埃安", "广汽传祺", "名爵", "曹操汽车", "北京汽车", "吉利几何", "小鹏汽车", "启辰",
            "东风风行", "东风富康", "广汽集团", "红旗", "深蓝汽车", "蔚来", "奔腾", "ARCFOX极狐",
            "高合", "岚图", "智己汽车", "东风纳米", "大运", "一汽", "哈弗", "坦克", "捷途", "北京",
            "海马", "SWM斯威汽车", "星途", "魏牌", "AITO", "蓝电", "中国重汽VGV", "睿蓝汽车",
            "理想汽车", "阿维塔", "上汽大通MAXUS", "江淮瑞风", "腾势"
        ]

        china_brand_sales = sum(total_sales.get(brand, 0) for brand in chinese_brands)
        total_sales_count = sum(total_sales.values())

        if total_sales_count > 0:
            china_sales_percentage = (china_brand_sales / total_sales_count) * 100
        else:
            china_sales_percentage = 0

        other_sales_percentage = 100 - china_sales_percentage

        return jsonify([
            {'brand_type': '中国品牌', 'total_count': china_brand_sales},
            {'brand_type': '其他品牌', 'total_count': total_sales_count - china_brand_sales}
        ])
    except Exception as e:
        print(f"Error: {e}")  # 打印错误信息到控制台
        return jsonify({"error": str(e)}), 500


# 获取销量前10的汽车系列
@app.route('/api/top-series', methods=['GET'])
def top_series():
    try:
        data = db.session.query(CarSales.series_name, CarSales.count).order_by(CarSales.count.desc()).limit(10).all()
        return jsonify([{ 'series_name': series, 'count': count } for series, count in data])
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# 获取汽车品牌销量柱状图数据（Top 10）
@app.route('/api/top-brands', methods=['GET'])
def top_brands():
    try:
        data = db.session.query(CarSales.brand_name, db.func.sum(CarSales.count)).group_by(CarSales.brand_name).order_by(db.func.sum(CarSales.count).desc()).limit(10).all()
        return jsonify([{ 'brand_name': brand, 'total_count': count } for brand, count in data])
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# 获取汽车销量词云数据
@app.route('/api/wordcloud', methods=['GET'])
def wordcloud():
    try:
        data = db.session.query(CarSales.series_name).all()
        wordcloud_text = ' '.join(series for (series,) in data)
        return jsonify({'text': wordcloud_text})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/type-sales', methods=['GET'])
def type_sales():
    data = db.session.query(CarSales.type, db.func.sum(CarSales.count)).group_by(CarSales.type).all()
    return jsonify([{ 'type': car_type, 'total_count': count } for car_type, count in data])

@app.route('/api/top-brands-line', methods=['GET'])
def top_brands_line():
    data = db.session.query(CarSales.brand_name, db.func.sum(CarSales.count)).group_by(CarSales.brand_name).order_by(db.func.sum(CarSales.count).desc()).limit(10).all()
    return jsonify([{ 'brand_name': brand, 'total_count': count } for brand, count in data])



# 启动应用
if __name__ == '__main__':
    app.run(debug=True)
