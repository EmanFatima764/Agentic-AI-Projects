from playwright.sync_api import sync_playwright


def scrape_website(url: str) -> dict:
    """
    Open a website and collect some basic information from it,
    such as its title, description, and visible text.
    """
    try:
        # Start Playwright so we can control a real browser with Python
        with sync_playwright() as p:

            # Open Chromium in the background so no browser window appears
            browser = p.chromium.launch(headless=True)

            # Create a new browser tab where we'll open the website
            page = browser.new_page()

            # Visit the given URL and wait until the page has mostly finished loading
            page.goto(url, wait_until="networkidle", timeout=30000)

            # Get the title shown in the browser tab
            title = page.title()

            # Look for the website's meta description
            meta_element = page.query_selector("meta[name='description']")

            # If a description exists, get its content; otherwise use a default message
            meta_description = (
                meta_element.get_attribute("content")
                if meta_element
                else "No meta description"
            )

            # Get all the visible text from the webpage
            raw_text = page.inner_text("body")

            # Remove unnecessary spaces and new lines
            # We keep only the first 1500 characters to avoid returning too much data
            clean_text = " ".join(raw_text.split())[:1500]

            # We're done with the browser, so close it
            browser.close()

            # Return everything we collected in an easy-to-use dictionary
            return {
                "success": True,
                "url": url,
                "title": title,
                "meta_description": meta_description,
                "content": clean_text
            }

    except Exception as e:
        # If something goes wrong, return the error instead of crashing the program
        return {
            "success": False,
            "error": str(e)
        }


if __name__ == "__main__":
    # Use a simple website to test whether our scraper is working
    test_url = "https://example.com"

    print(f"Scraping started: {test_url}")

    # Run the scraper and store the information it collects
    result = scrape_website(test_url)

    # Display the final result so we can check what was extracted
    print("\n--- Scraped Results ---")
    print(result)