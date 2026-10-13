import streamlit as st
import qrcode
from docxtpl import DocxTemplate, InlineImage
from docx.shared import Inches
from io import BytesIO
import datetime

st.set_page_config(page_title="A5 Permit Generator - Trail & Error", layout="wide")

# ==================== FULL-SCREEN STYLING ====================
st.markdown("""
    <style>
    .stApp {
        background: linear-gradient(135deg, #0f172a 0%, #1e293b 50%, #0f172a 100%);
        color: #f8fafc;
    }
    .fullscreen-splash {
        position: fixed;
        top: 0;
        left: 0;
        width: 100vw;
        height: 100vh;
        background: radial-gradient(circle at center, #1e293b 0%, #0f172a 100%);
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        z-index: 99999;
        padding: 2rem;
        overflow-y: auto;
    }
    .brand-title {
        font-size: 3.2rem;
        font-weight: 800;
        letter-spacing: 3px;
        background: linear-gradient(90deg, #38bdf8, #818cf8);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        margin-top: 1rem;
        margin-bottom: 0.5rem;
    }
    .brand-subtitle {
        font-size: 1.4rem;
        font-weight: 500;
        color: #94a3b8;
        letter-spacing: 1.5px;
        text-align: center;
        margin-bottom: 2rem;
    }
    .welcome-banner {
        padding: 1rem;
        background: rgba(56, 189, 248, 0.1);
        border-left: 4px solid #38bdf8;
        border-radius: 4px;
        margin-bottom: 1.5rem;
    }
    </style>
""", unsafe_allow_html=True)

# ==================== SESSION ROUTING ====================
if "auth_step" not in st.session_state:
    st.session_state["auth_step"] = "image_screen"

if "operator_name" not in st.session_state:
    st.session_state["operator_name"] = ""

if "authenticated" not in st.session_state:
    st.session_state["authenticated"] = False

# Screen 1: Full-Screen Image & Branding
if st.session_state["auth_step"] == "image_screen":
    st.markdown("<div class='fullscreen-splash'>", unsafe_allow_html=True)
    
    # Safe image loader with error fallback so it never shows a blank screen
    try:
        st.image("logo.png", width=650)
    except Exception:
        st.markdown("<h1 style='color: #38bdf8; font-size: 4rem; text-align: center;'>T & E</h1>", unsafe_allow_html=True)
        
    st.markdown("<div class='brand-title'>TRAIL & ERROR</div>", unsafe_allow_html=True)
    st.markdown("<div class='brand-subtitle'>Crafted By Punith Kumar N M</div>", unsafe_allow_html=True)
    
    col_btn1, col_btn2, col_btn3 = st.columns([2, 1.5, 2])
    with col_btn2:
        if st.button("🚀 Proceed to Secure Portal", use_container_width=True):
            st.session_state["auth_step"] = "login_screen"
            st.rerun()
            
    st.markdown("</div>", unsafe_allow_html=True)
    st.stop()

# Screen 2: Password and Operator Name Entry
elif st.session_state["auth_step"] == "login_screen":
    col1, col2, col3 = st.columns([1, 1.5, 1])
    with col2:
        st.markdown("<h2 style='text-align: center; color: #38bdf8;'>🔒 Authentication Required</h2>", unsafe_allow_html=True)
        st.write("")
        
        with st.form("login_form"):
            operator_input = st.text_input("Enter Your Name")
            password_input = st.text_input("Enter Password", type="password")
            submitted_login = st.form_submit_button("Access Portal", use_container_width=True)
            
            if submitted_login:
                if not operator_input.strip():
                    st.error("⚠️ Please enter your name.")
                elif password_input == "admin123":  # Change password here if desired
                    st.session_state["operator_name"] = operator_input.strip()
                    st.session_state["authenticated"] = True
                    st.session_state["auth_step"] = "app_screen"
                    st.rerun()
                else:
                    st.error("❌ Incorrect password. Please try again.")
                    
        if st.button("⬅️ Back to Home"):
            st.session_state["auth_step"] = "image_screen"
            st.rerun()
    st.stop()

