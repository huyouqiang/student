"""用户 MySQL 存储。"""

from typing import Optional

from app.database import get_connection


class UserStore:
    """用户存储，用于登录校验。"""

    def get_by_name(self, name: str) -> Optional[dict]:
        """根据用户名获取用户。"""
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT id, name, pass, role FROM users WHERE name = %s", (name,))
        row = cursor.fetchone()
        cursor.close()
        conn.close()
        return row

    def verify(self, name: str, password_hash: str) -> Optional[dict]:
        """校验用户名和密码，返回用户信息（不含密码）。"""
        user = self.get_by_name(name)
        if user and user["pass"] == password_hash:
            return {"id": user["id"], "name": user["name"], "role": user["role"]}
        return None


user_store = UserStore()
