import streamlit as st
import datetime
import time
import base64
import os
import smtplib
from email.mime.text import MIMEText

def get_base64_image(image_path):
    if os.path.exists(image_path):
        with open(image_path, "rb") as img_file:
            return base64.b64encode(img_file.read()).decode()
    return None

def odeslat_vysledek_lukasovi(data):
    """Funkce pro automatické odeslání e-mailu Lukášovi přes SMTP."""
    try:
        # Načtení přihlašovacích údajů ze Streamlit Secrets
        odesilatel_email = st.secrets["email_user"]
        odesilatel_heslo = st.secrets["email_password"]
        prijemce = "lukasgranzer@seznam.cz"

        zprava_text = f"""
        Ahoj Lukáši, Bob naplánoval nový výlet! ❤️
        
        🌍 Lokalita: {data['region']}, {data['country']}
        👣 Styl výletu: {', '.join(data['trip_types'])}
        📏 Vzdálenost: {data['duration']} km
        📅 Termín: {data['hike_date']}
        ✉️ Poznámka: {data['notes']}
        """

        msg = MIMEText(zprava_text)
        msg['Subject'] = '🐧 Nové Mystery Dobrodružství!'
        msg['From'] = odesilatel_email
        msg['To'] = prijemce

        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(odesilatel_email, odesilatel_heslo)
            server.send_message(msg)
        return True
    except Exception as e:
        # Pokud nejsou nastaveny Secrets nebo dojde k chybě, aplikace nespadne
        print(f"Chyba při odesílání e-mailu: {e}")
        return False

def mystery_hike_app():
    # 1. KONFIGURACE STRÁNKY
    st.set_page_config(
        page_title="Pro mého Boba 🐧", 
        layout="centered", 
        page_icon="🐧"
    )

    # 2. MINI GALERIE V ZÁHLAVÍ (01-04)
    col_img1, col_img2, col_img3, col_img4 = st.columns(4)
    for col, img in zip([col_img1, col_img2, col_img3, col_img4], ["01.png", "02.png", "03.png", "04.png"]):
        with col:
            try: st.image(img, use_container_width=True)
            except: st.write("🖼️")

    # 3. HLAVIČKA A ÚVODNÍ TEXT
    st.title("🐧 Naše Mystery Dobrodružství")
    st.subheader("Ahoj milovaný Bobe! ❤️")
    
    st.markdown("##### Tohle je mnou naprogramovaný web pro soukromé plánování našich výletů.")
    
    st.markdown(f"""
    Tenhle chytrý prográmek jsem pro tebe vymyslel, aby se nám ty společné výlety 
    plánovaly úplně samy. Vyklikej si svou vysněnou cestu a já se postarám o zbytek!
    """)

    if 'submitted' not in st.session_state:
        st.session_state.submitted = False

    # 4. FORMULÁŘ
    if not st.session_state.submitted:
        with st.form("mystery_form"):
            st.header("🌎 Kdepak budeme ťapkat?")
            c1, c2 = st.columns(2)
            with c1: country = st.selectbox("Vyber kam na výlet", ["Česká republika", "Slovensko", "Rakousko", "Itálie", "Německo", "Polsko"])
            with c2: region = st.text_input("Oblíbený kraj", placeholder="třeba Jeseníky, Alpy...")
            
            trip_types = st.multiselect("Jak si to dneska užijeme?", ["Pěší ťapkání 👣", "Cyklo-tučňáci 🚲", "Lyžovačka ⛷️", "Běžkování ❄️", "Kulturní vyžití 🏰", "Mňamky a dobrůtky 🍰"], default=["Pěší ťapkání 👣"])
            
            st.header("📅 Kdy a jakou trasu?")
            c3, c4 = st.columns(2)
            with c3: hike_date = st.date_input("Den našeho výletu", datetime.date.today())
            with c4: duration = st.slider("Kolik kilometříků ujdeme?", 0, 100, 15)
            
            notes = st.text_area("Bobovo tajné přáníčko")
            submit_button = st.form_submit_button("Poslat pusinku a zadání Lukášovi 📩")

            if submit_button:
                st.session_state.submitted = True
                
                # Příprava dat pro zobrazení a e-mail
                data_pro_vystup = {
                    "country": country, 
                    "region": region, 
                    "trip_types": trip_types, 
                    "hike_date": hike_date, 
                    "duration": duration, 
                    "notes": notes if notes else 'Žádná'
                }
                
                # Automatické odeslání e-mailu
                data_pro_mail = data_pro_vystup.copy()
                data_pro_mail['hike_date'] = hike_date.strftime('%d. %m. %Y')
                odeslat_vysledek_lukasovi(data_pro_mail)
                
                # Uložení do session_state
                st.session_state.update(data_pro_vystup)
                st.rerun()

    # 5. AKCE PO ODESLÁNÍ (NEKONEČNÁ ANIMACE 06.png)
    if st.session_state.submitted:
        img_base64 = get_base64_image("06.png")
        
        if img_base64:
            animation_code = f"""
            <div style="position: fixed; top: 0; left: 0; width: 100vw; height: 100vh; pointer-events: none; z-index: 9999; overflow: hidden;">
                <style>
                @keyframes floatUp {{
                    0% {{ transform: translateY(110vh) rotate(0deg); opacity: 0; }}
                    10% {{ opacity: 1; }}
                    90% {{ opacity: 1; }}
                    100% {{ transform: translateY(-20vh) rotate(360deg); opacity: 0; }}
                }}
                .bob-photo {{
                    position: absolute;
                    width: 300px; 
                    animation: floatUp 5s linear infinite;
                }}
                </style>
                {''.join([f'<img src="data:image/png;base64,{img_base64}" class="bob-photo" style="left: {i*12}%; animation-delay: {i*0.8}s;">' for i in range(8)])}
            </div>
            """
            st.markdown(animation_code, unsafe_allow_html=True)
        
        st.success(f"Hotovo! Moje nejdůležitější databáze (srdíčko) právě přijala tvá přání.")

        # Zobrazení fotky 05
        st.markdown("---")
        try: 
            st.image("05.png", caption="Tvoje překvapení se už peče! ❤️", use_container_width=True)
        except: 
            st.info("📸 (Zde je fotka 05)")

        # Protokol pro Lukáše
        st.subheader("Recept na uvaření výletu pro Lukáše:")
        summary = f"""
        **ZADAVATEL:** Vendulka (Bob)
        **LOKALITA:** {st.session_state.region}, {st.session_state.country}
        **STYL VÝLETU:** {', '.join(st.session_state.trip_types)}
        **MAX. VZDÁLENOST:** {st.session_state.duration} km
        **TERMÍN:** {st.session_state.hike_date.strftime('%d. %m. %Y')}
        **POZNÁMKA:** {st.session_state.notes}
        """
        st.code(summary)
        
        if st.button("Zkusit naplánovat další ťapkání"):
            st.session_state.submitted = False
            st.rerun()

if __name__ == "__main__":
    mystery_hike_app()
