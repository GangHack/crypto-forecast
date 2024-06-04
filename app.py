import streamlit as st
import numpy as np
import os
import datetime
import plotly.graph_objects as go

from utils.vars import *
from utils.cross_validation import (
    cross_validating,
    evaluating,
    plot_validation,
    plot_validation_neural
)
from utils.data_preprocessing import (
    prepare_history_data,
    display_future_change
)
from utils.db import (
    update_db,
    reset_tmp_db
)
from utils.model import (
    initialize_model,
    prepare_forecast_for_future,
    execute_prediction
)
from utils.ticker import display_stock_info
from utils.ui_params import (
    initialize_ui_params,
    create_cross_validation_form
)
from utils.visualization import (
    plot_predictions,
    plot_fbprophet_components
)

os.environ["KMP_DUPLICATE_LIB_OK"] = "True"


def main():
    qs_data = st.query_params.to_dict()
    for key, value in qs_data.items():
        if key == "reset_db" and str(value[0]) == "true":
            if reset_tmp_db():
                st.success(
                    "Тимчасову базу даних успішно видалено."
                )
            st.experimental_set_query_params(reset_db="false")

    st_app_menu = st.sidebar.selectbox(
        "Головне меню",
        options=list(MENU_OPTIONS.keys()),
        index=0,
        format_func=lambda x: MENU_OPTIONS[x]
    )

    ui_params = initialize_ui_params()

    if ui_params.ticker_name is None or len(ui_params.ticker_name) == 0:
        st.warning(
            "⚠️ Будь ласка, введіть дійсний символ або виберіть криптовалюту з меню бічної панелі ⚠️"
        )
    else:
        ph_app_status = st.empty()
        st.subheader(ui_params.ticker_name)

        df_history = display_stock_info(ui_params)

        st.subheader(f"{ui_params.ticker_name.upper()} Історичні ціни")
        fig = go.Figure(
            data=[go.Candlestick(
                x=df_history.index,
                open=df_history["Open"],
                high=df_history["High"],
                low=df_history["Low"],
                close=df_history["Close"]
            )]
        )
        fig.update_layout(
            xaxis_title="Date",
            yaxis_title="Price (USD)",
            xaxis_rangeslider_visible=True
        )
        st.plotly_chart(fig, use_container_width=True)

        if df_history is not None:
            update_db(ui_params.ticker_name)

            data = prepare_history_data(ui_params, df_history)

            st.subheader("Передбачення")

            ph_training = st.empty()
            ph_app_status.info("Розпочато навчання. Будь ласка, зачекайте...")
            ph_training.info("Розпочато навчання. Будь ласка, зачекайте...")
            m, train_metrics, val_metrics = initialize_model(ui_params, data)

            ph_app_status.info("Створення майбутнього набору даних...")
            ph_training.info("Створення майбутнього набору даних...")
            future = prepare_forecast_for_future(ui_params, m, data)

            ph_app_status.info("Передбачення...")
            ph_training.info("Передбачення...")
            prediction = execute_prediction(m, future)

            col1, col2 = st.columns(2)
            with col1:
                today_date = data["ds"].max()
                tomorrow_date = today_date + datetime.timedelta(days=1)
                st_from_date = np.datetime64(
                    st.date_input(
                        "Від",
                        value=tomorrow_date,
                        min_value=tomorrow_date
                    )
                )
            with col2:
                st_to_date = np.datetime64(
                    st.date_input(
                        "До",
                        value=prediction["ds"].max(),
                        max_value=prediction["ds"].max()
                    )
                )

            filtered_prediction = prediction[
                (prediction["ds"] >= st_from_date) &
                (prediction["ds"] <= st_to_date)
            ]
            st.write(filtered_prediction)
            ph_training.empty()

            st.header("Майбутні зміни")
            display_future_change(ui_params, data, filtered_prediction)

            st.subheader("Візуалізація")
            plot_predictions(ui_params, m, prediction)
            plot_fbprophet_components(ui_params, m, prediction)

            st.subheader("Крос-валідація")
            ph_cross_validation = st.empty()

            if ui_params.model == "fbprophet":
                with st.form(key="cross-validation"):
                    ui_cv_params = create_cross_validation_form(ui_params)

                if ui_cv_params.cross_validation:
                    ph_app_status.info("Cross-Validating...")
                    ph_cross_validation.info(
                        "Розпочато процес перехресної перевірки. Будь ласка, зачекайте..."
                    )

                    df_cv = cross_validating(
                        m,
                        ui_cv_params.initial_days,
                        ui_cv_params.period_days,
                        ui_cv_params.horizon_days
                    )

                    ph_cross_validation.info(
                        "Обчислення показників ефективності. Будь ласка, зачекайте..."
                    )
                    pm = evaluating(df_cv)

                    ph_cross_validation.info("Формуємо результати...")
                    plot_validation(
                        pm, df_cv, metric=ui_cv_params.validation_metric
                    )

            elif ui_params.model == "neuralprophet":
                st.write("**Тренувальні метрики**")
                st.write(train_metrics)
                plot_validation_neural(train_metrics, "Loss")
                plot_validation_neural(train_metrics, "RMSE")
                plot_validation_neural(train_metrics, "MAE")
                plot_validation_neural(train_metrics, "RegLoss")

                st.write("**Валідаційні метрики**")
                st.write(val_metrics)
                plot_validation_neural(val_metrics, "Loss_test")
                plot_validation_neural(val_metrics, "RegLoss_test")

                ph_cross_validation.empty()

        ph_app_status.empty()


if __name__ == '__main__':
    st.set_page_config(
        page_title="Прогнозування економічних показників криптовалют",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    main()
