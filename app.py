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
        font-size: 0.9rem;
        border: none;
        border-radius: 10px;
        padding: 10px 10px;
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

# 3. Base de Dados Simulada (Unidades Reais da ZN-SP)
LOJAS_ZN_DATABASE = [
    {
        "nome": "Supermercado Bergamini",
        "endereco": "Av. Luis Stamatis, 431 - Jaçanã",
        "distancia_km": 2.5,
        "preco_cesta": 278.90,
        "fator_custom": 1.00
    },
    {
        "nome": "Assaí Atacadista",
        "endereco": "Av. Senador José Ermírio de Moraes, 100 - Jaçanã",
        "distancia_km": 1.8,
        "preco_cesta": 281.50,
        "fator_custom": 0.98
    },
    {
        "nome": "Giga Atacado",
        "endereco": "Av. Nova Cantareira, 5300 - Tremembé",
        "distancia_km": 3.9,
        "preco_cesta": 285.00,
        "fator_custom": 1.02
    },
    {
        "nome": "Atacadão",
        "endereco": "Av. Otaviano Alves de Lima, 1828 - Limão",
        "distancia_km": 5.4,
        "preco_cesta": 289.90,
        "fator_custom": 0.96
    },
    {
        "nome": "Sonda Supermercados",
        "endereco": "R. Voluntários da Pátria, 3530 - Santana",
        "distancia_km": 6.2,
        "preco_cesta": 312.00,
        "fator_custom": 1.10
    },
    {
        "nome": "Tenda Atacado",
        "endereco": "Av. Inajar de Sousa, 3500 - Limão",
        "distancia_km": 7.8,
        "preco_cesta": 295.00,
        "fator_custom": 0.99
    }
]

ITENS_CESTA_OFICIAL = [
    "🍚 Arroz (5 kg)",
    "🫘 Feijão (4,5 kg)",
    "🥩 Carne bovina (4,5 kg)",
    "🥖 Pão francês (6 kg)",
    "🥛 Leite longa vida (6 L)",
    "🍅 Tomate (3 kg)",
    "🥔 Batata (6 kg)",
    "🍌 Banana (1,3 kg / 1 dúzia)",
    "☕ Café em pó (500 g)",
    "🌾 Farinha de trigo (1,5 kg)",
    "🧈 Manteiga/Margarina (750 g)",
    "🍬 Açúcar cristal (3 kg)",
    "🛢️ Óleo de soja (900 ml)"
]

CATALOGO_ESTENDIDO = {
    "Mercearia Básica": [
        {
            "id": "arroz",
            "nome": "Arroz Tipo 1",
            "variacoes": {
                "Pacote 1kg": 6.50,
                "Pacote 5kg": 28.90
            }
        },
        {
            "id": "feijao",
            "nome": "Feijão Carioca",
            "variacoes": {
                "Pacote 1kg": 8.50,
                "Pacote 2kg": 16.20
            }
        },
        {
            "id": "oleo",
            "nome": "Óleo de Soja",
            "variacoes": {
                "Garrafa 900ml": 6.80
            }
        },
        {
            "id": "acucar",
            "nome": "Açúcar Refinado",
            "variacoes": {
                "Pacote 1kg": 4.50,
                "Pacote 5kg": 21.00
            }
        },
        {
            "id": "cafe",
            "nome": "Café Torrado e Moído",
            "variacoes": {
                "Embalagem 250g": 9.90,
                "Embalagem 500g": 18.90
            }
        },
        {
            "id": "macarrao",
            "nome": "Macarrão Esparguete",
            "variacoes": {
                "Pacote 500g": 4.20,
                "Pacote 1kg": 7.90
            }
        }
    ],
    "Limpeza": [
        {
            "id": "sabao_em_po",
            "nome": "Sabão em Pó",
            "variacoes": {
                "Caixa 800g": 11.90,
                "Caixa 1,6kg": 22.50,
                "Saco 3kg": 39.90
            }
        },
        {
            "id": "detergente",
            "nome": "Detergente Líquido",
            "variacoes": {
                "Frasco 500ml": 2.60
            }
        },
        {
            "id": "amaciante",
            "nome": "Amaciante Concentrado",
            "variacoes": {
                "Frasco 500ml": 9.50,
                "Frasco 1.5L": 24.90
            }
        },
        {
            "id": "papel_higienico",
            "nome": "Papel Higiénico",
            "variacoes": {
                "Pacote 4 rolos": 7.50,
                "Pacote 12 rolos": 19.90,
                "Pacote 24 rolos": 36.90
            }
        }
    ],
    "Higiene Pessoal": [
        {
            "id": "sabonete",
            "nome": "Sabonete em Barra",
            "variacoes": {
                "Unidade 85g": 2.50,
                "Pack 6 unidades": 13.50
            }
        },
        {
            "id": "creme_dental",
            "nome": "Creme Dental",
            "variacoes": {
                "Tubo 70g": 3.90,
                "Tubo 90g": 4.90,
                "Pack Triplo (3x90g)": 12.90
            }
        }
    ]
}

