#!/usr/bin/env python3
"""Upload markdown files to Notion as pages with blocks."""

import json
import re
import sys
import time
import requests

NOTION_KEY = open("/Users/bond/.config/notion/api_key").read().strip()
NOTION_VERSION = "2022-06-28"
PARENT_PAGE_ID = "2fc83182-3725-80e5-9ebc-f4c8df0eac09"

HEADERS = {
    "Authorization": f"Bearer {NOTION_KEY}",
    "Content-Type": "application/json",
    "Notion-Version": NOTION_VERSION,
}

MAX_TEXT_LEN = 2000
MAX_CHILDREN = 100


def split_text(text, max_len=MAX_TEXT_LEN):
    """Split text into chunks of max_len, trying to break at sentence/word boundaries."""
    if len(text) <= max_len:
        return [text]
    chunks = []
    while len(text) > max_len:
        # Try to break at last newline, then period, then space
        idx = text.rfind('\n', 0, max_len)
        if idx < max_len // 2:
            idx = text.rfind('. ', 0, max_len)
            if idx > 0:
                idx += 1  # include the period
        if idx < max_len // 4:
            idx = text.rfind(' ', 0, max_len)
        if idx <= 0:
            idx = max_len
        chunks.append(text[:idx].strip())
        text = text[idx:].strip()
    if text:
        chunks.append(text)
    return chunks


def rich_text(text, bold=False, italic=False, code=False, strikethrough=False):
    """Create a Notion rich_text element."""
    if not text:
        return []
    
    # Parse inline formatting
    elements = parse_inline_formatting(text)
    return elements


def parse_inline_formatting(text):
    """Parse markdown inline formatting into Notion rich_text elements."""
    elements = []
    # Pattern to match: **bold**, *italic*, `code`, ~~strikethrough~~, [text](url)
    # We'll do a simple sequential parse
    
    i = 0
    current = ""
    
    while i < len(text):
        # Check for bold **text**
        if text[i:i+2] == '**' and not text[i:i+3] == '***':
            if current:
                elements.append(make_text(current))
                current = ""
            end = text.find('**', i + 2)
            if end != -1:
                bold_text = text[i+2:end]
                elements.append(make_text(bold_text, bold=True))
                i = end + 2
                continue
        
        # Check for italic *text* (but not **)
        if text[i] == '*' and (i == 0 or text[i-1] != '*') and (i+1 < len(text) and text[i+1] != '*'):
            if current:
                elements.append(make_text(current))
                current = ""
            end = text.find('*', i + 1)
            if end != -1 and text[end-1:end+1] != '**':
                italic_text = text[i+1:end]
                elements.append(make_text(italic_text, italic=True))
                i = end + 1
                continue
        
        # Check for inline code `text`
        if text[i] == '`' and (i+1 < len(text) and text[i+1] != '`'):
            if current:
                elements.append(make_text(current))
                current = ""
            end = text.find('`', i + 1)
            if end != -1:
                code_text = text[i+1:end]
                elements.append(make_text(code_text, code=True))
                i = end + 1
                continue
        
        # Check for links [text](url)
        if text[i] == '[':
            match = re.match(r'\[([^\]]+)\]\(([^)]+)\)', text[i:])
            if match:
                if current:
                    elements.append(make_text(current))
                    current = ""
                link_text = match.group(1)
                link_url = match.group(2)
                elements.append(make_text(link_text, link=link_url))
                i += match.end()
                continue
        
        current += text[i]
        i += 1
    
    if current:
        elements.append(make_text(current))
    
    return elements if elements else [make_text("")]


def make_text(text, bold=False, italic=False, code=False, strikethrough=False, link=None):
    """Create a single Notion text element."""
    obj = {
        "type": "text",
        "text": {"content": text[:MAX_TEXT_LEN]},
        "annotations": {
            "bold": bold,
            "italic": italic,
            "strikethrough": strikethrough,
            "underline": False,
            "code": code,
            "color": "default",
        }
    }
    if link:
        obj["text"]["link"] = {"url": link}
    return obj


def make_paragraph(text):
    """Create paragraph block(s), splitting if needed."""
    blocks = []
    for chunk in split_text(text):
        blocks.append({
            "object": "block",
            "type": "paragraph",
            "paragraph": {
                "rich_text": parse_inline_formatting(chunk)
            }
        })
    return blocks


def make_heading2(text):
    """Create heading_2 block."""
    # Strip markdown heading prefix
    clean = re.sub(r'^#{1,3}\s*', '', text).strip()
    return {
        "object": "block",
        "type": "heading_2",
        "heading_2": {
            "rich_text": parse_inline_formatting(clean)
        }
    }


def make_heading3(text):
    """Create heading_3 block."""
    clean = re.sub(r'^#{1,4}\s*', '', text).strip()
    return {
        "object": "block",
        "type": "heading_3",
        "heading_3": {
            "rich_text": parse_inline_formatting(clean)
        }
    }


