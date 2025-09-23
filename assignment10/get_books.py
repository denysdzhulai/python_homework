from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
import json
import os
import time

URL = "https://durhamcounty.bibliocommons.com/v2/search?query=learning%20spanish&searchType=smart"

RESULT_LI_SELECTORS = [
    "li.search-result",
    "li.result-item",
    "ul.search-results li",
    "ol.search-results li",
    "li[class*='result']",
    "li[class*='search']",
    "div.search-results li",
    "li[data-id]"
]

TITLE_SELECTORS = [
    "a.title",
    "h2 a",
    "h3 a",
    "a[itemprop='name']",
    ".result-title a",
    ".title a",
    ".card__title a",
    "a.link"
]

AUTHOR_SELECTORS = [
    ".contributors a",
    ".author a",
    ".contributor a",
    "a.author",
    "a[itemprop='author']",
    ".result-author a",
    ".authors a"
]

FORMAT_YEAR_SELECTORS = [
    ".format-year span",
    ".format-year",
    ".format .meta",
    ".result-format",
    ".format",
    ".media-type",
    ".edition"
]

WAIT_TIMEOUT = 3


def make_driver(headless=True):
    opts = webdriver.ChromeOptions()
    if headless:
        opts.add_argument("--headless=new")
        opts.add_argument("--disable-gpu")
    opts.add_argument("--no-sandbox")
    opts.add_argument("--disable-dev-shm-usage")
    driver = webdriver.Chrome(service=ChromeService(
        ChromeDriverManager().install()), options=opts)
    return driver


def try_first(element, selectors):
    """Return first text found by applying selectors (CSS) inside element."""
    for sel in selectors:
        try:
            el = element.find_element(By.CSS_SELECTOR, sel)
            txt = el.text.strip()
            if txt:
                return txt, sel
        except Exception:
            continue
    return "", None


def try_all_authors(element, selectors):
    """Return joined authors and the selector used."""
    for sel in selectors:
        try:
            els = element.find_elements(By.CSS_SELECTOR, sel)
            names = [e.text.strip() for e in els if e.text.strip()]
            if names:
                return ";".join(names), sel
        except Exception:
            continue
    return "", None


def find_result_items(driver):
    """Try multiple li selectors until we find matches. Return (items, selector)"""
    for sel in RESULT_LI_SELECTORS:
        try:
            elems = driver.find_elements(By.CSS_SELECTOR, sel)
            if elems and len(elems) > 0:
                return elems, sel
        except Exception:
            continue
    try:
        elems = driver.find_elements(By.CSS_SELECTOR, "main li")
        if elems and len(elems) > 0:
            return elems, "main li"
    except Exception:
        pass
    return [], None


def main():
    out_dir = os.path.dirname(__file__)
    csv_path = os.path.join(out_dir, "get_books.csv")
    json_path = os.path.join(out_dir, "get_books.json")

    driver = make_driver(headless=True)
    driver.get(URL)

    try:
        WebDriverWait(driver, WAIT_TIMEOUT).until(
            EC.presence_of_element_located(
                (By.CSS_SELECTOR, "main"))
        )
    except Exception:
        time.sleep(3)

    items, used_li = find_result_items(driver)
    print(f"Result item selector used: {used_li}; count found: {len(items)}")

    results = []
    max_items = min(len(items), 200)
    for idx in range(max_items):
        it = items[idx]
        title, title_sel = try_first(it, TITLE_SELECTORS)
        authors, author_sel = try_all_authors(it, AUTHOR_SELECTORS)
        fmt_year, fmt_sel = try_first(it, FORMAT_YEAR_SELECTORS)

        if not title:
            try:
                a = it.find_element(By.TAG_NAME, "a")
                title = a.text.strip()
                title_sel = "fallback:a"
            except Exception:
                pass

        results.append({
            "Title": title,
            "Author": authors,
            "Format-Year": fmt_year,
            "_found_title_sel": title_sel or "",
            "_found_author_sel": author_sel or "",
            "_found_format_sel": fmt_sel or "",
        })

    df = pd.DataFrame(results)
    df_csv = df.drop(
        columns=[c for c in df.columns if c.startswith("_found_")], errors='ignore')
    df_csv.to_csv(csv_path, index=False, encoding="utf-8")
    with open(json_path, "w", encoding="utf-8") as jf:
        json.dump(results, jf, indent=2, ensure_ascii=False)

    print(f"Wrote {len(df_csv)} rows to {csv_path} and {json_path}")
    print(df_csv.head(10).to_string(index=False))
    driver.quit()


if __name__ == "__main__":
    main()
