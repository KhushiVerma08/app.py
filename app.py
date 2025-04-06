import streamlit as st
import requests

BACKEND_URL = "https://online-shopping-system-9a7t.onrender.com"  # Replace with your backend URL

st.title("🛍️ Online Shopping System")

# Get products
res = requests.get(f"{BACKEND_URL}/products")
products = res.json() if res.status_code == 200 else []

st.subheader("📦 Products")
for product in products:
    st.write(f"**{product['name']}** - ${product['price']} | Stock: {product['stock']}")
    qty = st.number_input(f"Quantity of {product['name']}", 1, product['stock'], key=f"qty_{product['id']}")
    if st.button(f"Add to Cart {product['name']}", key=f"add_{product['id']}"):
        resp = requests.post(f"{BACKEND_URL}/cart", json={
            "id": product["id"],
            "name": product["name"],
            "price": product["price"],
            "quantity": qty
        })
        if resp.status_code == 201:
            st.success("Added to cart!")
        else:
            st.error("Failed to add!")

# View Cart
st.subheader("🛒 Cart")
cart_res = requests.get(f"{BACKEND_URL}/cart")
cart = cart_res.json() if cart_res.status_code == 200 else []

total = 0
for item in cart:
    st.write(f"{item['name']} x {item['quantity']} = ${item['quantity'] * item['price']}")
    total += item['price'] * item['quantity']
    if st.button(f"Remove {item['name']}", key=f"del_{item['id']}"):
        requests.delete(f"{BACKEND_URL}/cart/{item['id']}")
        st.rerun()

st.markdown(f"### 💰 Total: ${total}")
