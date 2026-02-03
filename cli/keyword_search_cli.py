#!/usr/bin/env python3

import argparse
import json
import string
from pathlib import Path


def main() -> None:
    parser = argparse.ArgumentParser(description="Keyword Search CLI")
    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    search_parser = subparsers.add_parser("search", help="Search movies using BM25")
    search_parser.add_argument("query", type=str, help="Search query")

    args = parser.parse_args()

    match args.command:
        case "search":
            print(f"Searching for: {args.query}")
            movies_json = Path(__file__).resolve().parent.parent / "data" / "movies.json"
            with movies_json.open() as f:
                data = json.load(f)
            
            keyword_matches = []
            remove_punctuation = str.maketrans("", "", string.punctuation)
            search_tokens = args.query.lower().translate(remove_punctuation).split()
            for info in data.get("movies", ""):
                processed_title = info.get("title", "").lower().translate(remove_punctuation).split()
                if title_matches(search_tokens, processed_title):
                    keyword_matches.append({"id": info["id"], "title": info["title"]})

            sorted_keyword_matches = sorted(keyword_matches, key=lambda x: x["id"])
            for i, info in enumerate(sorted_keyword_matches[:5]):
                print(f"{i + 1}. {info['title']}")
            
        case _:
            parser.print_help()

def title_matches(search_tokens, processed_title):
    return any(search_token in title_word
               for search_token in search_tokens
               for title_word in processed_title)


if __name__ == "__main__":
    main()
