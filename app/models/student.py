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
