# Cryptocurrency Wallet

################################################################################
# For this Challenge, you will assume the perspective of a Fintech Finder
# customer in order to do the following:

# * Generate a new Ethereum account instance by using your mnemonic seed phrase

# * Fetch and display the account balance associated with your Ethereum account
# address.

# * Calculate the total value of an Ethereum transaction, including the gas
# estimate, that pays a Fintech Finder candidate for their work.

# * Digitally sign a transaction that pays a Fintech Finder candidate, and send
# this transaction to the Ganache blockchain.

# * Review the transaction hash code associated with the validated blockchain transaction.

# Once you receive the transaction’s hash code, you will navigate to the Transactions
# section of Ganache to review the blockchain transaction details. 


# Imports
import streamlit as st
from dataclasses import dataclass
from typing import Any, List
from web3 import Web3
from crypto_wallet import generate_account, get_balance, send_transaction
w3 = Web3(Web3.HTTPProvider('HTTP://127.0.0.1:7545'))

# Fintech Finder Candidate Information

# Database of Fintech Finder candidates including their name, digital address, rating and hourly cost per Ether.
candidate_database = {
    "Lane": ["Lane", "0xaC8eB8B2ed5C4a0fC41a84Ee4950F417f67029F0", "4.3", .20, "Images/lane.jpeg"],
    "Ash": ["Ash", "0x2422858F9C4480c2724A309D58Ffd7Ac8bF65396", "5.0", .33, "Images/ash.jpeg"],
    "Jo": ["Jo", "0x8fD00f170FDf3772C5ebdCD90bF257316c69BA45", "4.7", .19, "Images/jo.jpeg"],
    "Kendall": ["Kendall", "0x8fD00f170FDf3772C5ebdCD90bF257316c69BA45", "4.1", .16, "Images/kendall.jpeg"]
}

# A list of the FinTech Finder candidates first names
people = ["Lane", "Ash", "Jo", "Kendall"]


def get_people():
    """Display the database of Fintech Finders candidate information."""
    db_list = list(candidate_database.values())

    for number in range(len(people)):
        st.image(db_list[number][4], width=200)
        st.write("Name: ", db_list[number][0])
        st.write("Ethereum Account Address: ", db_list[number][1])
        st.write("FinTech Finder Rating: ", db_list[number][2])
        st.write("Hourly Rate per Ether: ", db_list[number][3], "eth")
        st.text(" \n")

def simplify_address(address):
    """Return the first four and last four of a wallet address"""

    length = len(address)
    if length > 8:
        return f'{address[0:4]}...{address[(length-4):length]}'
    else:
        return address

################################################################################
# Streamlit Code

status = st.container()
# Streamlit application headings
st.markdown("# Fintech Finder!")
st.markdown("## Hire A Fintech Professional!")
st.text(" \n")


################################################################################
# Streamlit Sidebar Code - Start

st.sidebar.markdown("## Client Account Info")
account = generate_account()

# Write the client's Ethereum account address to the sidebar
balance_container = st.sidebar.empty()
balance = get_balance(w3, account.address)
balance_container.write(f'**Balance (ETH)**:  {balance:,.8f}')
st.sidebar.write(f'**Address:** {simplify_address(account.address)}')

st.sidebar.markdown('---')
st.sidebar.markdown('## Candidate Selection')
# Create a select box to chose a FinTech Hire candidate
person = st.sidebar.selectbox('Select a Person', people)

# Create a input field to record the number of hours the candidate worked
hours = st.sidebar.number_input("Hours Worked")

# Identify the FinTech Hire candidate
candidate = candidate_database[person][0]

# Write the Fintech Finder candidate's name to the sidebar
st.sidebar.write(f'**Name**: {candidate}')

# Identify the FinTech Finder candidate's hourly rate
hourly_rate = candidate_database[person][3]

# Write the inTech Finder candidate's hourly rate to the sidebar
st.sidebar.write(f'**Hourly rate**: {hourly_rate}')

# Identify the FinTech Finder candidate's Ethereum Address
candidate_address = candidate_database[person][1]

# Write the inTech Finder candidate's Ethereum Address to the sidebar
st.sidebar.write(f'**Address:** {simplify_address(candidate_address)}')

wage  = hourly_rate * hours
st.sidebar.write(f'**Total wage (ETH)**: {wage:,.8f}')

if st.sidebar.button("Send Payment"):
    try:
        if wage <= balance:
            transaction_hash = send_transaction(w3, account, candidate_address, wage)
            status.success(f'Payment successful.\n\nTransaction ID: {transaction_hash.hex()}')
            balance = get_balance(w3, account.address)
            balance_container.write(f'**Balance (ETH)**:  {balance:,.8f}')
        else:
            raise Exception('Insufficient funds.')
    except Exception as e:
        status.error(e)


################################################################################

# Writes FinTech Finder candidates to the Streamlit page
get_people()