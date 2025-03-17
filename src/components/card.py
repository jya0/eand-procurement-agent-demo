import streamlit as st

def shop_card(image_url, supplier, verified, price, time, age, location):
    card_html = f"""
    <div style="
         width: 100%;
         border: 1px solid #ddd;
         border-radius: 10px;
         padding: 15px;
         box-shadow: 2px 2px 5px rgba(0,0,0,0.1);
         background-color: white;
         color: #333;
         font-family: Arial, sans-serif;">
      <img src="{image_url}" style="width:100%; border-radius:8px;" alt="Shop Image">
      <h3 style="color: #222; margin-bottom: 5px;">{supplier}</h3>
      <p style="color: #4CAF50; font-weight: bold;">{verified}</p>
      <p style="color: #333;"><strong>Price:</strong> {price}</p>
      <p style="color: #333;"><strong>Time:</strong> {time}</p>
      <p style="color: #333;"><strong>Age:</strong> {age}</p>
      <p style="color: #333;"><strong>Location:</strong> {location}</p>
    </div>
    """
    # return st.container
    return card_html