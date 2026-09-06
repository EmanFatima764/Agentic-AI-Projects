import streamlit as st
import pandas as pd
import os
os.system("playwright install chromium")
os.system("playwright install-deps")

from scraper import scrape_website
from ai_engine import process_lead_with_ai


# Set up the basic Streamlit page settings
st.set_page_config(
    page_title="SmartLead AI",
    page_icon="⚡",
    layout="wide"
)


# Show the app title and briefly explain what the tool does
st.title("⚡ SmartLead AI - Lead Intelligence System")
st.write(
    "Enter a business website URL and the system will scan the website, "
    "analyze the information with AI, and create a personalized cold email pitch."
)

st.divider()


# Give the user a place to enter the business website URL
target_url = st.text_input(
    "Enter the website URL:",
    placeholder="https://example.com"
)


# Start the lead analysis when the user clicks this button
if st.button("Start Analysis (Process Lead)", type="primary"):

    # Make sure the user has entered a URL before starting the process
    if not target_url:
        st.warning("Please enter a valid URL first!")

    else:
        # Step 1: Visit the website and collect useful information
        with st.spinner("1/2: Scraping the website..."):
            scraped_data = scrape_website(target_url)

        # Stop here if the website could not be scraped successfully
        if not scraped_data.get("success"):
            st.error(
                f"An error occurred while scraping: "
                f"{scraped_data.get('error')}"
            )

        else:
            st.success("Website data was successfully collected!")

            # Step 2: Send the scraped information to the AI
            # The AI will analyze the lead and create a personalized pitch
            with st.spinner(
                "2/2: AI is analyzing the lead and creating a personalized email pitch..."
            ):
                ai_result = process_lead_with_ai(scraped_data)

            # Display the results only if the AI processing was successful
            if ai_result.get("success"):
                st.divider()
                st.subheader("🎯 Results")

                # Split the results area into two columns
                col1, col2 = st.columns([1, 2])

                with col1:
                    # Show the basic information collected from the website
                    st.markdown("**📌 Website Information:**")
                    st.write(f"**Title:** {scraped_data['title']}")
                    st.write(
                        f"**Meta Description:** "
                        f"{scraped_data['meta_description']}"
                    )

                with col2:
                    # Show the AI's analysis and personalized email pitch
                    st.markdown("**🤖 AI Analysis & Email Pitch:**")
                    st.info(ai_result["ai_analysis"])

                st.divider()

                # Put the collected information into a DataFrame
                # so the user can easily save the results as a CSV file
                df = pd.DataFrame([{
                    "URL": target_url,
                    "Title": scraped_data["title"],
                    "Meta Description": scraped_data["meta_description"],
                    "AI Analysis & Pitch": ai_result["ai_analysis"]
                }])

                # Convert the DataFrame into CSV format
                # index=False prevents pandas from adding an extra index column
                csv_data = df.to_csv(index=False).encode("utf-8")

                # Give the user a button to download the lead information
                st.download_button(
                    label="📥 Download Results as CSV",
                    data=csv_data,
                    file_name="smartlead_result.csv",
                    mime="text/csv"
                )

            else:
                # Show the AI error if the analysis could not be completed
                st.error(
                    f"An error occurred during AI processing: "
                    f"{ai_result.get('error')}"
                )
