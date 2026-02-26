#!/usr/bin/env python3
"""DuckDuckGo search wrapper for Bond"""
import sys
import json
from ddgs import DDGS

def search(query, max_results=5):
    results = []
    for r in DDGS().text(query, max_results=max_results):
        results.append({
            'title': r.get('title', ''),
            'url': r.get('href', ''),
            'snippet': r.get('body', '')
        })
    return results

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: ddg-search.py 'query' [max_results]")
        sys.exit(1)
    
    query = sys.argv[1]
    max_results = int(sys.argv[2]) if len(sys.argv) > 2 else 5
    
    results = search(query, max_results)
    
    if '--json' in sys.argv:
        print(json.dumps(results, ensure_ascii=False, indent=2))
    else:
        for i, r in enumerate(results, 1):
            print(f"{i}. {r['title']}")
            print(f"   {r['url']}")
            print(f"   {r['snippet'][:150]}...")
            print()
