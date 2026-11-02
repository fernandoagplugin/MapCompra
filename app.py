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
    
    # Botões lado a lado: Alterar CEP/Raio ou Alterar os Itens/Tipo de Cesta
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
