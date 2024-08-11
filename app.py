import streamlit as st
import pandas as pd
import gspread
from google.oauth2.service_account import Credentials
from datetime import datetime, timedelta
import time

# 直接在代碼中定義憑證
credentials_info = {
    "type": "service_account",
    "project_id": "learned-helper-431815-p2",
    "private_key_id": "00910552f4792ff8576465e035b24fa7e4eaa805",
    "private_key": "-----BEGIN PRIVATE KEY-----\nMIIEvQIBADANBgkqhkiG9w0BAQEFAASCBKcwggSjAgEAAoIBAQCSm2fA4tfB26tK\nYkjCqi0rGkzm4GdLucOpKqddXn5QcKTcQCqa0Te3rcr9uQDt/DDV99Z/xCrX1ab4\nGoS77i8FbqxLczUUyy0iiwocl9Cd8yfkvCanaHS4dxendteUZjwojGvjnWZbBcFm\n04Y2CQxzjCI6cw4aBcpwqO5sfzJ57oLh7a4RuACfqNKclvtbDtiBR0FkT498zKeE\nLsGUOq09+TcR/aIefb/mqio6pzJmBPe5CDCEbLT5YoJ3sHakbG5Ss8+0dWf5eT8K\nfeTN4AuGA0S1dJi7OxGowxiLXDD6P7qyYVg+WP9UJfk9sw4p13d0KN7rsh5BvoNz\n7EYXTrVNAgMBAAECggEAH2DpvQwQV+q3Z81Pe3LHBiGz8fp3wWp6KVv6xG40JO1n\nK8kEFWzQOx0UhGezfjxrC3DnVSNcdCPDf/jVDhA1ujjs4Z0/8DpoZ6tQt7v6p8Pi\ndv+aWlxuFwlOY8Z478dN+vPLJ8WJodPCiEqfwDMBmj2VGeOEUieJI8HUfh5fZF9I\nUIDGBNGnmi6kZNdBEfSqaLrlK6d2a6PzJN0kNJvEMPPhq8+goYLRHaq6HZhRvHhK\nYiL2KW9/ob1mpsT3EscCoOSGkmIFo/7sZ8K0CzySBFBbKBaxEBqn3yPpXoBjgSK9\neELApyQlKB7NF4D/vlItObJHuIgN2J+U/DT+M/0i9QKBgQDMlVTyigkZ2KKaljqc\nn+AE66wMvDqGuIcn+gnEs7INF6Aozio5pCj8VYFC4jof4b55p2KLQd0KkKr79qu1\nuln+zeJS38Le4VzYN95f3GH0wAMP8Xql0DeZQzB0jCS50U2sTU912zRGTGCd/j9a\nSwF/ifKSgNB7HYJ8qDyIAONzjwKBgQC3c/FwU7rdumiiJI24l8gfypT77Ic+n0Cv\nGpeU3zhdDDrk/OYbWUDEpzo+4yPrEBw+xLJS/2fOKE9q1UUblm2pnKs+iyMRWiri\nnyxFV2Rn5itu2Uu1XN2L0ayxa/nVV17ReXz2MOdJPbhgXuVcwUDQsmSOUtTRik1D\nHhHZjhArYwKBgGR1K5pRR7jGVMod3LgOFV21L+2s+/wtXki2Edfh+RtOr5l56ugV\nAP8vKWLjXXFMU1C/bbc950GJ2jwRWy3ITOq+xFS3haQV+5Y8kNh3ii45nwdUJ0qG\nnNaIVKHWMy5/ZWmnKM6RjfC7DnJmZ0t6K0kqPs/LqxPZYLq/jcGm1glnAoGAarQm\nf6ZD74noKD9Iq1ClV1B2nZ1zAMqSTgcSmcXIO97MNrqegNPGJ1v5NfDZyHSjaSLx\ncfMahr/NiZ8oxiYV/Oyicgttxz8B6LSahG6TeRdYte3v6jpsplG7t6rNMvjRrteS\nBoRlUqVyo6Mul2fUck8AzAODw6lEzUAlM7w8zW8CgYEAiPVHwNgQjahk/CWJDC9V\nl6Bynwsbrg350yoPh+mK40b3V94TbIds9mK+k0IDB0dL2vtSn2yDgkjd0icXD0P7\nxJkcUA85Ff09g1hZaidnBjuNi0RJqTdPv6GbGzT8/sufK4SQv8mi90xs+CxwQi7Z\nYjfyrq3IA1nlLt7O7YXV4hc=\n-----END PRIVATE KEY-----\n",
    "client_email": "musicclubhku@learned-helper-431815-p2.iam.gserviceaccount.com",
    "client_id": "101515430452934299650",
    "auth_uri": "https://accounts.google.com/o/oauth2/auth",
    "token_uri": "https://oauth2.googleapis.com/token",
    "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
    "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/musicclubhku%40learned-helper-431815-p2.iam.gserviceaccount.com",
    "universe_domain": "googleapis.com"
}

