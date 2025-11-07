## save 20 books page


from playwright.sync_api import sync_playwright
import csv
import pandas as pd

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)  # change to False to see the browser /slow_mo=300
    page = browser.new_page()
    page.goto("https://books.toscrape.com/")

    # Wait until book items are loaded
    page.wait_for_selector(".product_pod")

    # Select all books on the page
    books = page.locator(".product_pod")

    data = []

    for i in range(books.count()):
        # Extract book information
        title = books.nth(i).locator("h3 a").get_attribute("title")
        price = books.nth(i).locator(".price_color").inner_text()
        stock = books.nth(i).locator(".availability").inner_text().strip()

        # Store each book in a list
        data.append({
            "title": title,
            "price": price,
            "stock": stock
        })

    # Save to CSV
    with open("books.csv", "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["title", "price", "stock"])
        writer.writeheader()
        writer.writerows(data)

    print("✅ Saved", len(data), "books to books.csv")

    browser.close()

# Print first 5 books using for loop 
print("\nFirst 5 books:")
for book in data[:5]:
    print(book)


# Display last 5 book details using pandas
df = pd.read_csv('books.csv')
print(df.tail())

