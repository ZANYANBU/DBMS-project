"""Smoke tests for the School Management System.

Run with:  pytest

Each test works on a throwaway copy of the database, so the real
school_management.db is never changed.
"""

import os
import shutil
import sqlite3
import sys

import pytest

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)

import app as school  # noqa: E402


@pytest.fixture()
def client(tmp_path, monkeypatch):
    db = tmp_path / "school.db"
    shutil.copy(os.path.join(ROOT, "school_management.db"), db)
    monkeypatch.setattr(school, "DB_NAME", str(db))
    school.app.config.update(TESTING=True)
    with school.app.test_client() as c:
        yield c


def login(client, username, password):
    return client.post("/login", data={"username": username, "password": password})


def test_database_has_the_core_tables():
    conn = sqlite3.connect(os.path.join(ROOT, "school_management.db"))
    tables = {row[0] for row in conn.execute("SELECT name FROM sqlite_master WHERE type='table'")}
    conn.close()
    assert {"Student", "Staff", "Course", "Class", "Enrollment", "User_Login"} <= tables


def test_foreign_keys_are_enforced(client):
    conn = school.get_db()
    assert conn.execute("PRAGMA foreign_keys").fetchone()[0] == 1
    assert conn.execute("PRAGMA foreign_key_check").fetchall() == []
    conn.close()


def test_public_pages_load(client):
    assert client.get("/").status_code == 200
    assert client.get("/login").status_code == 200


@pytest.mark.parametrize("path", ["/dashboard", "/admin/dashboard", "/admin/students",
                                  "/admin/sql-console", "/staff/dashboard", "/student/grades"])
def test_pages_need_a_login(client, path):
    response = client.get(path)
    assert response.status_code == 302
    assert "/login" in response.headers["Location"]


def test_a_wrong_password_is_rejected(client):
    response = login(client, "admin", "not-the-password")
    assert response.status_code == 200
    assert b"Invalid username or password" in response.data


def test_admin_can_log_in_and_see_the_dashboard(client):
    response = login(client, "admin", "admin123")
    assert response.status_code == 302
    assert client.get("/dashboard").headers["Location"].endswith("/admin/dashboard")
    assert client.get("/admin/dashboard").status_code == 200
    assert client.get("/admin/students").status_code == 200


def test_logging_out_ends_the_session(client):
    login(client, "admin", "admin123")
    client.get("/logout")
    assert client.get("/admin/dashboard").status_code == 302


def test_passwords_are_stored_hashed():
    assert school.hash_password("admin123") != "admin123"
    assert school.hash_password("admin123") == school.hash_password("admin123")