def make_bulleted_list_item(text):
    """Create bulleted_list_item block(s), splitting if needed."""
    blocks = []
    for chunk in split_text(text):
        blocks.append({
            "object": "block",
            "type": "bulleted_list_item",
            "bulleted_list_item": {
                "rich_text": parse_inline_formatting(chunk)
            }
        })
    return blocks


def make_numbered_list_item(text):
    """Create numbered_list_item block(s), splitting if needed."""
    blocks = []
    for chunk in split_text(text):
        blocks.append({
            "object": "block",
            "type": "numbered_list_item",
            "numbered_list_item": {
                "rich_text": parse_inline_formatting(chunk)
            }
        })
    return blocks


def make_code_block(code, language="plain text"):
    """Create code block(s), splitting if needed."""
    blocks = []
    for chunk in split_text(code):
        blocks.append({
            "object": "block",
            "type": "code",
            "code": {
                "rich_text": [make_text(chunk)],
                "language": language
            }
        })
    return blocks


def make_quote(text):
    """Create quote block(s)."""
    blocks = []
    for chunk in split_text(text):
        blocks.append({
            "object": "block",
            "type": "quote",
            "quote": {
                "rich_text": parse_inline_formatting(chunk)
            }
        })
    return blocks


def make_divider():
    return {
        "object": "block",
        "type": "divider",
        "divider": {}
    }


def make_table_block(rows):
    """Create a table block from parsed table rows."""
    if not rows:
        return []
    
    # Determine number of columns
    num_cols = max(len(row) for row in rows)
    
    # Build table rows
    table_rows = []
    for row in rows:
        cells = []
        for i in range(num_cols):
            cell_text = row[i].strip() if i < len(row) else ""
            cells.append(parse_inline_formatting(cell_text) if cell_text else [make_text("")])
        table_rows.append({
            "object": "block",
            "type": "table_row",
            "table_row": {"cells": cells}
        })
    
    table = {
        "object": "block",
        "type": "table",
        "table": {
            "table_width": num_cols,
            "has_column_header": True,
            "has_row_header": False,
            "children": table_rows
        }
    }
    return [table]


def parse_markdown_to_blocks(markdown_text):
    """Parse markdown text into Notion blocks."""
    blocks = []
    lines = markdown_text.split('\n')
    i = 0
    
    while i < len(lines):
        line = lines[i]
        stripped = line.strip()
        
        # Skip empty lines
        if not stripped:
            i += 1
            continue
        
        # Horizontal rule
        if stripped in ('---', '***', '___') and len(stripped) >= 3:
            blocks.append(make_divider())
            i += 1
            continue
        
        # Code block
        if stripped.startswith('```'):
            lang = stripped[3:].strip() or "plain text"
            code_lines = []
            i += 1
            while i < len(lines) and not lines[i].strip().startswith('```'):
                code_lines.append(lines[i])
                i += 1
            i += 1  # skip closing ```
            code_text = '\n'.join(code_lines)
            blocks.extend(make_code_block(code_text, lang))
            continue
        
        # Table detection
        if '|' in stripped and i + 1 < len(lines) and re.match(r'^\s*\|[\s\-:|]+\|\s*$', lines[i+1].strip()):
            table_rows = []
            # Parse header
            row = [cell.strip() for cell in stripped.split('|')[1:-1]]
            table_rows.append(row)
            i += 1  # move to separator
            i += 1  # skip separator
            # Parse data rows
            while i < len(lines) and '|' in lines[i] and lines[i].strip().startswith('|'):
                row = [cell.strip() for cell in lines[i].strip().split('|')[1:-1]]
                table_rows.append(row)
                i += 1
            blocks.extend(make_table_block(table_rows))
            continue
        
        # Headings
        if stripped.startswith('#### '):
            blocks.append(make_heading3(stripped))
            i += 1
            continue
        if stripped.startswith('### '):
            blocks.append(make_heading3(stripped))
            i += 1
            continue
        if stripped.startswith('## '):
            blocks.append(make_heading2(stripped))
            i += 1
            continue
        if stripped.startswith('# '):
            blocks.append(make_heading2(stripped))
            i += 1
            continue
        
        # Blockquote
        if stripped.startswith('> '):
            quote_lines = []
            while i < len(lines) and lines[i].strip().startswith('>'):
                quote_lines.append(lines[i].strip().lstrip('>').strip())
                i += 1
            quote_text = '\n'.join(quote_lines)
            blocks.extend(make_quote(quote_text))
            continue
        
        # Numbered list
        if re.match(r'^\d+[\.\)]\s', stripped):
            text = re.sub(r'^\d+[\.\)]\s', '', stripped)
            blocks.extend(make_numbered_list_item(text))
            i += 1
            continue
        
        # Bulleted list
        if stripped.startswith('- ') or stripped.startswith('* ') or stripped.startswith('• '):
            text = stripped[2:]
            blocks.extend(make_bulleted_list_item(text))
            i += 1
            continue
        
        # Regular paragraph - collect consecutive non-special lines
        para_lines = [stripped]
        i += 1
        while i < len(lines):
            next_line = lines[i].strip()
            if not next_line:
                break
            if next_line.startswith('#') or next_line.startswith('```') or \
               next_line.startswith('- ') or next_line.startswith('* ') or \
               next_line.startswith('> ') or next_line in ('---', '***', '___') or \
               re.match(r'^\d+[\.\)]\s', next_line) or \
               ('|' in next_line and i + 1 < len(lines) and '|' in lines[i+1]):
                break
            para_lines.append(next_line)
            i += 1
        
        para_text = ' '.join(para_lines)
        blocks.extend(make_paragraph(para_text))
    
    return blocks


