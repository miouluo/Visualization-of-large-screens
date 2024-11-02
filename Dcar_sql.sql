-- 创建数据库数据表
CREATE DATABASE IF NOT EXISTS car DEFAULT CHARSET utf8mb4 COLLATE utf8mb4_unicode_ci;

CREATE TABLE IF NOT EXISTS car_sales_copy1 (
    id INT AUTO_INCREMENT PRIMARY KEY,
    series_name VARCHAR(255),
    image VARCHAR(255),
    `rank` INT,
    COUNT INT,
    brand_name VARCHAR(255),
    TYPE VARCHAR(255),
    sub_brand_name VARCHAR(255),
    min_price DECIMAL(10, 2),
    max_price DECIMAL(10, 2),
    MONTH VARCHAR(255)
) DEFAULT CHARSET utf8mb4 COLLATE utf8mb4_unicode_ci;

-- 展示mysql默认文件存放位置
SHOW VARIABLES LIKE 'secure_file_priv';

-- 导出文件
SELECT 'id', 'series_name', 'image', 'rank', 'count', 'brand_name', 'type', 'sub_brand_name', 'min_price', 'max_price', 'month'
UNION ALL
SELECT 
    id, 
    series_name, 
    image, 
    `rank`, 
    `count`, 
    brand_name, 
    `type`, 
    sub_brand_name, 
    min_price, 
    max_price, 
    `month`
FROM car_sales_copy1
INTO OUTFILE 'C:/ProgramData/MySQL/MySQL Server 8.0/Uploads/Dcar.csv'
FIELDS TERMINATED BY ','
ENCLOSED BY '"'
LINES TERMINATED BY '\n';



