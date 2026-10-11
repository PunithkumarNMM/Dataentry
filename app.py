import streamlit as st
import qrcode
from docxtpl import DocxTemplate, InlineImage
from docx.shared import Inches
from io import BytesIO
import datetime

st.set_page_config(page_title="A5 Permit Generator", layout="wide")
st.title("A5 Mineral Dispatch Permit Data Entry")

# ==================== PASSWORD PROTECTION ====================
def check_password():
    """Returns `True` if the user enters the correct password."""
    def password_entered():
        # Change "admin123" to whatever password you want to set
        if st.session_state["password"] == "7505":
            st.session_state["password_correct"] = True
            del st.session_state["password"]  # Don't store the password in state
        else:
            st.session_state["password_correct"] = False

    if "password_correct" not in st.session_state:
        # First time opening the app or not logged in yet
        st.text_input("🔒 Enter Password to Access App", type="password", on_change=password_entered, key="password")
        return False
    elif not st.session_state["password_correct"]:
        # Incorrect password entered
        st.text_input("🔒 Enter Password to Access App", type="password", on_change=password_entered, key="password")
        st.error("😕 Incorrect password. Please try again.")
        return False
    else:
        # Password correct
        return True

# Stop execution of the rest of the app if password is not correct
if not check_password():
    st.stop()
# ==============================================================

def select_with_other(label, options, default_val):
    choice = st.selectbox(label, options + ["Others"])
    if choice == "Others":
        return st.text_input(f"Custom {label}", default_val)
    return choice

with st.form("permit_form"):
    col1, col2 = st.columns(2)

    with col1:
        form_ap_no = st.text_input("Form AP No", "BLRNSWP54230069")
        sr_no = st.text_input("Sr No", "0003069")
        mdp_no = st.text_input("MDP No", "BLRNSWP5423000069")
        lease_no = st.text_input("Lease No", "BLRNSWP54")
        barcode = st.text_input("Barcode", "MYZ117332769")
        lease_name = st.text_input("Lease Name", "Sobhamma S")
        dsc_no = st.text_input("DSC No", "/")
        gst_no = st.text_input("GST No", "/")
        
        type_of_land = select_with_other("Type of Land", ["Revenue", "Patta Land", "Forest"], "Revenue")
        taluk_district = select_with_other("Taluk/District", ["Hoskote/Bangalore Rural", "Bangalore Urban", "Devanahalli"], "Hoskote/Bangalore Rural")
        loading_place = select_with_other("Loading Place", ["Gullahalli"], "Gullahalli")
        
        qty_num = st.number_input("Quantity Number", value=36.0, step=0.01)
        qty_unit = st.selectbox("Quantity Unit", ["Metric Ton (MT)", "Others"])
        if qty_unit == "Others":
            qty_unit_custom = st.text_input("Custom Unit", "Metric Ton (MT)")
            quantity = f"{qty_num} {qty_unit_custom}"
        else:
            quantity = f"{qty_num} {qty_unit}"

    with col2:
        mdp_type = select_with_other("MDP Type", ["MT"], "MT")
        form_ap_purpose = select_with_other("Form AP Purpose", ["Karnataka", "Inter-State"], "Karnataka")
        mineral_grade = select_with_other("Mineral / Grade", ["Murram", "Building Stone", "M-Sand"], "Murram")
        
        total_volume = st.text_input("Total Volume", "0.00")
        total_blocks = st.text_input("Total Block(s)", "0")

        total_amount_paid = st.text_area("Total Amount Paid", "3666.97(Royalty :3486.91, DMF: 180.06,APP: 0, AAPP: 900. 30, TCS: 36.01 ,)")
        buyer = st.text_input("Buyer", "EM Bricks PVT LTD")
        route = st.text_area("Route", "Sy no 60, 1st Cross Road, Shree Ganesha Temple, Hunnigere, Bengaluru, Bengaluru Urban, Karnataka, 562130,93 KM")
        
        st.subheader("Validity Period & 12-Hour Time Selection")
        v_start_date = st.date_input("Start Date", datetime.date(2026, 10, 10), min_value=datetime.date(2000, 1, 1))
        
        st.markdown("**Start Time (12-hour)**")
        st_h, st_m, st_ap = st.columns(3)
        with st_h:
            start_hour = st.selectbox("Hour", list(range(1, 13)), index=5)
        with st_m:
            start_min = st.selectbox("Minute", [f"{i:02d}" for i in range(60)], index=10)
        with st_ap:
            start_ampm = st.selectbox("AM/PM", ["AM", "PM"], index=0)

        v_end_date = st.date_input("End Date", datetime.date(2026, 10, 10), min_value=datetime.date(2000, 1, 1))
        
        st.markdown("**End Time (12-hour)**")
        en_h, en_m, en_ap = st.columns(3)
        with en_h:
            end_hour = st.selectbox("End Hour", list(range(1, 13)), index=8)
        with en_m:
            end_min = st.selectbox("End Minute", [f"{i:02d}" for i in range(60)], index=40)
        with en_ap:
            end_ampm = st.selectbox("End AM/PM", ["AM", "PM"], index=0)
        
        validity_str = f"{v_start_date.strftime('%d/%m/%Y')} {start_hour}:{start_min} {start_ampm} to {v_end_date.strftime('%d/%m/%Y')} {end_hour}:{end_min} {end_ampm} (2hrs 30 minutes)"

        check_post = st.text_input("Check Post", "No Checkpost")
        vehicle_no = st.text_input("Vehicle No", "KA53B4375 / Tipper")
        crusher_unit = st.text_input("Crusher Unit", "-")
        mobile_no = st.text_input("Mobile No", "9876543210")
        destination = st.text_area("Destination", "Hunnigere, Bengaluru, Bengaluru Urban, Karnataka, (KA) – 562130 93 Km")
        
        copy_type = "Leaseholder Copy"

    submitted = st.form_submit_button("Generate A5 Word Document")