# 4. Estado da Sessão
if 'step' not in st.session_state:
    st.session_state.step = 'onboarding'
if 'user_income' not in st.session_state:
    st.session_state.user_income = None
if 'basket_type' not in st.session_state:
    st.session_state.basket_type = None
if 'custom_basket' not in st.session_state:
    st.session_state.custom_basket = {}
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
    
    if st.button("Avançar para Localização ➔"):
        st.session_state.user_income = income_option
        st.session_state.step = 'location_setup'
        st.rerun()

# ==========================================
# TELA 3: CONFIGURAÇÃO DE LOCALIZAÇÃO E RAIO
# ==========================================
elif st.session_state.step == 'location_setup':
    st.markdown('<div class="main-title">Onde você está? 📍</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-title">Defina o seu CEP e a distância máxima para a busca.</div>', unsafe_allow_html=True)
    
    st.markdown('<div class="card-box">', unsafe_allow_html=True)
    cep_input = st.text_input("Digite seu CEP ou Bairro:", value=st.session_state.user_cep)
    
    radius_input = st.slider(
        "Raio máximo de distância (km):",
        min_value=1,
        max_value=20,
        value=st.session_state.search_radius,
        step=1
    )
    st.markdown('</div>', unsafe_allow_html=True)
    
    if st.button("Continuar para Escolha de Cesta ➔"):
        st.session_state.user_cep = cep_input
        st.session_state.search_radius = radius_input
        st.session_state.step = 'basket_selection'
        st.rerun()
        
    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("⬅️ Voltar"):
        st.session_state.step = 'income'
        st.rerun()

# ==========================================
# TELA 4: SELEÇÃO DO TIPO DE CESTA
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
    
    if st.button("Selecionar Cesta Oficial (DIEESE)"):
        st.session_state.basket_type = 'oficial'
        st.session_state.step = 'results'
        st.rerun()

    st.markdown("<br>", unsafe_allow_html=True)

    st.markdown("""
        <div class="card-box">
            <span class="badge-orange">⚙️ 100% Customizável</span>
            <h4 style="margin: 5px 0; color: #E53935;">Cesta Personalizada</h4>
            <p style="color: #666; font-size: 0.85rem;">Escolha itens e tamanhos no catálogo estendido (Limpeza, Higiene e mais).</p>
        </div>
    """, unsafe_allow_html=True)
    
    if st.button("Montar Cesta Customizada"):
        st.session_state.basket_type = 'custom'
        if not st.session_state.custom_basket:
            st.session_state.custom_basket = {}
        st.session_state.step = 'custom_builder'
        st.rerun()

    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("⬅️ Voltar"):
        st.session_state.step = 'location_setup'
        st.rerun()

# ==========================================
# TELA 5: MONTAGEM DA CESTA COMPACTA (CUSTOMIZADA)
# ==========================================
elif st.session_state.step == 'custom_builder':
    st.markdown('<div class="main-title">Monte sua Cesta 🛒</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-title">Escolha a opção de peso/tamanho e a quantidade:</div>', unsafe_allow_html=True)

    categorias = list(CATALOGO_ESTENDIDO.keys())
    tabs = st.tabs(categorias)

    for i, cat in enumerate(categorias):
        with tabs[i]:
            for prod in CATALOGO_ESTENDIDO[cat]:
                p_id = prod["id"]
                p_nome = prod["nome"]
                lista_pesos = list(prod["variacoes"].keys())
                
                col_nome, col_peso, col_qtd = st.columns([2.2, 2.0, 1.5])
                
                with col_nome:
                    st.markdown(f"**{p_nome}**")
                
                with col_peso:
                    peso_sel = st.selectbox(
                        "Opção",
                        options=lista_pesos,
                        key=f"sel_{p_id}",
                        label_visibility="collapsed"
                    )
                    preco_sel = prod["variacoes"][peso_sel]
                    st.caption(f"R$ {preco_sel:.2f}")

                with col_qtd:
                    key_item = f"{p_id}_{peso_sel}"
                    qtd_existente = 0
                    if key_item in st.session_state.custom_basket and isinstance(st.session_state.custom_basket[key_item], dict):
                        qtd_existente = st.session_state.custom_basket[key_item].get("qtd", 0)
                    
                    nova_qtd = st.number_input(
                        "Qtd",
                        min_value=0,
                        max_value=20,
                        value=qtd_existente,
                        key=f"qtd_{key_item}",
                        label_visibility="collapsed"
                    )

                    if nova_qtd > 0:
                        st.session_state.custom_basket[key_item] = {
                            "nome": f"{p_nome} ({peso_sel})",
                            "qtd": nova_qtd,
                            "preco_un": preco_sel
                        }
                    elif key_item in st.session_state.custom_basket:
                        del st.session_state.custom_basket[key_item]
                        
                st.markdown("<hr style='margin: 8px 0; border-top: 1px solid #f0f0f0;'>", unsafe_allow_html=True)

    total_itens = 0
    for v in st.session_state.custom_basket.values():
        if isinstance(v, dict) and "qtd" in v:
            total_itens += v["qtd"]

    st.markdown(f"**Total de pacotes/unidades:** `{total_itens}`")

    if total_itens > 0:
        if st.button("Ver Comparativo de Preços ➔"):
            st.session_state.step = 'results'
            st.rerun()
    else:
        st.info("Adicione pelo menos 1 item para continuar.")

    if st.button("⬅️ Voltar"):
        st.session_state.step = 'basket_selection'
        st.rerun()

