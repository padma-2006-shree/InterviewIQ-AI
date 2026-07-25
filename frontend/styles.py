import streamlit as st

def load_css():

    st.markdown("""
    <style>

    /* -----------------------------
       Background
    ------------------------------*/

    .stApp{
        background: linear-gradient(
            135deg,
            #0B1120 0%,
            #111827 40%,
            #1E293B 100%
        );
        color:white;
    }

    .main .block-container{
        padding-top:2rem;
        padding-bottom:2rem;
        max-width:1250px;
    }

    /* -----------------------------
       Scrollbar
    ------------------------------*/

    ::-webkit-scrollbar{
        width:10px;
    }

    ::-webkit-scrollbar-thumb{
        background:#3B82F6;
        border-radius:10px;
    }

    /* -----------------------------
       Titles
    ------------------------------*/

    h1{
        color:white;
        font-size:52px;
        font-weight:800;
    }

    h2{
        color:white;
        font-weight:700;
    }

    h3{
        color:#E5E7EB;
    }

    p,label{
        color:#CBD5E1;
    }

    /* -----------------------------
       Upload Box
    ------------------------------*/

    [data-testid="stFileUploader"]{

        background:rgba(255,255,255,.05);

        border:2px dashed #3B82F6;

        border-radius:18px;

        padding:25px;

        backdrop-filter:blur(15px);

    }

    /* -----------------------------
       Buttons
    ------------------------------*/

    .stButton>button{

        width:100%;

        background:linear-gradient(
            90deg,
            #2563EB,
            #3B82F6
        );

        color:white;

        border:none;

        border-radius:12px;

        padding:12px;

        font-weight:700;

        transition:.3s;

    }

    .stButton>button:hover{

        transform:translateY(-2px);

        box-shadow:0 0 20px #2563EB;

    }

    /* -----------------------------
       Cards
    ------------------------------*/

    .glass{

        background:rgba(255,255,255,.06);

        backdrop-filter:blur(18px);

        border:1px solid rgba(255,255,255,.08);

        border-radius:20px;

        padding:25px;

        box-shadow:0 0 25px rgba(0,0,0,.3);

        margin-bottom:20px;

    }

    /* -----------------------------
       Metric
    ------------------------------*/

    [data-testid="metric-container"]{

        background:rgba(255,255,255,.06);

        border-radius:18px;

        padding:20px;

        border:1px solid rgba(255,255,255,.08);

    }

    /* -----------------------------
       Success
    ------------------------------*/

    .stSuccess{

        border-radius:12px;

    }

    .stWarning{

        border-radius:12px;

    }

    .stInfo{

        border-radius:12px;

    }

    /* -----------------------------
       Hero
    ------------------------------*/

    .hero{

        padding:40px;

        border-radius:25px;

        background:linear-gradient(
            135deg,
            rgba(37,99,235,.18),
            rgba(17,24,39,.7)
        );

        border:1px solid rgba(255,255,255,.08);

        margin-bottom:30px;

    }

    .hero-title{

        font-size:58px;

        font-weight:800;

        color:white;

        line-height:1.1;

    }

    .hero-sub{

        color:#CBD5E1;

        font-size:18px;

        margin-top:15px;

    }

    .highlight{

        color:#FACC15;

    }

    /* -----------------------------
       Skill Badge
    ------------------------------*/

    .badge{

        display:inline-block;

        background:#1D4ED8;

        color:white;

        padding:10px 18px;

        border-radius:30px;

        margin:6px;

        font-weight:600;

        font-size:15px;

    }

    /* -----------------------------
       Footer
    ------------------------------*/

    .footer{

        text-align:center;

        color:#94A3B8;

        margin-top:50px;

        padding:20px;

    }

    </style>
    """, unsafe_allow_html=True)