if submitted:
    doc = DocxTemplate("format.docx")

  qr_data = (
        f"Form AP No: {form_ap_no} / "
        f"MDP No: {mdp_no} / "
        f"Quantity: {quantity} / "
        f"Date and Time: {v_start_date.strftime('%d/%m/%Y')} {start_hour}:{start_min} {start_ampm} / "
        f"Vehicle Number: {vehicle_no} / "
        f"Buyer: {buyer} / "
        f"Mineral and Grade: {mineral_grade} / "
        f"Bar code: {barcode} / "
        f"Destination: {destination}"
    )

    qr = qrcode.QRCode(box_size=4, border=1)
    qr.add_data(qr_data)
    qr.make(fit=True)
    qr_img = qr.make_image(fill_color="black", back_color="white")
    
    qr_io = BytesIO()
    qr_img.save(qr_io, format="PNG")
    qr_io.seek(0)

    # Compact QR code width to fit precisely inside your template box
    inline_qr = InlineImage(doc, qr_io, width=Inches(0.5))

    context = {
        "form_ap_no": form_ap_no,
        "sr_no": sr_no,
        "mdp_no": mdp_no,
        "lease_no": lease_no,
        "barcode": barcode,
        "lease_name": lease_name,
        "dsc_no": dsc_no,
        "gst_no": gst_no,
        "type_of_land": type_of_land,
        "taluk_district": taluk_district,
        "loading_place": loading_place,
        "quantity": quantity,
        "mdp_type": mdp_type,
        "form_ap_purpose": form_ap_purpose,
        "mineral_grade": mineral_grade,
        "total_volume": total_volume,
        "total_blocks": total_blocks,
        "total_amount_paid": total_amount_paid,
        "buyer": buyer,
        "route": route,
        "validity": validity_str,
        "check_post": check_post,
        "vehicle_no": vehicle_no,
        "crusher_unit": crusher_unit,
        "mobile_no": mobile_no,
        "destination": destination,
        "copy_type": copy_type,
        "qr_code": inline_qr
    }

    doc.render(context)

    output_io = BytesIO()
    doc.save(output_io)
    output_io.seek(0)

    st.success("Document created successfully!")
    st.download_button(
        label="Download A5 Word Document",
        data=output_io,
        file_name=f"Permit_{mdp_no}.docx",
        mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
    )