# ==========================================
# TELA 6: RESULTADOS E COMPARAÇÃO DINÂMICA
# ==========================================
elif st.session_state.step == 'results':
    st.markdown('<div class="main-title">Comparativo Dinâmico 📍</div>', unsafe_allow_html=True)
    
    sub_text = f"Lojas num raio de até <strong>{st.session_state.search_radius} km</strong> (Ref: {st.session_state.user_cep})"
    st.markdown(f'<div class="sub-title">{sub_text}</div>', unsafe_allow_html=True)

    if st.session_state.basket_type == 'oficial':
        with st.expander("📋 Ver 13 itens inclusos nesta Cesta Padrão (DIEESE)"):
            for item in ITENS_CESTA_OFICIAL:
                st.markdown(f"- {item}")
    else:
        with st.expander("📋 Ver produtos e pesos selecionados na sua Cesta Customizada"):
            for item_data in st.session_state.custom_basket.values():
                if isinstance(item_data, dict) and "nome" in item_data:
                    st.markdown(f"- {item_data['nome']} x {item_data['qtd']}")
    
    st.markdown("<br>", unsafe_allow_html=True)

    lojas_filtradas = [loja for loja in LOJAS_ZN_DATABASE if loja["distancia_km"] <= st.session_state.search_radius]

    if st.session_state.basket_type == 'custom':
        valor_base_custom = sum(
            item["preco_un"] * item["qtd"] 
            for item in st.session_state.custom_basket.values() 
            if isinstance(item, dict) and "preco_un" in item
        )

        for loja in lojas_filtradas:
            loja["preco_exibido"] = valor_base_custom * loja["fator_custom"]
    else:
        for loja in lojas_filtradas:
            loja["preco_exibido"] = loja["preco_cesta"]
    
    lojas_filtradas = sorted(lojas_filtradas, key=lambda x: x["preco_exibido"])
    
    if not lojas_filtradas:
        st.warning(f"⚠️ Nenhuma unidade encontrada neste raio de {st.session_state.search_radius} km. Tente alterar o raio ou o CEP abaixo.")
    else:
        vencedor = lojas_filtradas[0]
        demais_lojas = lojas_filtradas[1:]
        
        card_vencedor_html = (
            f'<div class="card-box" style="border: 2px solid #2E7D32; background-color: #F1F8E9;">'
            f'<span class="badge-orange" style="background-color: #C8E6C9; color: #2E7D32;">🏆 Menor Preço Total</span>'
            f'<h3 style="margin: 5px 0; color: #1B5E20;">🛒 {vencedor["nome"]}</h3>'
            f'<div class="address-text">📍 {vencedor["endereco"]} ({vencedor["distancia_km"]} km)</div>'
            f'<div class="price-tag" style="margin-bottom: 6px;">R$ {vencedor["preco_exibido"]:.2f}</div>'
            f'<div class="info-pagamento">💳🎫 Consulte formas de pagamento com a rede ({vencedor["nome"]}).</div>'
            f'</div>'
        )
        st.markdown(card_vencedor_html, unsafe_allow_html=True)

        if demais_lojas:
            st.markdown("---")
            st.markdown("#### Demais Opções Disponíveis na Região:")
            
            for loja in demais_lojas:
                card_loja_html = (
                    f'<div class="card-box">'
                    f'<strong>🛒 {loja["nome"]}</strong><br>'
                    f'<div class="address-text">📍 {loja["endereco"]} ({loja["distancia_km"]} km)</div>'
                    f'<span style="color: #E53935; font-weight: bold; font-size: 1.05rem;">R$ {loja["preco_exibido"]:.2f}</span><br>'
                    f'<div class="info-pagamento">💳🎫 Consulte formas de pagamento com a rede ({loja["nome"]}).</div>'
                    f'</div>'
                )
                st.markdown(card_loja_html, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    
    # Botões lado a lado para Alterar CEP / Raio ou Alterar Cesta
    col_btn1, col_btn2 = st.columns(2)
    
    with col_btn1:
        if st.button("📍 Alterar CEP/Raio"):
            st.session_state.step = 'location_setup'
            st.rerun()
            
    with col_btn2:
        if st.button("🛒 Alterar Cesta"):
            st.session_state.step = 'basket_selection'
            st.rerun()
