import streamlit as st
import pandas as pd

CATEGORY_RULES = {
    "Groceries": ["Tesco", "Waitrose", "Sainsbury", "Hampstead Butcher", "M&S West Hampstead", "Inkey List", "Ocado", "Smol"],
    "Dining Out and take away": ["Chipotle", "Five Guys", "Protein Pizza", "Deliveroo", "Greyhound Cafe", "LS Midtown and Rye"],
    "Lunches": ["Nusa Kitchen", "Coco Di Mama", "Dukan 41", "Wasabi", "Birley", "WH Smith", "Pret A Manger"],
    "Coffee/Snacks": ["Gails", "Caffe Nero", "Lolas", "The Sanctuary"],
    "Public Transit": ["TFL Travel Charge"],
    "Taxi": ["Uber", "Taxi"],
    "Medical Bills/Medicines": ["Boots", "Plowman and Partners", "Armco", "Aqua Pharmacy", "Nourishing Vitality"],
    "Clothing": ["Timpson", "Polarn O Pyret", "Pairs", "Marks & Spencer", "John Lewis", "Decathlon", "Cheeky", "H&M", "VF UK IB", "Adidas", "Asics", "Start-rite"],
    "Subscriptions": ["Zoom.com", "Apple.com", "Instagram", "Adobe", "OpenAI"],
    "Gifts/Donations": ["M&S Richmond", "Proto"],
    "Travel/Vacations": ["British Airways", "Airbnb", "Heathrow Express", "Gatwick Express"],
    "Dry Cleaning": ["Madam George"]
}

def categorize_transaction(description: str) -> str:
    desc = str(description).lower()
    for category, keywords in CATEGORY_RULES.items():
        for keyword in keywords:
            if keyword.lower() in desc:
                return category
    return "Uncategorized"

st.title("💳 Bank Statement Analyzer")

uploaded_file = st.file_uploader("Upload your bank statement (CSV)", type=["csv"])

if uploaded_file:
    df = pd.read_csv(uploaded_file)

    if "Description" not in df.columns or "Amount" not in df.columns:
        st.error("Your file must have 'Description' and 'Amount' columns")
    else:
        df["Category"] = df["Description"].apply(categorize_transaction)

        st.subheader("Transactions")
        st.dataframe(df)

        uncategorized = df[df["Category"] == "Uncategorized"]
        if not uncategorized.empty:
            st.warning("Uncategorized transactions – assign manually below:")
            for idx, row in uncategorized.iterrows():
                choice = st.selectbox(
                    f"{row['Description']} ({row['Amount']})",
                    ["Uncategorized"] + list(CATEGORY_RULES.keys()),
                    key=f"uncat_{idx}"
                )
                if choice != "Uncategorized":
                    df.at[idx, "Category"] = choice

        st.subheader("Summary")
        summary = df.groupby("Category")["Amount"].sum().reset_index()
        pivot = summary.set_index("Category").T
        pivot.loc["Total"] = pivot.sum(axis=0)
        st.dataframe(pivot)