def create_page(title, parent_id):
    """Create a new Notion page and return its ID and URL."""
    data = {
        "parent": {"page_id": parent_id},
        "properties": {
            "title": {
                "title": [{"text": {"content": title}}]
            }
        }
    }
    
    resp = requests.post(
        "https://api.notion.com/v1/pages",
        headers=HEADERS,
        json=data
    )
    resp.raise_for_status()
    result = resp.json()
    return result["id"], result["url"]


def append_blocks(page_id, blocks):
    """Append blocks to a page, batching in groups of 100."""
    total = len(blocks)
    for start in range(0, total, MAX_CHILDREN):
        batch = blocks[start:start + MAX_CHILDREN]
        data = {
            "children": batch
        }
        resp = requests.patch(
            f"https://api.notion.com/v1/blocks/{page_id}/children",
            headers=HEADERS,
            json=data
        )
        if resp.status_code == 429:
            retry_after = int(resp.headers.get("Retry-After", 2))
            print(f"  Rate limited, waiting {retry_after}s...")
            time.sleep(retry_after)
            resp = requests.patch(
                f"https://api.notion.com/v1/blocks/{page_id}/children",
                headers=HEADERS,
                json=data
            )
        if resp.status_code != 200:
            print(f"  ERROR ({resp.status_code}): {resp.text[:500]}")
            # Try to identify problematic block
            if len(batch) > 1:
                print(f"  Trying blocks one by one for this batch ({start}-{start+len(batch)})...")
                for idx, block in enumerate(batch):
                    single_resp = requests.patch(
                        f"https://api.notion.com/v1/blocks/{page_id}/children",
                        headers=HEADERS,
                        json={"children": [block]}
                    )
                    if single_resp.status_code == 429:
                        time.sleep(2)
                        single_resp = requests.patch(
                            f"https://api.notion.com/v1/blocks/{page_id}/children",
                            headers=HEADERS,
                            json={"children": [block]}
                        )
                    if single_resp.status_code != 200:
                        print(f"    Block {start+idx} failed: {block.get('type')} - {single_resp.text[:200]}")
                    else:
                        pass  # OK
            else:
                resp.raise_for_status()
        else:
            print(f"  Appended blocks {start+1}-{start+len(batch)} of {total}")
        
        # Small delay between batches
        if start + MAX_CHILDREN < total:
            time.sleep(0.5)


def process_file(filepath, title):
    """Read a markdown file, create a Notion page, and upload content."""
    print(f"\n{'='*60}")
    print(f"Processing: {title}")
    print(f"File: {filepath}")
    
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    print(f"  Content length: {len(content)} chars")
    
    # Parse markdown to blocks
    blocks = parse_markdown_to_blocks(content)
    print(f"  Parsed into {len(blocks)} blocks")
    
    # Create page
    page_id, page_url = create_page(title, PARENT_PAGE_ID)
    print(f"  Created page: {page_url}")
    
    # Append blocks
    if blocks:
        append_blocks(page_id, blocks)
    
    print(f"  ✅ Done: {page_url}")
    return page_url


def main():
    files = [
        ("/Users/bond/.openclaw/workspace/drafts/course-agents-part1.md",
         "🤖 50 агентов — Часть 1 (1-25)"),
        ("/Users/bond/.openclaw/workspace/drafts/course-agents-part2.md",
         "🤖 50 агентов — Часть 2 (26-50)"),
        ("/Users/bond/.openclaw/workspace/drafts/course-pricing-analysis.md",
         "💰 Конкурентный анализ + Ценовая модель"),
    ]
    
    urls = []
    for filepath, title in files:
        url = process_file(filepath, title)
        urls.append((title, url))
        time.sleep(1)  # Pause between pages
    
    print(f"\n{'='*60}")
    print("🎉 All pages created successfully!")
    print(f"{'='*60}")
    for title, url in urls:
        print(f"  {title}")
        print(f"  → {url}")
    print()


if __name__ == "__main__":
    main()
