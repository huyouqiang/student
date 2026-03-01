"""学生成绩 MySQL 存储。"""

from decimal import Decimal
from typing import Any, Dict, List, Optional

from app.database import get_connection
from app.schemas.grade import GradeCreate


def _normalize_grade_row(row: Optional[Dict[str, Any]]) -> Optional[Dict[str, Any]]:
    """将 Decimal 等类型转为 JSON 可序列化格式。"""
    if row is None:
        return None
    r = dict(row)
    if "score" in r and isinstance(r["score"], Decimal):
        r["score"] = float(r["score"])
    return r


class GradeStore:
    """成绩 MySQL 存储，支持增删改查。"""

    def create(self, data: GradeCreate) -> dict:
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute(
            "INSERT INTO grades (student_id, student_name, subject, score, exam_date, semester) "
            "VALUES (%s, %s, %s, %s, %s, %s)",
            (
                data.student_id,
                data.student_name,
                data.subject,
                data.score,
                data.exam_date,
                data.semester,
            ),
        )
        conn.commit()
        rid = cursor.lastrowid
        cursor.execute("SELECT * FROM grades WHERE id = %s", (rid,))
        row = _normalize_grade_row(cursor.fetchone())
        cursor.close()
        conn.close()
        return row

    def get_all(self, student_id: Optional[int] = None) -> List[dict]:
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        if student_id is not None:
            cursor.execute("SELECT * FROM grades WHERE student_id = %s", (student_id,))
        else:
            cursor.execute("SELECT * FROM grades")
        rows = [_normalize_grade_row(r) for r in cursor.fetchall()]
        cursor.close()
        conn.close()
        return rows

    def get_count(self, student_id: Optional[int] = None) -> int:
        """获取总记录数。"""
        conn = get_connection()
        cursor = conn.cursor()
        if student_id is not None:
            cursor.execute(
                "SELECT COUNT(*) FROM grades WHERE student_id = %s",
                (student_id,),
            )
        else:
            cursor.execute("SELECT COUNT(*) FROM grades")
        total = cursor.fetchone()[0]
        cursor.close()
        conn.close()
        return total

    def search_count(self, keyword: str, student_id: Optional[int] = None) -> int:
        """搜索条件下的总记录数。"""
        if not keyword or not keyword.strip():
            return self.get_count(student_id)
        conn = get_connection()
        cursor = conn.cursor()
        pattern = f"%{keyword.strip()}%"
        if student_id is not None:
            cursor.execute(
                "SELECT COUNT(*) FROM grades WHERE student_id = %s AND (student_name LIKE %s OR subject LIKE %s OR semester LIKE %s)",
                (student_id, pattern, pattern, pattern),
            )
        else:
            cursor.execute(
                "SELECT COUNT(*) FROM grades WHERE student_name LIKE %s OR subject LIKE %s OR semester LIKE %s",
                (pattern, pattern, pattern),
            )
        total = cursor.fetchone()[0]
        cursor.close()
        conn.close()
        return total

    def search_page(
        self,
        offset: int,
        limit: int,
        keyword: str,
        student_id: Optional[int] = None,
    ) -> List[dict]:
        """分页搜索成绩列表。"""
        if not keyword or not keyword.strip():
            return self.get_page(offset, limit, student_id)
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        pattern = f"%{keyword.strip()}%"
        if student_id is not None:
            cursor.execute(
                "SELECT * FROM grades WHERE student_id = %s AND (student_name LIKE %s OR subject LIKE %s OR semester LIKE %s) ORDER BY id LIMIT %s OFFSET %s",
                (student_id, pattern, pattern, pattern, limit, offset),
            )
        else:
            cursor.execute(
                "SELECT * FROM grades WHERE student_name LIKE %s OR subject LIKE %s OR semester LIKE %s ORDER BY id LIMIT %s OFFSET %s",
                (pattern, pattern, pattern, limit, offset),
            )
        rows = [_normalize_grade_row(r) for r in cursor.fetchall()]
        cursor.close()
        conn.close()
        return rows

    def get_page(
        self,
        offset: int,
        limit: int,
        student_id: Optional[int] = None,
    ) -> List[dict]:
        """分页获取成绩列表。"""
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        if student_id is not None:
            cursor.execute(
                "SELECT * FROM grades WHERE student_id = %s ORDER BY id LIMIT %s OFFSET %s",
                (student_id, limit, offset),
            )
        else:
            cursor.execute(
                "SELECT * FROM grades ORDER BY id LIMIT %s OFFSET %s",
                (limit, offset),
            )
        rows = [_normalize_grade_row(r) for r in cursor.fetchall()]
        cursor.close()
        conn.close()
        return rows

    def get_by_id(self, grade_id: int) -> Optional[dict]:
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM grades WHERE id = %s", (grade_id,))
        row = _normalize_grade_row(cursor.fetchone())
        cursor.close()
        conn.close()
        return row

    def update(self, grade_id: int, data: dict) -> Optional[dict]:
        if not data:
            return self.get_by_id(grade_id)
        set_parts = []
        values = []
        for k, v in data.items():
            if v is not None:
                set_parts.append(f"{k} = %s")
                values.append(v)
        if not set_parts:
            return self.get_by_id(grade_id)
        values.append(grade_id)
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute(
            f"UPDATE grades SET {', '.join(set_parts)} WHERE id = %s",
            tuple(values),
        )
        conn.commit()
        if cursor.rowcount == 0:
            cursor.close()
            conn.close()
            return None
        cursor.execute("SELECT * FROM grades WHERE id = %s", (grade_id,))
        row = _normalize_grade_row(cursor.fetchone())
        cursor.close()
        conn.close()
        return row

    def delete(self, grade_id: int) -> bool:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM grades WHERE id = %s", (grade_id,))
        ok = cursor.rowcount > 0
        conn.commit()
        cursor.close()
        conn.close()
        return ok


grade_store = GradeStore()
