"""Downloading raw project gutenberg texts and record where they came from."""

import csv
import hashlib
import time
import urllib.error, urllib.request
from datetime import date
from pathlib import Path

# adding candidate books after verifying Title and authors
# took many indian books from https://www.gutenberg.org/ebooks/subject/3686?sort_order=title
# 5314 Grimms is original large set and 2591 is smaller one. 
#need to check Indian stories

BOOKS= {
    5314: "Hunt_Grimms"
    2591: "Grimms_small",
    36309: "IndWHDRouse",
    62514: "IndJataka_ECBabbitt"
    31209: "Ind_Stokes"
}

ROOT = Path(__file__).resolve().parents[1]
RAW_DIR = ROOT/'data'/'raw'
MANIFEST = ROOT/'data'/'manifest.csv'
HEADER_FIELDS = ("Title", "Author", "Translator", "Editor", "Release date", "Language")

def url_for(book_id: int) -> str:
    return f"https://www.gutenberg.org/cache/epub/{book_id}/pg{book_id}.txt

def download(book_id: int) -> bytes:
    request = urllib.request.Request(
        url_for(book_id),
        headers={"User-Agent": "folktale-nlp-course-project (for student research)"},   #informing agents about our work for scraping"
    )
    with urllib.request.urlopen(request,timeout=30) as response:     #gentle request at 30 seconds"
        return response.read()

def parse_header (text: str) -> dict:
    """pull the metadat lines fromt he top of each title on gutenberg website"""
    found = {}
    for line in text.splitlines()[:80]:
        for field in HEADER_FIELDS:
            if line.startswith(field + ":"):
                found[field] = line.split(":", 1)[1].strip()
    return found

#### build main function for this

