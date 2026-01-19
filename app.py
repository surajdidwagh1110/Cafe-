import streamlit as st
from datetime import datetime

st.set_page_config(page_title="Cafe Menu", page_icon="☕", layout="wide")

# Initialize session state
if "order_history" not in st.session_state:
	st.session_state.order_history = []
if "user_name" not in st.session_state:
	st.session_state.user_name = ""
if "user_phone" not in st.session_state:
	st.session_state.user_phone = ""
if "user_address" not in st.session_state:
	st.session_state.user_address = ""

menu = {
	"Coffee": 2.50,
	"Tea": 2.00,
	"Croissant": 3.00,
	"Bagel": 2.75,
	"Sandwich": 5.50,
}

# Initialize qty in session state
for item in menu:
	if f"qty_{item}" not in st.session_state:
		st.session_state[f"qty_{item}"] = 0

st.title("☕ Cafe Menu")
st.header("Welcome! Choose items and place your order.")

# User Details Section
st.subheader("Your Details")
col1, col2, col3 = st.columns(3)
with col1:
	st.session_state.user_name = st.text_input("Name", value=st.session_state.user_name, placeholder="Enter your name")
with col2:
	st.session_state.user_phone = st.text_input("Phone", value=st.session_state.user_phone, placeholder="Enter your phone")
with col3:
	st.session_state.user_address = st.text_input("Address", value=st.session_state.user_address, placeholder="Enter delivery address")

st.divider()

# Menu Selection
st.subheader("Menu Items")
cols = st.columns(2)

with st.form("order_form"):
	for i, (item, price) in enumerate(menu.items()):
		col = cols[i % 2]
		with col:
			st.session_state[f"qty_{item}"] = st.number_input(
				f"{item} — ${price:.2f}",
				min_value=0,
				step=1,
				value=st.session_state[f"qty_{item}"],
				key=f"input_{item}"
			)
	submitted = st.form_submit_button("Calculate Total")

# Order Summary & Checkout
ordered = {item: st.session_state[f"qty_{item}"] for item in menu if st.session_state[f"qty_{item}"] > 0}

if submitted:
	if not st.session_state.user_name or not st.session_state.user_phone:
		st.error("⚠️ Please enter your name and phone number.")
	elif not ordered:
		st.info("No items selected.")
	else:
		st.subheader("Order Summary")
		subtotal = 0.0
		for item, qty in ordered.items():
			price = menu[item]
			line_total = price * qty
			subtotal += line_total
			st.write(f"• {item} x {qty} = ${line_total:.2f}")
		tax_rate = 0.08
		tax = subtotal * tax_rate
		total = subtotal + tax
		st.divider()
		st.write(f"**Subtotal:** ${subtotal:.2f}")
		st.write(f"**Tax ({int(tax_rate*100)}%):** ${tax:.2f}")
		st.write(f"**Total:** ${total:.2f}")
		st.write(f"**Delivery to:** {st.session_state.user_address}")
		
		if st.button("✅ Place Order", use_container_width=True):
			order_data = {
				"timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
				"name": st.session_state.user_name,
				"phone": st.session_state.user_phone,
				"address": st.session_state.user_address,
				"items": ordered,
				"total": total
			}
			st.session_state.order_history.append(order_data)
			st.success(f"✅ Order placed! Order ID: #{len(st.session_state.order_history)}")
			# Reset form
			for item in menu:
				st.session_state[f"qty_{item}"] = 0
			st.rerun()

# Order History
if st.session_state.order_history:
	st.divider()
	st.subheader("📋 Order History")
	for idx, order in enumerate(st.session_state.order_history, 1):
		with st.expander(f"Order #{idx} — {order['name']} ({order['timestamp']})"):
			st.write(f"**Phone:** {order['phone']}")
			st.write(f"**Address:** {order['address']}")
			st.write("**Items:**")
			for item, qty in order['items'].items():
				st.write(f"  • {item} x {qty}")
			st.write(f"**Total:** ${order['total']:.2f}")