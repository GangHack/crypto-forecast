import streamlit as st

from utils.vars import *
from utils.attr_dict_class import AttrDict


def format_crypto(x):
    return CRYPTOS[x] if x is None else x + " - " + CRYPTOS[x]


def initialize_ui_params() -> AttrDict:
    st.title("Прогнозування економічних показників криптовалют")
    st_ml_model = st.sidebar.selectbox(
        "Модель передбачення",
        options=list(ML_MODELS.keys()),
        index=0,
        format_func=lambda x: ML_MODELS[x]
    )
    st_crypto_stock = st.sidebar.radio("Тип символу", options=TICKER_TYPE)
    if st_crypto_stock == TICKER_TYPE[0]:
        st_crypto_name = st.sidebar.selectbox(
            "Криптовалютний символ",
            options=list(CRYPTOS.keys()),
            format_func=format_crypto
        )
        st_currency_name = st.sidebar.selectbox("Валюта", options=CURRENCIES)

        if st_crypto_name is None:
            st_ticker_name = None
        else:
            st_ticker_name = st_crypto_name + "-" + st_currency_name

    elif st_crypto_stock == TICKER_TYPE[1]:
        st_ticker_name_list = st.sidebar.text_input("Фондовий символ")
        st_ticker_name_list = [st_ticker_name_list]

        if len(st_ticker_name_list) > 0:
            st_ticker_name = st_ticker_name_list[0].upper()
        else:
            st_ticker_name = None

    st_period = st.sidebar.selectbox(
        "Період",
        options=list(PERIODS.keys()),
        index=7,
        format_func=lambda x: PERIODS[x]
    )
    st_interval = st.sidebar.selectbox(
        "Інтервал",
        options=list(INTERVALS.keys()),
        index=8,
        format_func=lambda x: INTERVALS[x]
    )
    st_price_column = st.sidebar.selectbox(
        "Вартість",
        options=TICKER_DATA_COLUMN,
        index=3
    )
    st_future_days = st.sidebar.number_input(
        "Кількість майбутніх днів",
        value=365,
        min_value=1,
        step=1
    )
    st_future_volume = st.sidebar.number_input(
        "Припущення майбутнього обсягу",
        value=0,
        min_value=0,
        step=1
    )
    st.sidebar.caption("Встановіть значення в 0 для ігнорування")
    st_training_percentage = st.sidebar.slider(
        "Відсоток навчання",
        min_value=0.0,
        max_value=1.0,
        step=0.1,
        value=0.8
    )
    st_yearly_seasonality = st.sidebar.selectbox(
        "Річна сезонність",
        options=SEASONALITY_OPTIONS,
        index=0
    )
    st_weekly_seasonality = st.sidebar.selectbox(
        "Тижнева сезонність",
        options=SEASONALITY_OPTIONS,
        index=0
    )
    st_daily_seasonality = st.sidebar.selectbox(
        "Щоденна сезонність",
        options=SEASONALITY_OPTIONS,
        index=0
    )
    st_holidays = st.sidebar.selectbox(
        "Свята",
        options=list(HOLIDAYS.keys()),
        index=0,
        format_func=lambda x: HOLIDAYS[x]
    )

    if st_crypto_stock == TICKER_TYPE[0]:
        st_seasonality_mode_index = 0
    else:
        st_seasonality_mode_index = 1
    st_seasonality_mode = st.sidebar.selectbox(
        "Режим сезонності",
        options=SEASONALITY_MODE_OPTIONS,
        index=st_seasonality_mode_index
    )

    params_dict = AttrDict(
        model=st_ml_model,
        ticker_name=st_ticker_name,
        period=st_period,
        interval=st_interval,
        future_days=st_future_days,
        price_column=st_price_column,
        yearly_seasonality=st_yearly_seasonality,
        future_volume=st_future_volume,
        daily_seasonality=st_daily_seasonality,
        training_percentage=st_training_percentage,
        holidays=st_holidays,
        weekly_seasonality=st_weekly_seasonality,
        seasonality_mode=st_seasonality_mode
    )

    return params_dict


def create_cross_validation_form(settings) -> AttrDict:
    col1, col2, col3 = st.columns(3)
    with col1:
        st_cv_initial_days = st.number_input(
            "Початкові дні", value=730, min_value=1, step=1
        )
    with col2:
        st_cv_period_days = st.number_input(
            "Дні в періоді", value=180, min_value=1, step=1
        )
    with col3:
        st_cv_horizon_days = st.number_input(
            "Горизонт днів", value=365, min_value=1, step=1
        )

    st_validation_metric = st.selectbox(
        "Валідаційна метрика", options=VALIDATION_METRICS, index=3
    )
    show_cross_validation = st.form_submit_button(label="Cross-Validate")
    st.caption("Це може зайняти деякий час.")

    params_dict = AttrDict(
        initial_days=st_cv_initial_days,
        cross_validation=show_cross_validation,
        period_days=st_cv_period_days,
        horizon_days=st_cv_horizon_days,
        validation_metric=st_validation_metric,
    )

    return params_dict
