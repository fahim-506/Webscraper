## save all pages

from playwright.sync_api import sync_playwright
import csv

# Start Playwright
with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page()

    # Prepare a list to store all books
    all_books = []

    # Loop through all 50 pages
    for page_num in range(1, 51):  # 50 pages total
        url = f"https://books.toscrape.com/catalogue/page-{page_num}.html"
        print(f"Scraping page {page_num}...")
        page.goto(url)

        # Wait for books to load
        page.wait_for_selector(".product_pod")

        #Select all book elements
        books = page.locator(".product_pod")

        # Loop through all books on the page
        for i in range(books.count()):
            # Extract information from each book
            title = books.nth(i).locator("h3 a").get_attribute("title")
            price = books.nth(i).locator(".price_color").inner_text()
            stock = books.nth(i).locator(".availability").inner_text().strip()

            # Save book data
            all_books.append({
                "title": title,
                "price": price,
                "stock": stock
            })

    # Save all pages to CSV
    with open("all_books.csv", "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["title", "price", "stock"])
        writer.writeheader()
        writer.writerows(all_books)

    print("✅ Scraped", len(all_books), "books total!")
    browser.close()
