import streamlit as st
import requests
import math

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

# 3. Base de Dados Oficial com Unidades e Endereços Reais Fixos (Com Coordenadas para Cálculo Haversine)
REDES_SUPERMERCADOS_REAIS = [
    {
        "nome": "Supermercado Bergamini",
        "endereco": "Av. Luis Stamatis, 431 - Jaçanã, São Paulo - SP",
        "lat": -23.4682,
        "lon": -46.5741,
        "preco_base_fator": 1.00
    },
    {
        "nome": "Assaí Atacadista",
        "endereco": "Av. Senador José Ermírio de Moraes, 100 - Jaçanã, São Paulo - SP",
        "lat": -23.4721,
        "lon": -46.5802,
        "preco_base_fator": 0.98
    },
    {
        "nome": "Giga Atacado",
        "endereco": "Av. Nova Cantareira, 5300 - Tremembé, São Paulo - SP",
        "lat": -23.4610,
        "lon": -46.6045,
        "preco_base_fator": 1.02
    },
    {
        "nome": "Atacadão",
        "endereco": "Av. Otaviano Alves de Lima, 1828 - Limão, São Paulo - SP",
        "lat": -23.5125,
        "lon": -46.6710,
        "preco_base_fator": 0.96
    },
    {
        "nome": "Sonda Supermercados",
        "endereco": "R. Voluntários da Pátria, 3530 - Santana, São Paulo - SP",
        "lat": -23.4980,
        "lon": -46.6255,
        "preco_base_fator": 1.10
    },
    {
        "nome": "Tenda Atacado",
        "endereco": "Av. Inajar de Sousa, 3500 - Limão, São Paulo - SP",
        "lat": -23.4920,
        "lon": -46.6820,
        "preco_base_fator": 0.99
    }
]

# Funções de Apoio Geográfico (ViaCEP + Nominatim + Haversine)
@st.cache_data(show_spinner=False)
def consultar_viacep(cep_string):
    cep_limpo = "".join(filter(str.isdigit, str(cep_string)))
    if len(cep_limpo) != 8:
        return None
    try:
        url = f"https://viacep.com.br/ws/{cep_limpo}/json/"
        response = requests.get(url, timeout=3)
        if response.status_code == 200:
            data = response.json()
            if "erro" not in data:
                return data
    except Exception:
        pass
    return None

@st.cache_data(show_spinner=False)
def obter_coordenadas(cep_string):
    cep_limpo = "".join(filter(str.isdigit, str(cep_string)))
    try:
        url = f"https://nominatim.openstreetmap.org/search?postalcode={cep_limpo}&country=Brazil&format=json"
        headers = {'User-Agent': 'MapCompraApp/1.0'}
        response = requests.get(url, headers=headers, timeout=4)
        if response.status_code == 200:
            data = response.json()
            if data:
                return float(data[0]['lat']), float(data[0]['lon'])
    except Exception:
        pass
    return None, None

def calcular_distancia_haversine(lat1, lon1, lat2, lon2):
    R = 6371.0
    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)
    a = math.sin(dlat / 2)**2 + math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * math.sin(dlon / 2)**2
    c = 2 * math.asin(math.sqrt(a))
    return R * c

def gerar_lojas_com_distancia_real(cep, raio_busca):
    dados_cep = consultar_viacep(cep)
    lat_user, lon_user = obter_coordenadas(cep)
    
    # Se não achar coordenadas exatas pelo CEP, usa coordenadas padrão de referência em SP
    if not lat_user or not lon_user:
        lat_user, lon_user = -23.4733, -46.5873
        
    lojas_calculadas = []
    for loja in REDES_SUPERMERCADOS_REAIS:
        dist = calcular_distancia_haversine(lat_user, lon_user, loja["lat"], loja["lon"])
        
        # Inclui todas as lojas que estiverem dentro do raio selecionado pelo utilizador
        if dist <= raio_busca:
            preco_base_cesta = 280.00 * loja["preco_base_fator"]
            lojas_calculadas.append({
                "nome": loja["nome"],
                "endereco": loja["endereco"],
                "distancia_km": round(dist, 2),
                "preco_cesta": round(preco_base_cesta, 2),
                "fator_custom": loja["preco_base_fator"]
            })
            
    # Ordena por proximidade ou menor preço
    lojas_calculadas = sorted(lojas_calculadas, key=lambda x: x["distancia_km"])
    return lojas_calculadas, dados_cep

