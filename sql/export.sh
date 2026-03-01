#!/bin/bash
# 导出 student 数据库到 school.sql
# 使用方式: ./sql/export.sh 或 bash sql/export.sh

cd "$(dirname "$0")/.."

MYSQL_HOST="${MYSQL_HOST:-localhost}"
MYSQL_USER="${MYSQL_USER:-root}"
MYSQL_DATABASE="${MYSQL_DATABASE:-student}"

mysqldump -h "$MYSQL_HOST" -u "$MYSQL_USER" -p "$MYSQL_DATABASE" > sql/school.sql

echo "导出完成: sql/school.sql"
