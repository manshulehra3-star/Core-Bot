import os
import aiosqlite
import json
import logging
from typing import Any, Dict, List, Optional

logger = logging.getLogger("InfiniteCore.Database")

class Database:
    def __init__(self, db_path: str = "./data/infinite_core.db"):
        self.db_path = db_path
        os.makedirs(os.path.dirname(self.db_path), exist_ok=True)

    async def get_connection(self) -> aiosqlite.Connection:
        conn = await aiosqlite.connect(self.db_path)
        conn.row_factory = aiosqlite.Row
        await conn.execute("PRAGMA foreign_keys = ON;")
        return conn

    async def init_db(self):
        async with await self.get_connection() as db:
            await db.executescript("""
            CREATE TABLE IF NOT EXISTS users (
                user_id INTEGER PRIMARY KEY,
                username TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );

            CREATE TABLE IF NOT EXISTS ticket_categories (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT UNIQUE NOT NULL,
                emoji TEXT DEFAULT '🎫',
                description TEXT,
                category_id INTEGER,
                staff_role_id INTEGER,
                ping_role_id INTEGER,
                welcome_msg TEXT,
                auto_close_hours INTEGER DEFAULT 24,
                transcripts_enabled INTEGER DEFAULT 1,
                priority TEXT DEFAULT 'Medium',
                ai_enabled INTEGER DEFAULT 1,
                max_tickets_per_user INTEGER DEFAULT 3
            );

            CREATE TABLE IF NOT EXISTS tickets (
                ticket_id TEXT PRIMARY KEY,
                channel_id INTEGER UNIQUE,
                guild_id INTEGER,
                user_id INTEGER,
                category_name TEXT,
                status TEXT DEFAULT 'open',
                claimed_by INTEGER DEFAULT NULL,
                priority TEXT DEFAULT 'Medium',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                closed_at TIMESTAMP DEFAULT NULL,
                FOREIGN KEY (user_id) REFERENCES users(user_id)
            );

            CREATE TABLE IF NOT EXISTS ticket_messages (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                ticket_id TEXT,
                author_id INTEGER,
                author_name TEXT,
                content TEXT,
                timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (ticket_id) REFERENCES tickets(ticket_id)
            );

            CREATE TABLE IF NOT EXISTS plans (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT UNIQUE NOT NULL,
                category TEXT NOT NULL, -- VPS, Minecraft, Other
                price REAL NOT NULL,
                billing_period TEXT DEFAULT 'Monthly',
                ram TEXT,
                cpu TEXT,
                disk TEXT,
                bandwidth TEXT,
                slots INTEGER DEFAULT 0,
                description TEXT,
                features TEXT, -- JSON array
                plan_url TEXT,
                panel_plan_id TEXT,
                enabled INTEGER DEFAULT 1
            );

            CREATE TABLE IF NOT EXISTS promo_codes (
                code TEXT PRIMARY KEY,
                plan_name TEXT,
                discount_type TEXT NOT NULL, -- percentage or fixed
                discount_value REAL NOT NULL,
                usage_limit INTEGER DEFAULT 100,
                used_count INTEGER DEFAULT 0,
                min_amount REAL DEFAULT 0.0,
                expires_at TIMESTAMP,
                enabled INTEGER DEFAULT 1
            );

            CREATE TABLE IF NOT EXISTS promo_usage (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                code TEXT,
                user_id INTEGER,
                used_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (code) REFERENCES promo_codes(code)
            );

            CREATE TABLE IF NOT EXISTS payment_methods (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT UNIQUE NOT NULL,
                details TEXT NOT NULL,
                instructions TEXT,
                enabled INTEGER DEFAULT 1
            );

            CREATE TABLE IF NOT EXISTS payments (
                payment_id TEXT PRIMARY KEY,
                user_id INTEGER NOT NULL,
                amount REAL NOT NULL,
                original_amount REAL NOT NULL,
                promo_code TEXT,
                method TEXT,
                status TEXT DEFAULT 'pending', -- pending, waiting_approval, approved, rejected
                target_user_id INTEGER,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );

            CREATE TABLE IF NOT EXISTS payment_submissions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                payment_id TEXT NOT NULL,
                user_id INTEGER NOT NULL,
                screenshot_url TEXT NOT NULL,
                submitted_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                status TEXT DEFAULT 'pending',
                reviewed_by INTEGER,
                reviewed_at TIMESTAMP,
                FOREIGN KEY (payment_id) REFERENCES payments(payment_id)
            );

            CREATE TABLE IF NOT EXISTS qr_config (
                id INTEGER PRIMARY KEY CHECK (id = 1),
                image_path_or_url TEXT NOT NULL,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );

            CREATE TABLE IF NOT EXISTS links (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                url TEXT NOT NULL,
                category TEXT DEFAULT 'Website',
                enabled INTEGER DEFAULT 1
            );

            CREATE TABLE IF NOT EXISTS panel_configs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                panel_type TEXT NOT NULL, -- Pterodactyl, SVM, HVM, Puffer, Custom
                api_url TEXT NOT NULL,
                api_key TEXT NOT NULL,
                enabled INTEGER DEFAULT 1
            );

            CREATE TABLE IF NOT EXISTS welcome_config (
                guild_id INTEGER PRIMARY KEY,
                channel_id INTEGER,
                leave_channel_id INTEGER,
                dm_enabled INTEGER DEFAULT 1,
                welcome_message TEXT,
                leave_message TEXT,
                dm_message TEXT
            );

            CREATE TABLE IF NOT EXISTS announcement_config (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                guild_id INTEGER,
                title TEXT,
                content TEXT,
                channel_id INTEGER,
                scheduled_time TIMESTAMP,
                status TEXT DEFAULT 'pending'
            );

            CREATE TABLE IF NOT EXISTS security_config (
                guild_id INTEGER PRIMARY KEY,
                anti_spam INTEGER DEFAULT 1,
                anti_mention INTEGER DEFAULT 1,
                max_mentions INTEGER DEFAULT 5,
                anti_raid INTEGER DEFAULT 1,
                anti_invite INTEGER DEFAULT 1,
                anti_links INTEGER DEFAULT 0,
                action TEXT DEFAULT 'timeout'
            );

            CREATE TABLE IF NOT EXISTS moderation_logs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                guild_id INTEGER,
                user_id INTEGER,
                moderator_id INTEGER,
                action TEXT,
                reason TEXT,
                timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );

            CREATE TABLE IF NOT EXISTS provisioning_jobs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                payment_id TEXT UNIQUE,
                user_id INTEGER,
                plan_id INTEGER,
                panel_type TEXT,
                status TEXT DEFAULT 'pending', -- pending, processing, completed, failed
                details TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
            """)
            await db.commit()
            await self._seed_defaults(db)
        logger.info("Database initialized successfully.")

    async def _seed_defaults(self, db: aiosqlite.Connection):
        # Seed default payment methods
        methods = [
            ("Google Pay", "Pay via GPay UPI ID / QR"),
            ("PhonePe", "Pay via PhonePe UPI ID / QR"),
            ("Paytm", "Pay via Paytm Wallet / UPI"),
            ("UPI", "Direct UPI Payment"),
            ("PayPal", "PayPal Invoice / Transfer"),
            ("QR", "Scan QR Code for Instant Payment"),
            ("Bank Transfer", "Direct NEFT/IMPS Bank Transfer")
        ]
        for name, details in methods:
            await db.execute(
                "INSERT OR IGNORE INTO payment_methods (name, details) VALUES (?, ?)",
                (name, details)
            )

        # Seed default ticket categories
        ticket_cats = [
            ("Purchase", "🛒", "Order new VPS or Minecraft server hosting"),
            ("VPS Support", "🖥️", "Technical issues with your Virtual Private Server"),
            ("Minecraft Support", "⛏️", "Minecraft server configuration & performance help"),
            ("Billing", "💳", "Invoices, payment issues, and renewal assistance"),
            ("Technical Support", "🛠️", "General technical and infrastructure assistance"),
            ("Partnership", "🤝", "Sponsorship and business partnership inquiries"),
            ("General Support", "💬", "General questions about Infinite Core services"),
            ("Other", "❓", "Miscellaneous queries not covered above")
        ]
        for name, emoji, desc in ticket_cats:
            await db.execute(
                "INSERT OR IGNORE INTO ticket_categories (name, emoji, description) VALUES (?, ?, ?)",
                (name, emoji, desc)
            )
        await db.commit()

    async def execute(self, query: str, params: tuple = ()) -> aiosqlite.Cursor:
        async with await self.get_connection() as db:
            cursor = await db.execute(query, params)
            await db.commit()
            return cursor

    async def fetchone(self, query: str, params: tuple = ()) -> Optional[Dict[str, Any]]:
        async with await self.get_connection() as db:
            async with db.execute(query, params) as cursor:
                row = await cursor.fetchone()
                return dict(row) if row else None

    async def fetchall(self, query: str, params: tuple = ()) -> List[Dict[str, Any]]:
        async with await self.get_connection() as db:
            async with db.execute(query, params) as cursor:
                rows = await cursor.fetchall()
                return [dict(r) for r in rows]
          
