"""学校 MySQL 存储。"""

from typing import List, Optional

from app.database import get_connection
from app.schemas.school import SchoolCreate


class SchoolStore:
    """学校 MySQL 存储，支持增删改查。"""

    def create(self, data: SchoolCreate) -> dict:
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute(
            "INSERT INTO schools (name, address, school_type, student_count) "
            "VALUES (%s, %s, %s, %s)",
            (data.name, data.address, data.school_type, data.student_count),
        )
        conn.commit()
        rid = cursor.lastrowid
        cursor.execute("SELECT * FROM schools WHERE id = %s", (rid,))
        row = cursor.fetchone()
        cursor.close()
        conn.close()
        return row

    def get_all(self) -> List[dict]:
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM schools")
        rows = cursor.fetchall()
        cursor.close()
        conn.close()
        return rows

    def get_by_id(self, school_id: int) -> Optional[dict]:
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM schools WHERE id = %s", (school_id,))
        row = cursor.fetchone()
        cursor.close()
        conn.close()
        return row

    def update(self, school_id: int, data: dict) -> Optional[dict]:
        if not data:
            return self.get_by_id(school_id)
        set_parts = []
        values = []
        for k, v in data.items():
            if v is not None:
                set_parts.append(f"{k} = %s")
                values.append(v)
        if not set_parts:
            return self.get_by_id(school_id)
        values.append(school_id)
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute(
            f"UPDATE schools SET {', '.join(set_parts)} WHERE id = %s",
            tuple(values),
        )
        conn.commit()
        if cursor.rowcount == 0:
            cursor.close()
            conn.close()
            return None
        cursor.execute("SELECT * FROM schools WHERE id = %s", (school_id,))
        row = cursor.fetchone()
        cursor.close()
        conn.close()
        return row

    def delete(self, school_id: int) -> bool:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM schools WHERE id = %s", (school_id,))
        ok = cursor.rowcount > 0
        conn.commit()
        cursor.close()
        conn.close()
        return ok


school_store = SchoolStore()
