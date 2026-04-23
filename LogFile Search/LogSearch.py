#!/usr/bin/env python3

import argparse
import os
import sys
import re
import json
import ipaddress
import xml.etree.ElementTree as ET
from configparser import ConfigParser

from docx import Document
from fuzzywuzzy import fuzz
import openpyxl

# ============================================================
# Terminal color support
# ============================================================

def supports_color():
    return sys.stdout.isatty()

class Colors:
    GREEN = "\033[92m"
    YELLOW = "\033[93m"
    RED = "\033[91m"
    CYAN = "\033[96m"
    RESET = "\033[0m"

# ============================================================
# Regex helpers
# ============================================================

IP_REGEX = re.compile(r"\b(?:\d{1,3}\.){1,3}\d{1,3}\b")

# ============================================================
# Input normalization helpers
# ============================================================

def clean_arg(val: str) -> str:
    return val.strip().strip('"').strip("'")

def split_and_clean(val: str):
    return [clean_arg(v) for v in val.split(",") if clean_arg(v)]

# ============================================================
# Core search engine
# ============================================================

def search_files(directory, search_terms, use_prefix, threshold=75):
    results = {term: {"text": set(), "json": set(), "xml": set()} for term in search_terms}
    text_exts = ('.txt', '.log', '.csv')

    for root, _, files in os.walk(directory):
        for name in files:
            path = os.path.join(root, name)

            try:
                if name.endswith('.xlsx'):
                    process_excel(path, search_terms, results, use_prefix, threshold)
                elif name.endswith('.docx'):
                    process_docx(path, search_terms, results, use_prefix, threshold)
                elif name.endswith('.ini'):
                    process_ini(path, search_terms, results, use_prefix, threshold)
                elif name.endswith('.json'):
                    process_json(path, search_terms, results, use_prefix, threshold)
                elif name.endswith('.xml'):
                    process_xml(path, search_terms, results, use_prefix, threshold)
                elif name.endswith(text_exts):
                    process_text(path, search_terms, results, use_prefix, threshold)
            except Exception:
                continue

    return results

# ============================================================
# File processors
# ============================================================

def process_text(path, terms, results, use_prefix, threshold):
    with open(path, "r", encoding="utf-8", errors="ignore") as f:
        for line in f:
            scan_content(line, path, terms, results, use_prefix, threshold)

def process_excel(path, terms, results, use_prefix, threshold):
    wb = openpyxl.load_workbook(path, read_only=True, data_only=True)
    for ws in wb.worksheets:
        for row in ws.iter_rows(values_only=True):
            for cell in row:
                if cell:
                    scan_content(str(cell), path, terms, results, use_prefix, threshold)

def process_docx(path, terms, results, use_prefix, threshold):
    doc = Document(path)
    for p in doc.paragraphs:
        scan_content(p.text, path, terms, results, use_prefix, threshold)

def process_ini(path, terms, results, use_prefix, threshold):
    cfg = ConfigParser()
    cfg.read(path)
    for s in cfg.sections():
        for k, v in cfg.items(s):
            scan_content(k, path, terms, results, use_prefix, threshold)
            scan_content(v, path, terms, results, use_prefix, threshold)

def process_json(path, terms, results, use_prefix, threshold):
    with open(path, encoding="utf-8", errors="ignore") as f:
        scan_content(json.dumps(json.load(f)), path, terms, results, use_prefix, threshold, "json")

def process_xml(path, terms, results, use_prefix, threshold):
    tree = ET.parse(path)
    scan_content(
        ET.tostring(tree.getroot(), encoding="unicode"),
        path, terms, results, use_prefix, threshold, "xml"
    )

# ============================================================
# Matching logic
# ============================================================

