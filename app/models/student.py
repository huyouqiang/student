"""学生 MySQL 存储。"""

from typing import List, Optional

from app.database import get_connection
from app.schemas.student import StudentCreate


class StudentStore:
    """学生 MySQL 存储，支持增删改查。"""

    def create(self, data: StudentCreate) -> dict:
        """新增学生，返回完整记录。"""
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute(
            "INSERT INTO students (name, age, grade) VALUES (%s, %s, %s)",
            (data.name, data.age, data.grade),
        )
        conn.commit()
        rid = cursor.lastrowid
        cursor.execute("SELECT * FROM students WHERE id = %s", (rid,))
        row = cursor.fetchone()
        cursor.close()
        conn.close()
        return row

    def get_all(self) -> List[dict]:
        """获取全部学生列表。"""
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM students")
        rows = cursor.fetchall()
        cursor.close()
        conn.close()
        return rows

    def get_count(self) -> int:
        """获取总记录数。"""
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM students")
        total = cursor.fetchone()[0]
        cursor.close()
        conn.close()
        return total

    def get_page(self, offset: int, limit: int) -> List[dict]:
        """分页获取学生列表。"""
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute(
            "SELECT * FROM students ORDER BY id LIMIT %s OFFSET %s",
            (limit, offset),
        )
        rows = cursor.fetchall()
        cursor.close()
        conn.close()
        return rows

    def search(self, keyword: str, limit: int = 20) -> List[dict]:
        """按姓名或年级搜索学生。"""
        if not keyword or not keyword.strip():
            return []
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        pattern = f"%{keyword.strip()}%"
        cursor.execute(
            "SELECT * FROM students WHERE name LIKE %s OR grade LIKE %s ORDER BY id LIMIT %s",
            (pattern, pattern, limit),
        )
        rows = cursor.fetchall()
        cursor.close()
        conn.close()
        return rows

    def search_count(self, keyword: str) -> int:
        """搜索条件下的总记录数。"""
        if not keyword or not keyword.strip():
            return self.get_count()
        conn = get_connection()
        cursor = conn.cursor()
        pattern = f"%{keyword.strip()}%"
        cursor.execute(
            "SELECT COUNT(*) FROM students WHERE name LIKE %s OR grade LIKE %s",
            (pattern, pattern),
        )
        total = cursor.fetchone()[0]
        cursor.close()
        conn.close()
        return total

    def search_page(self, offset: int, limit: int, keyword: str) -> List[dict]:
        """分页搜索学生。"""
        if not keyword or not keyword.strip():
            return self.get_page(offset, limit)
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        pattern = f"%{keyword.strip()}%"
        cursor.execute(
            "SELECT * FROM students WHERE name LIKE %s OR grade LIKE %s ORDER BY id LIMIT %s OFFSET %s",
            (pattern, pattern, limit, offset),
        )
        rows = cursor.fetchall()
        cursor.close()
        conn.close()
        return rows

    def get_by_id(self, student_id: int) -> Optional[dict]:
        """根据 id 获取学生。"""
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM students WHERE id = %s", (student_id,))
        row = cursor.fetchone()
        cursor.close()
        conn.close()
        return row

    def update(self, student_id: int, data: dict) -> Optional[dict]:
        """更新学生，只更新传入的字段。"""
        if not data:
            return self.get_by_id(student_id)
        set_parts = []
        values = []
        for k, v in data.items():
            if v is not None:
                set_parts.append(f"{k} = %s")
                values.append(v)
        if not set_parts:
            return self.get_by_id(student_id)
        values.append(student_id)
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute(
            f"UPDATE students SET {', '.join(set_parts)} WHERE id = %s",
            tuple(values),
        )
        conn.commit()
        if cursor.rowcount == 0:
            cursor.close()
            conn.close()
            return None
        cursor.execute("SELECT * FROM students WHERE id = %s", (student_id,))
        row = cursor.fetchone()
        cursor.close()
        conn.close()
        return row

    def delete(self, student_id: int) -> bool:
        """删除学生。"""
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM students WHERE id = %s", (student_id,))
        ok = cursor.rowcount > 0
        conn.commit()
        cursor.close()
        conn.close()
        return ok


student_store = StudentStore()
