"""MySQL 数据库连接与表初始化。"""

import os

import mysql.connector

DB_CONFIG = {
    "host": os.environ.get("MYSQL_HOST", "localhost"),
    "user": os.environ.get("MYSQL_USER", "root"),
    "password": os.environ.get("MYSQL_PASSWORD", ""),
    "database": os.environ.get("MYSQL_DATABASE", "student"),
}


def get_connection():
    """获取数据库连接。"""
    return mysql.connector.connect(**DB_CONFIG)


def init_db() -> None:
    """创建数据库和表（若不存在）。"""
    # 先连接不指定 database，创建库
    conn = mysql.connector.connect(
        host=DB_CONFIG["host"],
        user=DB_CONFIG["user"],
        password=DB_CONFIG["password"],
    )
    cursor = conn.cursor()
    cursor.execute(
        "CREATE DATABASE IF NOT EXISTS student "
        "DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci"
    )
    cursor.close()
    conn.close()

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS students (
            id INT AUTO_INCREMENT PRIMARY KEY,
            name VARCHAR(100) NOT NULL,
            age INT NOT NULL,
            grade VARCHAR(50) DEFAULT ''
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS teachers (
            id INT AUTO_INCREMENT PRIMARY KEY,
            name VARCHAR(100) NOT NULL,
            subject VARCHAR(50) DEFAULT '',
            title VARCHAR(50) DEFAULT '',
            phone VARCHAR(20) DEFAULT ''
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS schools (
            id INT AUTO_INCREMENT PRIMARY KEY,
            name VARCHAR(100) NOT NULL,
            address VARCHAR(200) DEFAULT '',
            school_type VARCHAR(20) DEFAULT '',
            student_count INT DEFAULT 0
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS grades (
            id INT AUTO_INCREMENT PRIMARY KEY,
            student_id INT NULL,
            student_name VARCHAR(100) NOT NULL,
            subject VARCHAR(50) NOT NULL,
            score DECIMAL(5,2) NOT NULL,
            exam_date VARCHAR(20) DEFAULT '',
            semester VARCHAR(50) DEFAULT ''
        )
    """)

    conn.commit()
    cursor.close()
    conn.close()