# 4. Dados dos Produtos
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
        {"id": "arroz", "nome": "Arroz Tipo 1", "variacoes": {"Pacote 1kg": 6.50, "Pacote 5kg": 28.90}},
        {"id": "feijao", "nome": "Feijão Carioca", "variacoes": {"Pacote 1kg": 8.50, "Pacote 2kg": 16.20}},
        {"id": "oleo", "nome": "Óleo de Soja", "variacoes": {"Garrafa 900ml": 6.80}},
        {"id": "acucar", "nome": "Açúcar Refinado", "variacoes": {"Pacote 1kg": 4.50, "Pacote 5kg": 21.00}},
        {"id": "cafe", "nome": "Café Torrado e Moído", "variacoes": {"Embalagem 250g": 9.90, "Embalagem 500g": 18.90}},
        {"id": "macarrao", "nome": "Macarrão Esparguete", "variacoes": {"Pacote 500g": 4.20, "Pacote 1kg": 7.90}}
    ],
    "Limpeza": [
        {"id": "sabao_em_po", "nome": "Sabão em Pó", "variacoes": {"Caixa 800g": 11.90, "Caixa 1,6kg": 22.50, "Saco 3kg": 39.90}},
        {"id": "detergente", "nome": "Detergente Líquido", "variacoes": {"Frasco 500ml": 2.60}},
        {"id": "amaciante", "nome": "Amaciante Concentrado", "variacoes": {"Frasco 500ml": 9.50, "Frasco 1.5L": 24.90}},
        {"id": "papel_higienico", "nome": "Papel Higiénico", "variacoes": {"Pacote 4 rolos": 7.50, "Pacote 12 rolos": 19.90, "Pacote 24 rolos": 36.90}}
    ],
    "Higiene Pessoal": [
        {"id": "sabonete", "nome": "Sabonete em Barra", "variacoes": {"Unidade 85g": 2.50, "Pack 6 unidades": 13.50}},
        {"id": "creme_dental", "nome": "Creme Dental", "variacoes": {"Tubo 70g": 3.90, "Tubo 90g": 4.90, "Pack Triplo (3x90g)": 12.90}}
    ]
}

# 5. Estado da Sessão
if 'step' not in st.session_state:
    st.session_state.step = 'location_setup'
if 'basket_type' not in st.session_state:
    st.session_state.basket_type = None
if 'custom_basket' not in st.session_state:
    st.session_state.custom_basket = {}
if 'user_cep' not in st.session_state:
    st.session_state.user_cep = "02300000"
if 'dados_endereco' not in st.session_state:
    st.session_state.dados_endereco = None
if 'search_radius' not in st.session_state:
    st.session_state.search_radius = 15

# ==========================================
# TELA 1: CONFIGURAÇÃO DE LOCALIZAÇÃO
# ==========================================
if st.session_state.step == 'location_setup':
    st.markdown('<div class="main-title">MapCompra 🛒📍</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-title">Insira o seu CEP para calcular a distância exata até os atacarejos.</div>', unsafe_allow_html=True)
    
    st.markdown('<div class="card-box">', unsafe_allow_html=True)
    cep_input = st.text_input("Digite seu CEP (apenas números):", value=st.session_state.user_cep)
    
    if cep_input:
        info_cep = consultar_viacep(cep_input)
        if info_cep:
            st.session_state.dados_endereco = info_cep
            st.success(f"📍 **Localizado:** {info_cep.get('bairro', 'Centro')} - {info_cep.get('localidade')}/{info_cep.get('uf')}")
        else:
            st.warning("⚠️ Insira um CEP válido de 8 dígitos.")
            st.session_state.dados_endereco = None
            
    radius_input = st.slider(
        "Raio máximo de busca (km):",
        min_value=1,
        max_value=30,
        value=st.session_state.search_radius,
        step=1
    )
    st.markdown('</div>', unsafe_allow_html=True)
    
    if st.button("Continuar para Escolha de Cesta ➔"):
        st.session_state.user_cep = cep_input
        st.session_state.search_radius = radius_input
        st.session_state.step = 'basket_selection'
        st.rerun()

# ==========================================
# TELA 2: SELEÇÃO DO TIPO DE CESTA
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
    if st.button("⬅️ Alterar CEP/Raio"):
        st.session_state.step = 'location_setup'
        st.rerun()

# ==========================================
# TELA 3: MONTAGEM DA CESTA CUSTOMIZADA
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
# TELA 4: RESULTADOS E COMPARAÇÃO DINÂMICA
# ==========================================
elif st.session_state.step == 'results':
    st.markdown('<div class="main-title">Comparativo Dinâmico 📍</div>', unsafe_allow_html=True)
    
    end_info = st.session_state.dados_endereco or {}
    ref_local = f"{end_info.get('bairro', 'Região')} - {end_info.get('localidade', 'São Paulo')}" if end_info else st.session_state.user_cep
    
    sub_text = f"Lojas num raio de até <strong>{st.session_state.search_radius} km</strong> (Ref: {ref_local})"
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

    # Gera as lojas reais calculando a distância Haversine a partir do CEP inserido
    base_lojas, _ = gerar_lojas_com_distancia_real(st.session_state.user_cep, st.session_state.search_radius)

    if st.session_state.basket_type == 'custom':
        valor_base_custom = sum(
            item["preco_un"] * item["qtd"] 
            for item in st.session_state.custom_basket.values() 
            if isinstance(item, dict) and "preco_un" in item
        )

        for loja in base_lojas:
            loja["preco_exibido"] = valor_base_custom * loja["fator_custom"]
    else:
        for loja in base_lojas:
            loja["preco_exibido"] = loja["preco_cesta"]
    
    lojas_filtradas = sorted(base_lojas, key=lambda x: x["preco_exibido"])
    
    if not lojas_filtradas:
        st.warning(f"⚠️ Nenhuma unidade encontrada neste raio de {st.session_state.search_radius} km. Tente aumentar o raio de busca.")
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
    
    col_btn1, col_btn2 = st.columns(2)
    
    with col_btn1:
        if st.button("📍 Alterar CEP/Raio"):
            st.session_state.step = 'location_setup'
            st.rerun()
            
    with col_btn2:
        texto_botao = "✏️ Alterar Itens" if st.session_state.basket_type == 'custom' else "🛒 Mudar Cesta"
        if st.button(texto_botao):
            if st.session_state.basket_type == 'custom':
                st.session_state.step = 'custom_builder'
            else:
                st.session_state.step = 'basket_selection'
            st.rerun()
