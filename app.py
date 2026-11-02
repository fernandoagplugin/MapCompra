import streamlit as st

# 1. Configuração da página (Mobile-First)
st.set_page_config(
    page_title="MapCompra 🛒",
    page_icon="🛒",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# 2. CSS Personalizado (Fundo Branco, Detalhes em Vermelho Varejo e Laranja Ação)
st.markdown("""
    <style>
    /* Fundo Branco e Texto Grafite */
    .stApp {
        background-color: #FFFFFF;
        color: #1A1A1A;
    }
    
    /* Esconder menu superior e footer do Streamlit para parecer App Nativo */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* Estilo dos Títulos */
    .main-title {
        color: #E53935;
        font-size: 2.2rem;
        font-weight: 800;
        text-align: center;
        margin-bottom: 0px;
    }
    
    .sub-title {
        color: #555555;
        font-size: 1rem;
        text-align: center;
        margin-bottom: 25px;
    }

    /* Cards e Containers Brancos com Borda Suave */
    .card-box {
        background-color: #FFFFFF;
        border: 1px solid #EEEEEE;
        border-radius: 12px;
        padding: 20px;
        box-shadow: 0px 4px 12px rgba(0, 0, 0, 0.05);
        margin-bottom: 15px;
    }
    
    /* Botões Principais em Laranja Quente com Hover em Vermelho */
    div.stButton > button:first-child {
        background: linear-gradient(90deg, #FF6F00, #E53935);
        color: white;
        font-weight: bold;
        font-size: 1.05rem;
        border: none;
        border-radius: 10px;
        padding: 12px 24px;
        width: 100%;
        box-shadow: 0 4px 10px rgba(229, 57, 53, 0.3);
        transition: all 0.3s ease;
    }
    
    div.stButton > button:first-child:hover {
        background: linear-gradient(90deg, #E53935, #D32F2F);
        box-shadow: 0 6px 15px rgba(211, 47, 47, 0.4);
        color: white;
    }

    /* Botão Secundário / Pular */
    .secondary-btn button {
        background: transparent !important;
        color: #757575 !important;
        border: 1px solid #E0E0E0 !important;
        box-shadow: none !important;
    }

    /* Badges de Destaque em Laranja */
    .badge-orange {
        background-color: #FFF3E0;
        color: #E65100;
        font-weight: bold;
        padding: 4px 12px;
        border-radius: 20px;
        font-size: 0.85rem;
        display: inline-block;
        margin-bottom: 8px;
    }
    </style>
""", unsafe_allow_html=True)

# 3. Inicialização de Estado da Sessão (Navegação)
if 'step' not in st.session_state:
    st.session_state.step = 'onboarding'
if 'user_income' not in st.session_state:
    st.session_state.user_income = None
if 'basket_type' not in st.session_state:
    st.session_state.basket_type = None

# ==========================================
# TELA 1: ONBOARDING & LOGIN
# ==========================================
if st.session_state.step == 'onboarding':
    st.markdown('<div class="main-title">MapCompra 🛒📍</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-title">Sua cesta básica pelo menor preço, nos atacarejos mais próximos.</div>', unsafe_allow_html=True)
    
    st.markdown("""
        <div style="text-align: center; margin: 30px 0;">
            <span style="font-size: 4rem;">🏬📍✨</span>
        </div>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("🌐 Entrar com Google"):
            st.session_state.step = 'income'
            st.rerun()
    with col2:
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
        "Selecione uma opção para nos ajudar a calcular a melhor economia para o seu perfil:",
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
    
    # Opção 1: Cesta Padrão
    st.markdown("""
        <div class="card-box">
            <span class="badge-orange">⚡ Rápido em 1-Clique</span>
            <h3 style="margin: 5px 0; color: #E53935;">Cesta Básica Padrão</h3>
            <p style="color: #666; font-size: 0.9rem;">Calculada com os 13 itens essenciais de alimentação para uma família (Arroz, Feijão, Óleo, Leite, Café, Açúcar, etc.).</p>
        </div>
    """, unsafe_allow_html=True)
    if st.button("Simular Cesta Padrão Agora"):
        st.session_state.basket_type = 'padrao'
        st.success("Cesta Padrão Selecionada! Redirecionando para o mapa...")

    st.markdown("<br>", unsafe_allow_html=True)

    # Opção 2: Cesta Personalizada
    st.markdown("""
        <div class="card-box">
            <span class="badge-orange">⚙️ 100% Customizável</span>
            <h3 style="margin: 5px 0; color: #E53935;">Cesta Personalizada</h3>
            <p style="color: #666; font-size: 0.9rem;">Escolha as quantidades e itens do nosso catálogo mestre de 50 produtos (Limpeza, Carnes, Hortifruti e Mercearia).</p>
        </div>
    """, unsafe_allow_html=True)
    if st.button("Montar Minha Cesta Customizada"):
        st.session_state.basket_type = 'custom'
        st.info("Em breve: Catálogo de 50 itens!")