def scan_content(content, path, terms, results, use_prefix, threshold, filetype="text"):
    content_l = content.lower()

    for term in terms:
        if term.startswith("IP-"):
            val = term[3:]
            if (
                match_ip_or_cidr(val, content) or
                (use_prefix and match_ip_prefix(val, content))
            ):
                results[term][filetype].add(path)

        elif term.startswith("MAC-"):
            val = term[4:]
            if (
                match_mac(val, content) or
                (use_prefix and match_mac_prefix(val, content))
            ):
                results[term][filetype].add(path)

        else:
            t = term.lower()
            if t in content_l or fuzz.partial_ratio(t, content_l) >= threshold:
                results[term][filetype].add(path)

# ---------------- IP FUNCTIONS ----------------

def match_ip_or_cidr(search_term, content):
    try:
        if "/" in search_term:
            net = ipaddress.ip_network(search_term, strict=False)
            is_cidr = True
        else:
            ip = ipaddress.ip_address(search_term)
            is_cidr = False
    except ValueError:
        return False

    for cand in IP_REGEX.findall(content):
        try:
            found = ipaddress.ip_address(cand)
            if is_cidr and found in net:
                return True
            if not is_cidr and found == ip:
                return True
        except ValueError:
            continue

    return False

def match_ip_prefix(prefix, content):
    return any(cand.startswith(prefix) for cand in IP_REGEX.findall(content))

# ---------------- MAC FUNCTIONS ----------------

def match_mac(term, content):
    t = re.sub(r"[^0-9A-Fa-f]", "", term).lower()
    c = re.sub(r"[^0-9A-Fa-f]", "", content).lower()
    return t in c

def match_mac_prefix(prefix, content):
    p = re.sub(r"[^0-9A-Fa-f]", "", prefix).lower()
    c = re.sub(r"[^0-9A-Fa-f]", "", content).lower()
    return c.startswith(p)

# ============================================================
# Main CLI
# ============================================================

def main():
    parser = argparse.ArgumentParser(
        formatter_class=argparse.RawTextHelpFormatter,
        description=(
            "Multi‑File Search Utility (DFIR‑Ready)\n\n"
            "DEFAULT MODE (Safe):\n"
            "  • IP exact + CIDR matching\n"
            "  • Full MAC matching\n\n"
            "PREFIX MODE (Opt‑In):\n"
            "  • Enables partial prefix matching for IP/MAC\n"
            "  • Use with care during IR investigations\n\n"
            "Examples:\n"
            "  -I 192.168.1.0/24\n"
            "  -P -I 192.168.1.\n"
            "  -P -M 00:11:22\n"
        )
    )

    parser.add_argument("-D", "--directory", required=True)
    parser.add_argument("-K", "--keywords")
    parser.add_argument("-I", "--ip", dest="ip_addresses")
    parser.add_argument("-M", "--mac", dest="mac_addresses")
    parser.add_argument(
        "-P", "--prefix",
        action="store_true",
        help="Enable prefix matching for IP and MAC addresses."
    )
    parser.add_argument("--case", dest="case_id")
    parser.add_argument("--quiet", action="store_true")

    args = parser.parse_args()

    keywords = split_and_clean(args.keywords) if args.keywords else []
    ips = split_and_clean(args.ip_addresses) if args.ip_addresses else []
    macs = split_and_clean(args.mac_addresses) if args.mac_addresses else []

    search_terms = (
        keywords +
        [f"IP-{i}" for i in ips] +
        [f"MAC-{m}" for m in macs]
    )

    if not search_terms:
        parser.error("No search terms supplied.")

    results = search_files(
        os.path.abspath(args.directory),
        search_terms,
        args.prefix
    )

    color = supports_color() and not args.quiet
    def c(t, col): return f"{col}{t}{Colors.RESET}" if color else t

    for term, buckets in results.items():
        hit = False
        for ft, paths in buckets.items():
            for p in paths:
                hit = True
                print(p if args.quiet else c("[FOUND]", Colors.GREEN), term, "->", p)
        if not hit and not args.quiet:
            print(c("[NONE ]", Colors.YELLOW), term)

if __name__ == "__main__":
    main()