# 創建 Credentials 對象，包含正確的範圍
scopes = ["https://www.googleapis.com/auth/spreadsheets"]
credentials = Credentials.from_service_account_info(credentials_info, scopes=scopes)

# 使用 gspread 來進行認證
gc = gspread.authorize(credentials)

# 獲取 Google Sheet
sheet = None
try:
    workbook = gc.open_by_key('1QiHaWbAecEk9mykRmAb7AmLgW3qMhjUop5WqQr3fVAo')
    sheet = workbook.worksheet('Sheet1')
except Exception as e:
    st.error(f"Error fetching the worksheet: {str(e)}")

# 檢查工作表是否成功獲取
if sheet is not None:
    # 將 Google Sheet 轉換為 DataFrame
    values = sheet.get_all_values()
    if not values:
        # 如果工作表為空，則添加標題
        headers = ['Order ID', 'Product', 'Amount', 'Unit Price', 'Total Price', 'Order Price', 'Member', 'Payment Method', 'Remark', 'Purchase Time']
        sheet.append_row(headers)
        values = [headers]
    df = pd.DataFrame(values[1:], columns=values[0])

    # 定義價格和圖片 URL
    price_member = {
        "Pin(Mic)": 30, "Pin(Piano)": 30, "Pin(Drum)": 30, "Pin(Bass)": 30,
        "Pin(Acoustic guitar)": 30, "Pin(Electric guitar)": 30, "Guitar pick set": 35,
        "Bag": 50, "Bottle": 60, "Stickers": 20, "Soc T (White)(M)": 65, "Soc T (White)(L)": 65,
        "Soc T (Black)(M)": 65, "Soc T (Black)(L)": 65,
        "Computer Bag (Blue)": 65, "Computer Bag (Black)": 65
    }

    price_non_member = {
        "Pin(Mic)": 40, "Pin(Piano)": 40, "Pin(Drum)": 40, "Pin(Bass)": 40,
        "Pin(Acoustic guitar)": 40, "Pin(Electric guitar)": 40, "Guitar pick set": 45,
        "Bag": 65, "Bottle": 75, "Stickers": 25, "Soc T (White)(M)": 80, "Soc T (White)(L)": 80,
        "Soc T (Black)(M)": 80, "Soc T (Black)(L)": 80,
        "Computer Bag (Blue)": 80, "Computer Bag (Black)": 80
    }

    image_urls = {
        "Pin(Mic)": "https://i.ibb.co/tXLvH5M/5.png",
        "Pin(Piano)": "https://i.ibb.co/pXsRyDt/1.png",
        "Pin(Drum)": "https://i.ibb.co/kSX9yD7/4.png",
        "Pin(Bass)": "https://i.ibb.co/xgnM8hQ/3.png",
        "Pin(Acoustic guitar)": "https://i.ibb.co/R6JhLfs/2.png",
        "Pin(Electric guitar)": "https://i.ibb.co/sJcFwf5/6.png",
        "Guitar pick set": "https://i.imgur.com/SaetUTy.jpeg",
        "Bag": "https://i.imgur.com/1GsCIQk.jpeg",
        "Bottle": "https://i.imgur.com/mmS2uQn.jpeg",
        "Stickers": "https://i.imgur.com/IJV4Csx.jpeg",
        "Soc T (White)": "https://i.imgur.com/PnFMCpu.jpeg",
        "Soc T (Black)": "https://i.imgur.com/cNIQgB9.jpeg",
        "Computer Bag (Blue)": "https://i.imgur.com/ZFgyyUI.png",
        "Computer Bag (Black)": "https://i.imgur.com/cRsCW9H.png"
    }

    # Streamlit app layout
    st.set_page_config(page_title="Music Club", layout="wide", page_icon="https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQzm6CccDRv29fOOTVnmdWqjXQkX5pki_D_FHoeHkrEEGek43K66hpoySORfTHqILS1DU4&usqp=CAU")

    st.image("https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQzm6CccDRv29fOOTVnmdWqjXQkX5pki_D_FHoeHkrEEGek43K66hpoySORfTHqILS1DU4", width=100)
    st.title("MUSIC CLUB, HKU")
    st.text("#一張單只可以有一個ComboSet")
    st.link_button("Go to sheet", "https://docs.google.com/spreadsheets/d/1QiHaWbAecEk9mykRmAb7AmLgW3qMhjUop5WqQr3fVAo/edit?gid=0#gid=0")

    # Initialize session state
    if 'quantities' not in st.session_state:
        st.session_state.quantities = {product: 0 for product in image_urls.keys()}
    if 'clear_flag' not in st.session_state:
        st.session_state.clear_flag = False
    if 'remark_key' not in st.session_state:
        st.session_state.remark_key = 0

    # Container for product selection
    st.subheader("Select Products")
    cols = st.columns(7)

    for idx, product in enumerate(image_urls.keys()):
        with cols[idx % 7]:
            st.image(image_urls[product], caption=product, use_column_width=True)
            
            if product in ["Soc T (White)", "Soc T (Black)"]:
                col1, col2 = st.columns(2)
                with col1:
                    quantity_m = st.number_input(
                        f"Quantity (M)",
                        min_value=0,
                        max_value=100,
                        step=1,
                        value=0 if st.session_state.clear_flag else st.session_state.quantities.get(f"{product}(M)", 0),
                        key=f"quantity_{product}(M)"
                    )
                with col2:
                    quantity_l = st.number_input(
                        f"Quantity (L)",
                        min_value=0,
                        max_value=100,
                        step=1,
                        value=0 if st.session_state.clear_flag else st.session_state.quantities.get(f"{product}(L)", 0),
                        key=f"quantity_{product}(L)"
                    )
                st.session_state.quantities[f"{product}(M)"] = quantity_m
                st.session_state.quantities[f"{product}(L)"] = quantity_l
            else:
                quantity = st.number_input(
                    "Quantity",
                    min_value=0,
                    max_value=100,
                    step=1,
                    value=0 if st.session_state.clear_flag else st.session_state.quantities.get(product, 0),
                    key=f"quantity_{product}"
                )
                st.session_state.quantities[product] = quantity

    # Order details section
    st.subheader("Order Details")

    # Checkbox for member status
    member = st.checkbox("Member", key="member", value=False if st.session_state.clear_flag else st.session_state.get('member', False))

    # Radio buttons for payment method
    payment_method = st.radio(
        "Select Payment Method",
        options=["PayMe", "FPS", "Alipay", "Cash"],
        index=0,  # Default selection
        key="payment_method"
    )

    # Calculate total price without discount
    total_price = sum(
        (price_member[product] if member else price_non_member[product]) * quantity
        for product, quantity in st.session_state.quantities.items() if quantity > 0
    )
    # Apply rules for discounts and set remark
    if member:
        pins_count = sum(st.session_state.quantities[product] for product in price_member if 'Pin' in product)
        t_shirt_count = sum(st.session_state.quantities.get(f"Soc T ({color})({size})", 0) for color in ["White", "Black"] for size in ["M", "L"])
        computer_bag_count = st.session_state.quantities.get("Computer Bag (Blue)", 0) + st.session_state.quantities.get("Computer Bag (Black)", 0)
        
        if (t_shirt_count >= 1 and st.session_state.quantities.get("Bottle", 0) >= 1 and 
            st.session_state.quantities.get("Bag", 0) >= 1 and computer_bag_count >= 1):
            auto_remark = "Combo Set D"
            total_price -= 90
        elif pins_count >= 3:
            auto_remark = "Combo Set B"
            total_price -= 15
        elif st.session_state.quantities.get("Bag", 0) >= 1 and pins_count >= 1:
            auto_remark = "Combo Set A"
            total_price -= 15
        elif st.session_state.quantities.get("Bag", 0) >= 1 and t_shirt_count >= 1:
            auto_remark = "Combo Set C"
            total_price -= 20
        else:
            auto_remark = ""
    else:
        auto_remark = ""

    # Display calculated remark, allowing user input but prefilling with the suggested combo remark
    remark = st.text_input("Remark", value=auto_remark, key=f"remark_{st.session_state.remark_key}")

    # Display selected products and quantities
    selected_items = []
    for product, quantity in st.session_state.quantities.items():
        if quantity > 0:
            selected_items.append(f"{product}: {quantity}")
    if selected_items:
        st.write("You have selected the following items:")
        st.write(", ".join(selected_items))
    else:
        st.write("No items selected.")

    st.write(f"Total Price: **${total_price}**")

    # Define button layout
    button_layout = st.columns(4)

    # Add Submit Order button
    with button_layout[0]:
        if st.button("Submit Order"):
            if total_price == 0:
                st.warning("Please select at least one product.")
            else:
                new_order_id = f"{int(df['Order ID'].max()) + 1:06d}" if not df['Order ID'].empty else "000001"
                new_rows = []
                purchase_time = (datetime.now() + timedelta(hours=8)).strftime("%Y-%m-%d %H:%M:%S")
                order_price_logged = False  # Track if order price has been logged

                for product, amount in st.session_state.quantities.items():
                    if amount > 0:
                        unit_price = price_member[product] if member else price_non_member[product]
                        total_item_price = unit_price * amount
                        if not order_price_logged:
                            new_rows.append([new_order_id, product, amount, unit_price, total_item_price, total_price, member, payment_method, remark, purchase_time])
                            order_price_logged = True
                        else:
                            new_rows.append([new_order_id, product, amount, unit_price, total_item_price, '', member, payment_method, remark, purchase_time])  # Leave Order Price empty since it's logged once

                sheet.append_rows(new_rows)
                st.success(f"Order {new_order_id} Submitted Successfully!")
                time.sleep(2)
                st.session_state.clear_flag = True
                st.session_state.remark_key += 1
                st.rerun()

    # Add Clear button
    with button_layout[1]:
        if st.button("Clear Inputs"):
            st.session_state.clear_flag = True
            st.session_state.remark_key += 1
            st.success("Inputs cleared successfully!")
            time.sleep(2)
            st.rerun()

    # Reset clear flag back to False after rerun
    if st.session_state.clear_flag:
        for product in st.session_state.quantities.keys():
            st.session_state.quantities[product] = 0
        st.session_state.clear_flag = False

    # Add Reload Data button
    with button_layout[2]:
        if st.button("Reload Data"):
            values = sheet.get_all_values()
            df = pd.DataFrame(values[1:], columns=values[0])
            st.write("Data reloaded.")

    # Add Show Last Order Record button
    with button_layout[3]:
        if st.button("Show Last Order Record"):
            if not df.empty:
                last_order_id = df.iloc[-1]['Order ID']
                st.write(f"Last Order ID: {last_order_id}")
                st.write("Order Details:")
                last_order = df[df['Order ID'] == last_order_id]
                for index, row in last_order.iterrows():
                    st.write(f" - {row['Product']}: {row['Amount']} (Price: ${row['Unit Price']})")
                    st.write(f"   Purchase Time: {row['Purchase Time']}")
            else:
                st.warning("No records found.")
