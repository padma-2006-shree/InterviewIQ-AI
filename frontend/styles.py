import streamlit as st


def load_css():
    st.markdown("""
    <style>
    /* -----------------------------
       Background & Typography
    ------------------------------*/
    .stApp {
        background: linear-gradient(
            135deg,
            #0B1120 0%,
            #111827 40%,
            #1E293B 100%
        );
        color: #F8FAFC;
    }

    .main .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
        max-width: 1250px;
    }

    /* Scrollbar */
    ::-webkit-scrollbar {
        width: 8px;
    }
    ::-webkit-scrollbar-thumb {
        background: #3B82F6;
        border-radius: 8px;
    }

    /* Headings */
    h1 {
        color: #FFFFFF;
        font-size: 42px;
        font-weight: 800;
        letter-spacing: -0.5px;
    }
    h2 {
        color: #F1F5F9;
        font-weight: 700;
    }
    h3 {
        color: #E2E8F0;
    }
    p, label {
        color: #CBD5E1;
    }

    /* -----------------------------
       Buttons
    ------------------------------*/
    .stButton>button {
        width: 100%;
        background: linear-gradient(90deg, #2563EB, #3B82F6);
        color: white;
        border: none;
        border-radius: 10px;
        padding: 10px 18px;
        font-weight: 700;
        font-size: 15px;
        transition: all 0.25s ease;
        box-shadow: 0 4px 14px rgba(37, 99, 235, 0.35);
    }
    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(37, 99, 235, 0.55);
        background: linear-gradient(90deg, #1D4ED8, #2563EB);
    }

    /* -----------------------------
       Cards & Glassmorphism
    ------------------------------*/
    .glass {
        background: rgba(255, 255, 255, 0.05);
        backdrop-filter: blur(16px);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 16px;
        padding: 22px;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.25);
        margin-bottom: 20px;
    }

    .hero {
        padding: 30px;
        border-radius: 20px;
        background: linear-gradient(135deg, rgba(37, 99, 235, 0.2), rgba(17, 24, 39, 0.8));
        border: 1px solid rgba(255, 255, 255, 0.12);
        margin-bottom: 24px;
    }
    .hero-title {
        font-size: 44px;
        font-weight: 800;
        color: white;
        line-height: 1.15;
    }
    .hero-sub {
        color: #94A3B8;
        font-size: 17px;
        margin-top: 10px;
    }
    .highlight {
        color: #60A5FA;
    }

    /* -----------------------------
       Skill Badges
    ------------------------------*/
    .badge {
        display: inline-block;
        background: rgba(37, 99, 235, 0.2);
        color: #93C5FD;
        border: 1px solid rgba(59, 130, 246, 0.4);
        padding: 6px 14px;
        border-radius: 20px;
        margin: 4px;
        font-weight: 600;
        font-size: 14px;
    }
    .badge-matched {
        background: rgba(16, 185, 129, 0.15);
        color: #6EE7B7;
        border: 1px solid rgba(16, 185, 129, 0.4);
        padding: 6px 14px;
        border-radius: 20px;
        margin: 4px;
        font-weight: 600;
        font-size: 14px;
        display: inline-block;
    }
    .badge-missing {
        background: rgba(245, 158, 11, 0.15);
        color: #FCD34D;
        border: 1px solid rgba(245, 158, 11, 0.4);
        padding: 6px 14px;
        border-radius: 20px;
        margin: 4px;
        font-weight: 600;
        font-size: 14px;
        display: inline-block;
    }

    /* -----------------------------
       Footer
    ------------------------------*/
    .footer {
        text-align: center;
        color: #64748B;
        margin-top: 40px;
        padding: 20px;
        font-size: 14px;
    }
    </style>
    """, unsafe_allow_html=True)
