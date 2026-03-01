#!/bin/bash
# 导出 student 数据库到 school.sql（含所有数据）
# 使用方式: ./sql/export.sh 或 bash sql/export.sh

cd "$(dirname "$0")/.."

MYSQL_HOST="${MYSQL_HOST:-localhost}"
MYSQL_USER="${MYSQL_USER:-root}"
MYSQL_PASSWORD="${MYSQL_PASSWORD:-}"
MYSQL_DATABASE="${MYSQL_DATABASE:-student}"

PASS_ARG=""
[[ -n "$MYSQL_PASSWORD" ]] && PASS_ARG="--password=$MYSQL_PASSWORD"

if mysqldump -h "$MYSQL_HOST" -u "$MYSQL_USER" $PASS_ARG "$MYSQL_DATABASE" > sql/school.sql; then
  echo "导出完成: sql/school.sql"
else
  echo "导出失败，请检查 MySQL 是否运行以及 MYSQL_HOST/USER/PASSWORD/DATABASE 配置"
  exit 1
fi