# ==================== SCREEN 3: WELCOME & DATA ENTRY ====================
st.markdown(f"""
    <div class='welcome-banner'>
        <h3 style='margin:0; color: #38bdf8;'>👋 Welcome, {st.session_state["operator_name"]}!</h3>
        <p style='margin:0; color: #cbd5e1;'>Portal unlocked. You can now generate A5 Mineral Dispatch Permits.</p>
    </div>
""", unsafe_allow_html=True)

st.title("A5 Mineral Dispatch Permit Data Entry")

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
        
        st.subheader("Validity Period & Start Time")
        v_start_date = st.date_input("Start Date", datetime.date(2026, 10, 10), min_value=datetime.date(2000, 1, 1))
        
        st.markdown("**Start Time (12-hour)**")
        st_h, st_m, st_ap = st.columns(3)
        with st_h:
            start_hour = st.selectbox("Hour", list(range(1, 13)), index=5)
        with st_m:
            start_min = st.selectbox("Minute", [f"{i:02d}" for i in range(60)], index=10)
        with st_ap:
            start_ampm = st.selectbox("AM/PM", ["AM", "PM"], index=0)

        duration_options = []
        total_minutes_list = []
        for minutes in range(15, 24 * 60 + 1, 15):
            hrs = minutes // 60
            mins = minutes % 60
            if hrs > 0 and mins > 0:
                label = f"{hrs}hrs {mins} minutes"
            elif hrs > 0:
                label = f"{hrs}hrs"
            else:
                label = f"{mins} minutes"
            duration_options.append(label)
            total_minutes_list.append(minutes)

        selected_duration_label = st.selectbox(
            "Validity Duration", 
            duration_options,
            index=duration_options.index("2hrs 30 minutes") if "2hrs 30 minutes" in duration_options else 10
        )
        
        selected_total_minutes = total_minutes_list[duration_options.index(selected_duration_label)]

        check_post = st.text_input("Check Post", "No Checkpost")
        vehicle_no = st.text_input("Vehicle No", "KA53B4375 / Tipper")
        crusher_unit = st.text_input("Crusher Unit", "-")
        mobile_no = st.text_input("Mobile No", "9876543210")
        destination = st.text_area("Destination", "Hunnigere, Bengaluru, Bengaluru Urban, Karnataka, (KA) – 562130 93 Km")
        
        copy_type = "Leaseholder Copy"

    submitted = st.form_submit_button("Generate A5 Word Document")

if submitted:
    h_24 = start_hour
    if start_ampm == "PM" and start_hour != 12:
        h_24 += 12
    elif start_ampm == "AM" and start_hour == 12:
        h_24 = 0

    start_dt = datetime.datetime.combine(v_start_date, datetime.time(h_24, int(start_min)))
    delta = datetime.timedelta(minutes=selected_total_minutes)
    end_dt = start_dt + delta

    start_date_str = v_start_date.strftime('%d/%m/%Y')
    start_time_str = f"{start_hour}:{start_min} {start_ampm}"
    start_date_time = f"{start_date_str} {start_time_str}"

    end_date_str = end_dt.strftime('%d/%m/%Y')
    end_hour_12 = end_dt.strftime('%I').lstrip('0')
    if not end_hour_12: 
        end_hour_12 = "12"
    end_min_str = end_dt.strftime('%M')
    end_ampm_str = end_dt.strftime('%p')
    end_time_str = f"{end_hour_12}:{end_min_str} {end_ampm_str}"

    validity_str = f"{start_date_time} to {end_date_str} {end_time_str} ({selected_duration_label})"

    doc = DocxTemplate("format.docx")

    qr_data = (
        f"Form AP No: {form_ap_no} / "
        f"MDP No: {mdp_no} / "
        f"Quantity: {quantity} / "
        f"Date and Time: {validity_str} / "
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
        "start_date_time": start_date_time,
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
