"""教师 MySQL 存储。"""

from typing import List, Optional

from app.database import get_connection
from app.schemas.teacher import TeacherCreate


class TeacherStore:
    """教师 MySQL 存储，支持增删改查。"""

    def create(self, data: TeacherCreate) -> dict:
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute(
            "INSERT INTO teachers (name, subject, title, phone) VALUES (%s, %s, %s, %s)",
            (data.name, data.subject, data.title, data.phone),
        )
        conn.commit()
        rid = cursor.lastrowid
        cursor.execute("SELECT * FROM teachers WHERE id = %s", (rid,))
        row = cursor.fetchone()
        cursor.close()
        conn.close()
        return row

    def get_all(self) -> List[dict]:
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM teachers")
        rows = cursor.fetchall()
        cursor.close()
        conn.close()
        return rows

    def get_by_id(self, teacher_id: int) -> Optional[dict]:
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM teachers WHERE id = %s", (teacher_id,))
        row = cursor.fetchone()
        cursor.close()
        conn.close()
        return row

    def update(self, teacher_id: int, data: dict) -> Optional[dict]:
        if not data:
            return self.get_by_id(teacher_id)
        set_parts = []
        values = []
        for k, v in data.items():
            if v is not None:
                set_parts.append(f"{k} = %s")
                values.append(v)
        if not set_parts:
            return self.get_by_id(teacher_id)
        values.append(teacher_id)
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute(
            f"UPDATE teachers SET {', '.join(set_parts)} WHERE id = %s",
            tuple(values),
        )
        conn.commit()
        if cursor.rowcount == 0:
            cursor.close()
            conn.close()
            return None
        cursor.execute("SELECT * FROM teachers WHERE id = %s", (teacher_id,))
        row = cursor.fetchone()
        cursor.close()
        conn.close()
        return row

    def delete(self, teacher_id: int) -> bool:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM teachers WHERE id = %s", (teacher_id,))
        ok = cursor.rowcount > 0
        conn.commit()
        cursor.close()
        conn.close()
        return ok


teacher_store = TeacherStore()
