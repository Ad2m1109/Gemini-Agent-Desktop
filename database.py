import sqlite3
from dataclasses import dataclass
from datetime import datetime
from typing import List, Optional
from pathlib import Path

@dataclass
class ChatTurn:
    id: int
    session_id: int
    prompt: str
    response: str
    timestamp: datetime
    file_modified: Optional[str] = None
    version_snapshot: Optional[str] = None

class Database:
    def __init__(self, db_path: str = "agent_data.db"):
        self.db_path = db_path
        self._init_db()

    def _init_db(self):
        """Initialize the database schema if it doesn't exist"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            # Create sessions table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS sessions (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    project_path TEXT NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)

            # Create chat_turns table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS chat_turns (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    session_id INTEGER,
                    prompt TEXT NOT NULL,
                    response TEXT NOT NULL,
                    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    file_modified TEXT,
                    version_snapshot TEXT,
                    FOREIGN KEY (session_id) REFERENCES sessions(id)
                )
            """)
            conn.commit()

    def create_session(self, project_path: str) -> int:
        """Create a new chat session for a project"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO sessions (project_path) VALUES (?)",
                (project_path,)
            )
            conn.commit()
            return cursor.lastrowid

    def add_chat_turn(self, session_id: int, prompt: str, response: str,
                     file_modified: Optional[str] = None,
                     version_snapshot: Optional[str] = None) -> int:
        """Add a new chat turn to a session"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO chat_turns 
                (session_id, prompt, response, file_modified, version_snapshot)
                VALUES (?, ?, ?, ?, ?)
            """, (session_id, prompt, response, file_modified, version_snapshot))
            conn.commit()
            return cursor.lastrowid

    def get_session_history(self, session_id: int) -> List[ChatTurn]:
        """Get all chat turns for a session"""
        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            cursor.execute("""
                SELECT * FROM chat_turns 
                WHERE session_id = ? 
                ORDER BY timestamp
            """, (session_id,))
            
            turns = []
            for row in cursor.fetchall():
                turn = ChatTurn(
                    id=row['id'],
                    session_id=row['session_id'],
                    prompt=row['prompt'],
                    response=row['response'],
                    timestamp=datetime.fromisoformat(row['timestamp']),
                    file_modified=row['file_modified'],
                    version_snapshot=row['version_snapshot']
                )
                turns.append(turn)
            
            return turns

    def get_version_snapshot(self, turn_id: int) -> Optional[str]:
        """Get the version snapshot path for a specific chat turn"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute(
                "SELECT version_snapshot FROM chat_turns WHERE id = ?",
                (turn_id,)
            )
            result = cursor.fetchone()
            return result[0] if result else None