import streamlit as st

# 1. Configuração da página (Mobile-First)
st.set_page_config(
    page_title="MapCompra 🛒",
    page_icon="🛒",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# 2. CSS Personalizado (Layout Smartphone + Cores Varejo)
st.markdown("""
    <style>
    .stApp { background-color: #F0F2F5; }
    
    .block-container {
        max-width: 420px !important;
        background-color: #FFFFFF;
        padding: 2rem 1.5rem;
        border-radius: 24px;
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.12);
        margin-top: 3rem;
        margin-bottom: 3rem;
    }
    
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    .main-title {
        color: #E53935;
        font-size: 1.8rem;
        font-weight: 800;
        text-align: center;
        margin-bottom: 0px;
    }
    
    .sub-title {
        color: #666666;
        font-size: 0.95rem;
        text-align: center;
        margin-bottom: 20px;
    }

    .card-box {
        background-color: #FFFFFF;
        border: 1px solid #EEEEEE;
        border-radius: 12px;
        padding: 16px;
        box-shadow: 0px 2px 8px rgba(0, 0, 0, 0.04);
        margin-bottom: 12px;
    }
    
    div.stButton > button:first-child {
        background: linear-gradient(90deg, #FF6F00, #E53935);
        color: white;
        font-weight: bold;
        font-size: 1rem;
        border: none;
        border-radius: 10px;
        padding: 10px 20px;
        width: 100%;
        box-shadow: 0 4px 10px rgba(229, 57, 53, 0.3);
        transition: all 0.3s ease;
    }
    
    div.stButton > button:first-child:hover {
        background: linear-gradient(90deg, #E53935, #D32F2F);
        color: white;
    }

    .badge-orange {
        background-color: #FFF3E0;
        color: #E65100;
        font-weight: bold;
        padding: 3px 10px;
        border-radius: 20px;
        font-size: 0.8rem;
        display: inline-block;
        margin-bottom: 6px;
    }
    
    .price-tag {
        font-size: 1.2rem;
        font-weight: 800;
        color: #2E7D32;
    }
    
    .address-text {
        color: #555555;
        font-size: 0.82rem;
        margin-top: 4px;
        margin-bottom: 6px;
    }

    .info-pagamento {
        font-size: 0.78rem;
        color: #555555;
        margin-top: 6px;
        background-color: #FAFAFA;
        padding: 6px 10px;
        border-radius: 6px;
        border-left: 3px solid #FF6F00;
    }
    </style>
""", unsafe_allow_html=True)

# 3. Base de Dados Simulada (Unidades Reais da Zona Norte de SP)
LOJAS_ZN_DATABASE = [
    {
        "nome": "Supermercado Bergamini",
        "endereco": "Av. Luis Stamatis, 431 - Jaçanã",
        "distancia_km": 2.5,
        "preco_cesta": 278.90,
    },
    {
        "nome": "Assaí Atacadista",
        "endereco": "Av. Senador José Ermírio de Moraes, 100 - Jaçanã",
        "distancia_km": 1.8,
        "preco_cesta": 281.50,
    },
    {
        "nome": "Giga Atacado",
        "endereco": "Av. Nova Cantareira, 5300 - Tremembé",
        "distancia_km": 3.9,
        "preco_cesta": 285.00,
    },
    {
        "nome": "Atacadão",
        "endereco": "Av. Otaviano Alves de Lima, 1828 - Limão",
        "distancia_km": 5.4,
        "preco_cesta": 289.90,
    },
    {
        "nome": "Sonda Supermercados",
        "endereco": "R. Voluntários da Pátria, 3530 - Santana",
        "distancia_km": 6.2,
        "preco_cesta": 312.00,
    },
    {
        "nome": "Tenda Atacado",
        "endereco": "Av. Inajar de Sousa, 3500 - Limão",
        "distancia_km": 7.8,
        "preco_cesta": 295.00,
    }
]

# 4. Estado da Sessão
if 'step' not in st.session_state:
    st.session_state.step = 'onboarding'
if 'user_income' not in st.session_state:
    st.session_state.user_income = None
if 'basket_type' not in st.session_state:
    st.session_state.basket_type = None
if 'user_cep' not in st.session_state:
    st.session_state.user_cep = "02300-000"
if 'search_radius' not in st.session_state:
    st.session_state.search_radius = 5

# ==========================================
# TELA 1: ONBOARDING & LOGIN
# ==========================================
if st.session_state.step == 'onboarding':
    st.markdown('<div class="main-title">MapCompra 🛒📍</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-title">Sua cesta básica pelo menor preço, nos atacarejos mais próximos.</div>', unsafe_allow_html=True)
    
    st.markdown("""
        <div style="text-align: center; margin: 20px 0;">
            <span style="font-size: 3.5rem;">🏬📍✨</span>
        </div>
    """, unsafe_allow_html=True)
    
    if st.button("🌐 Entrar com Google"):
        st.session_state.step = 'income'
        st.rerun()

    if st.button("🍎 Entrar com Apple"):
        st.session_state.step = 'income'
        st.rerun()

    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("Continuar sem Login (Convidado)"):
        st.session_state.step = 'income'
        st.rerun()

# ==========================================
# TELA 2: CAPTURA DE RENDA (OPCIONAL)
# ==========================================
elif st.session_state.step == 'income':
    st.markdown('<div class="main-title">Perfil Rápido 📊</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-title">Qual a sua faixa de renda mensal? (100% anónimo)</div>', unsafe_allow_html=True)
    
    st.markdown('<div class="card-box">', unsafe_allow_html=True)
    income_option = st.radio(
        "Selecione uma opção:",
        [
            "Até 2 salários mínimos (Até R$ 3.000)",
            "De 2 a 4 salários mínimos (R$ 3.000 - R$ 6.000)",
            "De 4 a 7 salários mínimos (R$ 6.000 - R$ 10.000)",
            "Acima de 7 salários mínimos (Acima de R$ 10.000)",
            "Prefiro não informar"
        ],
        index=4
    )
    st.markdown('</div>', unsafe_allow_html=True)
    
    if st.button("Avançar para Escolha de Cesta ➔"):
        st.session_state.user_income = income_option
        st.session_state.step = 'basket_selection'
        st.rerun()

# ==========================================
# TELA 3: SELEÇÃO DO TIPO DE CESTA
# ==========================================
elif st.session_state.step == 'basket_selection':
    st.markdown('<div class="main-title">Simulador de Cesta 🛍️</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-title">Como prefere montar a sua compra hoje?</div>', unsafe_allow_html=True)
    
    st.markdown("""
        <div class="card-box">
            <span class="badge-orange">🇧🇷 Padrão Oficial do Governo</span>
            <h4 style="margin: 5px 0; color: #E53935;">Cesta Básica Nacional (13 Itens)</h4>
            <p style="color: #666; font-size: 0.85rem;">Arroz, feijão, carne, óleo, leite, café, açúcar, pão, farinha, macarrão, tomate, batata e manteiga.</p>
        </div>
    """, unsafe_allow_html=True)
    
    if st.button("Selecionar Cesta Oficial"):
        st.session_state.basket_type = 'oficial'
        st.session_state.step = 'location_setup'
        st.rerun()

    st.markdown("<br>", unsafe_allow_html=True)

    st.markdown("""
        <div class="card-box">
            <span class="badge-orange">⚙️ 100% Customizável</span>
            <h4 style="margin: 5px 0; color: #E53935;">Cesta Personalizada</h4>
            <p style="color: #66
