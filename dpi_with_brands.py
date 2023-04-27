import requests
import streamlit as st
import datetime
import urllib.parse

# Function to check if keywords are found in content
def check_keywords_in_content(content, keywords):
    for keyword in keywords:
        if keyword.lower() in content.lower():
            return True
    return False

# Streamlit web app
def main():
    st.set_page_config(page_title="DPI-Brands", page_icon=":rocket:")

    st.title("Market Research Web App - Google Search URL Generator")
    st.write("Company Brand Names can be inputted as comma seperated values. These- are optional. ")

    # Input parameters
    company_name = st.text_input("Enter Company Name")
    search_term = st.text_input("Enter Search Term")
    keywords = st.text_area("Enter Associated Keywords (comma separated)")
    keywords = [kw.strip() for kw in keywords.split(',') if kw.strip()]
    website_name = st.text_input("Search in a specific website Name (Optional)")
    brands = st.text_area("Enter Brand Names (comma separated) - Optional")
    brands = [brand.strip() for brand in brands.split(',') if brand.strip()]

    # Get current year
    current_year = datetime.datetime.now().year

    # Get current date
    current_date = datetime.datetime.now().date()

    # Calculate past year
    past_year = current_year - 1

    # Perform Google search
    if st.button("Generate Search URL"):
        urls = []
        if not brands:
            search_query = f'{search_term} {" ".join(keywords)} after:{past_year}-01-01 before:{current_date}'
            if company_name:
                search_query = f'intext:"{company_name}" ' + search_query
            if website_name:
                search_query += f" site:{website_name}"
            search_query = search_query.replace(" ", "%20")
            url = f"https://www.google.com/search?q={search_query}"
            urls.append(url)
            st.markdown(f"### Generated Google Search URL: [{url}]({url})")
        else:
            for brand in brands:
                # Construct search query with time frame
                search_query = f'{search_term} {" ".join(keywords)} after:{past_year}-01-01 before:{current_date}'
                if company_name:
                    search_query = f'intext:"{company_name}" ' + search_query
                if website_name:
                    search_query += f" site:{website_name}"
                search_query = search_query.replace(" ", "%20")
                if brand:
                    search_query = f'{search_query} "{brand}"'
                url = f"https://www.google.com/search?q={search_query}"
                urls.append(url)

            # Display URLs in table
            st.subheader("Generated Google Search URLs for Brands:")
            table_data = []
            for i, url in enumerate(urls):
                brand_name = brands[i] if i < len(brands) else ""
                table_data.append((brand_name, url))
            st.dataframe(table_data, columns=["Brand Name", "Google Search URL"], 
                     value=[f"[{url}]({url})" for _, url in table_data])

            # Get content for each URL
            for url in urls:
                st.markdown(f"#### Generated Google Search URL: [{url}]({url})")
                response = requests.get(url)
                content = response.text

                # Check if content contains keywords
                if check_keywords_in_content(content, keywords):
                    st.subheader("Captured Content:")
                    st.code(content, language='html')
                else:
                    st.write("No content captured for the given keywords")

if __name__ == '__main__':
    main()
