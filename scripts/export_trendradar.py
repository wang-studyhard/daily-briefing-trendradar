import argparse
import json
import sqlite3
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import urlparse


def valid_url(value: str) -> bool:
    parsed = urlparse(value or "")
    return parsed.scheme in {"http", "https"} and bool(parsed.netloc)


def export_feed(database: Path, output: Path, limit: int = 200) -> None:
    connection = sqlite3.connect(database)
    try:
        rows = connection.execute(
            """
            SELECT n.title, p.name, n.rank, n.url, n.last_crawl_time
            FROM news_items n
            LEFT JOIN platforms p ON p.id = n.platform_id
            WHERE n.title IS NOT NULL AND n.url IS NOT NULL AND n.url != ''
            ORDER BY n.rank ASC, n.last_crawl_time DESC
            LIMIT ?
            """,
            (limit,),
        ).fetchall()
    finally:
        connection.close()

    items = []
    seen_urls = set()
    for index, (title, source, rank, url, published_at) in enumerate(rows, start=1):
        if not title or not valid_url(url) or url in seen_urls:
            continue
        seen_urls.add(url)
        items.append(
            {
                "title": title.strip(),
                "source": (source or "TrendRadar").strip(),
                "rank": int(rank or index),
                "url": url.strip(),
                "publishedAt": published_at or "",
                "platform": "trendradar",
            }
        )

    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(
        json.dumps(
            {
                "generatedAt": datetime.now(timezone.utc).isoformat(),
                "items": items,
            },
            ensure_ascii=False,
            indent=2,
        )
        + "\n",
        encoding="utf-8",
    )


def main() -> None:
    parser = argparse.ArgumentParser(description="Export TrendRadar SQLite news into the Daily Briefing candidate feed")
    parser.add_argument("--db", required=True, type=Path)
    parser.add_argument("--out", required=True, type=Path)
    parser.add_argument("--limit", default=200, type=int)
    args = parser.parse_args()
    export_feed(args.db, args.out, max(1, min(args.limit, 500)))


if __name__ == "__main__":
    main()

