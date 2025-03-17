import streamlit as st
from src.components.card import shop_card
from src.components.chatbox import chatbox
# from src.components.testcard import shopy_card


def section_header(headerText: str, captionText: str):
    with st.container():
        st.header(headerText, divider=True)
        st.caption(captionText)

def section_search():
    with st.form(key="search_form"):
        col1, col2 = st.columns(2)
        
        with col1:
            name = st.text_input("Name")
            time_input = st.time_input("Time")
            location = st.text_input("Location")
        
        with col2:
            price = st.slider("Price", min_value=0.0, max_value=1000.0, 
                            value=0.0, step=0.01, format="%.2f")
            verify = st.radio("Verify", options=["Yes", "No"])
            age = st.number_input("Age", min_value=0)
        
        submitted = st.form_submit_button("Search")
        



def section_search_results():
   col1, col2 = st.columns([4, 2])
   shops = [
      {
         "image_url": "https://img2.chinadaily.com.cn/images/202410/15/670dca8fa310f1268d82d003.jpeg",
         "supplier": "Fresh Mart",
         "verified": "✓ Verified",
         "price": "$20/hr",
         "time": "2-5 days",
         "age": "5 years",
         "location": "Downtown"
      },
      {
         "image_url": "https://img2.chinadaily.com.cn/images/202410/15/670dca8fa310f1268d82d003.jpeg",
         "supplier": "Tech Haven",
         "verified": "✓ Verified",
         "price": "$35/hr",
         "time": "1-3 days",
         "age": "2 years",
         "location": "Midtown"
      },
      {
         "image_url": "https://img2.chinadaily.com.cn/images/202410/15/670dca8fa310f1268d82d003.jpeg",
         "supplier": "Fashion Plus",
         "verified": "ⓘ Pending Verification",
         "price": "$28/hr",
         "time": "3-7 days",
         "age": "4 years",
         "location": "Suburbs"
      },
      {
         "image_url": "https://img2.chinadaily.com.cn/images/202410/15/670dca8fa310f1268d82d003.jpeg",
         "supplier": "Fashion Plus",
         "verified": "ⓘ Pending Verification",
         "price": "$28/hr",
         "time": "3-7 days",
         "age": "4 years",
         "location": "Suburbs"
      },
      {
         "image_url": "https://img2.chinadaily.com.cn/images/202410/15/670dca8fa310f1268d82d003.jpeg",
         "supplier": "Fashion Plus",
         "verified": "ⓘ Pending Verification",
         "price": "$28/hr",
         "time": "3-7 days",
         "age": "4 years",
         "location": "Suburbs"
      },
      {
         "image_url": "https://img2.chinadaily.com.cn/images/202410/15/670dca8fa310f1268d82d003.jpeg",
         "supplier": "Fashion Plus",
         "verified": "ⓘ Pending Verification",
         "price": "$28/hr",
         "time": "3-7 days",
         "age": "4 years",
         "location": "Suburbs"
      },
      {
         "image_url": "https://img2.chinadaily.com.cn/images/202410/15/670dca8fa310f1268d82d003.jpeg",
         "supplier": "Fashion Plus",
         "verified": "ⓘ Pending Verification",
         "price": "$28/hr",
         "time": "3-7 days",
         "age": "4 years",
         "location": "Suburbs"
      },
      {
         "image_url": "https://img2.chinadaily.com.cn/images/202410/15/670dca8fa310f1268d82d003.jpeg",
         "supplier": "Fashion Plus",
         "verified": "ⓘ Pending Verification",
         "price": "$28/hr",
         "time": "3-7 days",
         "age": "4 years",
         "location": "Suburbs"
      }
   ]

   with col1:
      st.header("Available Shops")
      # with st.container():
      #    st.write(shopy_card(
      #       image_url="https://img2.chinadaily.com.cn/images/202410/15/670dca8fa310f1268d82d003.jpeg",
      #       supplier="Awesome Shop",
      #       verified="Verified Seller",
      #       price="$50/hour",
      #       time="2-4 days",
      #       age="5 years",
      #       location="New York"))
         
      #    st.write(shopy_card(
      #       image_url="https://img2.chinadaily.com.cn/images/202410/15/670dca8fa310f1268d82d003.jpeg",
      #       supplier="Awesome Shop",
      #       verified="Verified Seller",
      #       price="$50/hour",
      #       time="2-4 days",
      #       age="5 years",
      #       location="New York"))
      # cards_html = "".join([shop_card(**shop) for shop in shops])
      # # listOfContainers
      # # st.write()
      # container_html = f"""
      # <div style="
      #       height: 800px;
      #       overflow-y: scroll;
      #       display: grid;
      #       grid-template-columns: repeat(3, 1fr);
      #       gap: 10px;
      #       border: 1px solid #ccc;
      #       padding: 10px;">
      #    {cards_html}
      # </div>
      # """
      # st.markdown(container_html, unsafe_allow_html=True)

   with col2:
      chatbox()
