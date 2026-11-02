import streamlit as st

# 1. Configuração da página (Mobile-First)
st.set_page_config(
    page_title="MapCompra 🛒",
    page_icon="🛒",
    layout="centered",
    initial_sidebar_state="collapsed",
)

# 2. CSS Personalizado (Simulador de Tela Mobile + Fundo Branco/Vermelho/Laranja)
st.markdown(
    """
    <style>
    /* Fundo geral da tela no desktop (cinza suave para destacar o "celular") */
    .stApp {
        background-color: #F0F2F5;
    }
    
    /* Container principal simulando a tela de um smartphone */
    .block-container {
        max-width: 420px !important;
        background-color: #FFFFFF;
        padding: 2rem 1.5rem;
        border-radius: 24px;
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.12);
        margin-top: 3rem;
        margin-bottom: 3rem;
    }
    
    /* Esconder elementos padrão do Streamlit */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* Títulos */
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

    /* Cards e Containers Brancos */
    .card-box {
        background-color: #FFFFFF;
        border: 1px solid #EEEEEE;
        border-radius: 12px;
        padding: 16px;
        box-shadow: 0px 2px 8px rgba(0, 0, 0, 0.04);
        margin-bottom: 12px;
    }
    
    /* Botões Principais (Gradiente Laranja para Vermelho) */
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

    /* Badge Laranja */
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
    </style>
""",
    unsafe_allow_html=True,
)

# 3. Estado da Sessão
if "step" not in st.session_state:
  st.session_state.step = "onboarding"
if "user_income" not in st.session_state:
  st.session_state.user_income = None
if "basket_type" not in st.session_state:
  st.session_state.basket_type = None

# ==========================================
# TELA 1: ONBOARDING & LOGIN
# ==========================================
if st.session_state.step == "onboarding":
  st.markdown(
      '<div class="main-title">MapCompra 🛒📍</div>', unsafe_allow_html=True
  )
  st.markdown(
      '<div class="sub-title">Sua cesta básica pelo menor preço, nos'
      " atacarejos mais próximos.</div>",
      unsafe_allow_html=True,
  )

  st.markdown(
      """
        <div style="text-align: center; margin: 20px 0;">
            <span style="font-size: 3.5rem;">🏬📍✨</span>
        </div>
    """,
      unsafe_allow_html=True,
  )

  if st.button("🌐 Entrar com Google"):
    st.session_state.step = "income"
    st.rerun()

  if st.button("🍎 Entrar com Apple"):
    st.session_state.step = "income"
    st.rerun()

  st.markdown("<br>", unsafe_allow_html=True)
  if st.button("Continuar sem Login (Convidado)"):
    st.session_state.step = "income"
    st.rerun()

# ==========================================
# TELA 2: CAPTURA DE RENDA (OPCIONAL)
# ==========================================
elif st.session_state.step == "income":
  st.markdown(
      '<div class="main-title">Perfil Rápido 📊</div>', unsafe_allow_html=True
  )
  st.markdown(
      '<div class="sub-title">Qual a sua faixa de renda mensal? (100%'
      " anónimo)</div>",
      unsafe_allow_html=True,
  )

  st.markdown('<div class="card-box">', unsafe_allow_html=True)
  income_option = st.radio(
      "Selecione uma opção:",
      [
          "Até 2 salários mínimos (Até R$ 3.000)",
          "De 2 a 4 salários mínimos (R$ 3.000 - R$ 6.000)",
          "De 4 a 7 salários mínimos (R$ 6.000 - R$ 10.000)",
          "Acima de 7 salários mínimos (Acima de R$ 10.000)",
          "Prefiro não informar",
      ],
      index=4,
  )
  st.markdown("</div>", unsafe_allow_html=True)

  if st.button("Avançar para Escolha de Cesta ➔"):
    st.session_state.user_income = income_option
    st.session_state.step = "basket_selection"
    st.rerun()

# ==========================================
# TELA 3: SELEÇÃO DO TIPO DE CESTA
# ==========================================
elif st.session_state.step == "basket_selection":
  st.markdown(
      '<div class="main-title">Simulador de Cesta 🛍️</div>',
      unsafe_allow_html=True,
  )
  st.markdown(
      '<div class="sub-title">Como prefere montar a sua compra hoje?</div>',
      unsafe_allow_html=True,
  )

  st.markdown(
      """
        <div class="card-box">
            <span class="badge-orange">⚡ Rápido em 1-Clique</span>
            <h4 style="margin: 5px 0; color: #E53935;">Cesta Básica Padrão</h4>
            <p style="color: #666; font-size: 0.85rem;">13 itens essenciais de alimentação para a família.</p>
        </div>
    """,
      unsafe_allow_html=True,
  )
  if st.button("Simular Cesta Padrão"):
    st.session_state.basket_type = "padrao"
    st.success("Redirecionando para o mapa...")

  st.markdown("<br>", unsafe_allow_html=True)

  st.markdown(
      """
        <div class="card-box">
            <span class="badge-orange">⚙️ 100% Customizável</span>
            <h4 style="margin: 5px 0; color: #E53935;">Cesta Personalizada</h4>
            <p style="color: #666; font-size: 0.85rem;">Escolha itens do catálogo de 50 produtos (Limpeza, Carnes, etc.).</p>
        </div>
    """,
      unsafe_allow_html=True,
  )
  if st.button("Montar Cesta Customizada"):
    st.session_state.basket_type = "custom"
    st.info("Em breve: Catálogo de 50 itens!")
