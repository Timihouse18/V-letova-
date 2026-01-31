import streamlit as st
import datetime
import base64
import os
import urllib.parse

def get_base64_image(image_path):
    """Zakóduje obrázek do base64 pro použití v CSS animaci."""
    if os.path.exists(image_path):
        with open(image_path, "rb") as img_file:
            return base64.b64encode(img_file.read()).decode()
    return None

def vygeneruj_whatsapp_odkaz(data):
    """Vytvoří odkaz pro přímé odeslání dat na WhatsApp Lukášovi."""
    # Vaše zadané číslo v mezinárodním formátu
    moje_cislo = "420728898135" 
    
    text_zpravy = f"""*🐧 Mystery Výlet naplánován!*
    
📍 *Lokalita:* {data['region']}, {data['country']}
👣 *Styl:* {', '.join(data['trip_types'])}
📏 *Vzdálenost:* {data['duration']} km
📅 *Termín:* {data['hike_date']}
✉️ *Poznámka:* {data['notes']}

_Těším se na naše dobrodružství! ❤️_"""
    
    # Kódování textu pro URL (nahrazení speciálních znaků)
    encoded_text = urllib.parse.quote(text_zpravy)
    return f"https://wa.me/{moje_cislo}?text={encoded_text}"

def mystery_hike_app():
    # 1. KONFIGURACE STRÁNKY
    st.set_page_config(
        page_title="Pro mého Boba 🐧", 
        layout="centered", 
        page_icon="🐧"
    )
    st.title("🐧 Naše Mystery Dobrodružství, slajdni dolů pro výlet!")
    
    # 2. MINI GALERIE V ZÁHLAVÍ (01-04)
    col1, col2, col3, col4 = st.columns(4)
    for col, img in zip([col1, col2, col3, col4], ["01.png", "02.png", "03.png", "04.png"]):
        with col:
            try: st.image(img, use_container_width=True)
            except: st.write("🖼️")

    # 3. HLAVIČKA A ÚVODNÍ TEXT
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
                st.session_state.update({
                    "country": country, "region": region, "trip_types": trip_types, 
                    "hike_date": hike_date, "duration": duration, "notes": notes if notes else "Žádná"
                })
                st.rerun()

    # 5. AKCE PO ODESLÁNÍ (ANIMACE A WHATSAPP)
    if st.session_state.submitted:
        # Nekonečná animace létajících velkých obrázků 06.png
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
                    width: 100px; 
                    animation: floatUp 5s linear infinite;
                }}
                </style>
                {''.join([f'<img src="data:image/png;base64,{img_base64}" class="bob-photo" style="left: {i*12}%; animation-delay: {i*0.8}s;">' for i in range(8)])}
            </div>
            """
            st.markdown(animation_code, unsafe_allow_html=True)
        
        st.success("Hotovo! Moje nejdůležitější databáze (srdíčko) právě přijala tvá přání.")

        # VELKÉ WHATSAPP TLAČÍTKO PRO ODESLÁNÍ
        wa_link = vygeneruj_whatsapp_odkaz({
            "country": st.session_state.country,
            "region": st.session_state.region,
            "trip_types": st.session_state.trip_types,
            "hike_date": st.session_state.hike_date.strftime('%d. %m. %Y'),
            "duration": st.session_state.duration,
            "notes": st.session_state.notes
        })
        
        st.markdown(f"""
            <a href="{wa_link}" target="_blank" style="text-decoration: none;">
                <div style="background-color: #25D366; color: white; padding: 25px; text-align: center; border-radius: 20px; font-weight: bold; font-size: 24px; margin: 25px 0; box-shadow: 0 4px 15px rgba(0,0,0,0.3); border: 2px solid #128C7E;">
                    KLIKNI SEM A POŠLI PLÁN LUKÁŠOVI 🟢
                </div>
            </a>
        """, unsafe_allow_html=True)

        st.markdown("---")
        # Zobrazení fotky 05
        try: 
            st.image("05.png", caption="Tvoje překvapení se už peče! ❤️", use_container_width=True)
        except: 
            st.info("📸 (Zde je fotka 05)")

        # Tlačítko pro nový pokus
        if st.button("Zkusit naplánovat další ťapkání"):
            st.session_state.submitted = False
            st.rerun()

if __name__ == "__main__":
    mystery_hike_app()



