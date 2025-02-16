from playwright.sync_api import sync_playwright
import time


def search_trademarks(query, max_pages=5):
    with sync_playwright() as p:
        # Launch browser
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        # Open Rospatent trademark search website
        page.goto("https://searchplatform.rospatent.gov.ru/trademarks")

        # Wait for the search input to be visible
        page.wait_for_selector("input.search-input_5uoaK")

        # Enter the search query
        page.fill("input.search-input_5uoaK", query)

        # Click the search button
        time.sleep(1)
        #page.click("button.search-button_HBeQy")
        page.click("button:has-text('Поиск')")

        # Wait until the element is visible
        page.wait_for_selector("div.total_m4J5y", state="visible")

        # Extract the number from the span inside the div
        total_records = page.locator("div.total_m4J5y span").text_content()

        # Convert to integer (if needed)
        total_records = int(total_records.strip())

        print(f"Total records: {total_records}")

        # Wait for search results to load
        page.wait_for_selector(".table_wCH66")

        results = []
        current_page = 1

        while current_page <= max_pages:
            print(f"Scraping page {current_page}...")

            # Extract table rows
            rows = page.locator(".table_wCH66 tbody tr").all()

            for row in rows:
                columns = row.locator("td").all_inner_texts()
                if columns:

                    # Step 1: Hover over the SVG
                    svg_element = row.locator(
                        "svg"
                    )  # Adjust if there's a specific class
                    if svg_element.is_visible():
                        svg_element.hover()
                        time.sleep(1)  # Ensure tooltip appears

                    # Step 2: Click "Открыть карточку"
                    open_card_button = row.locator(
                        "div:has-text('Открыть карточку')"
                    )

                    print(f"open_card_button.count() = {open_card_button.count()}")

                    if open_card_button.is_visible():
                        open_card_button.click()
                        time.sleep(2)  # Allow popup to load

                        # Step 3: Extract "Классы МКТУ и перечень товаров и/или услуг"
                        mktu_element = page.locator(
                            "div.column_YNGYX:has-text('Классы МКТУ')"
                        )

                        print(f"mktu_element.count() = {mktu_element.count()}")

                        if mktu_element.count() > 0:
                            mktu_text = mktu_element.locator(
                                ".value_S2u3a"
                            ).inner_text()
                        else:
                            mktu_text = "Not found"

                        # Step 4: Close popup using <div class="close_e0SDh">✖</div>
                        close_button = page.locator(".close_e0SDh")
                        if close_button.is_visible():
                            close_button.click()
                            time.sleep(1)  # Ensure popup closes

                    else:
                        mktu_text = "Not found"

                    results.append(
                        {
                            "№": columns[0],
                            "Заявка": columns[1],
                            "Регистрация": columns[2],
                            "Тип знака": columns[3],
                            "Дата подачи": columns[4],
                            "Дата регистрации": columns[5],
                            "Заявитель / правообладатель": columns[6],
                            "Классы МКТУ": mktu_text,
                        }
                    )

                    print(results[-1])
                break

            # Try to go to the next page
            next_page_button = page.locator(".pagination_SIODz >> text='>'").nth(0)

            if False:  # next_page_button.is_enabled():
                next_page_button.click()
                time.sleep(2)  # Allow time for page load
                current_page += 1
            else:
                break  # No more pages

        # Print results
        # for result in results:
        #     print(result)

        # Close browser
        browser.close()


# Example usage: scrape up to 5 pages of search results for "Apple"
search_trademarks("Apple", max_pages=1)
