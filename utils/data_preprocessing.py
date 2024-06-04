import datetime
import streamlit as st


def prepare_history_data(ui_params, df_history):
    df_history_prep = df_history.reset_index()

    date_column = "Date" if "Date" in df_history_prep.columns else "Datetime"

    if ui_params.future_volume > 0:
        data = df_history_prep[[date_column, ui_params.price_column, "Volume"]]
    else:
        data = df_history_prep[[date_column, ui_params.price_column]]
    data = data.rename(
        columns={
            date_column: "ds",
            ui_params.price_column: "y"
        }
    )

    return data


def highlight_negative(s):
    return ["color: red;"] * len(s) if s.Change < 0 else ["color: green"] * len(s)


def display_future_change(settings, data, processed_prediction):
    if settings.model == "fbprophet":
        yhat_label_low = "yhat_lower"
        yhat_label_mid = "yhat"
        yhat_label_high = "yhat_upper"
    elif settings.model == "neuralprophet":
        yhat_label_low = "yhat1"
        yhat_label_mid = "yhat1"
        yhat_label_high = "yhat1"

    last_day_price = data[data["ds"] == data["ds"].max()].iloc[0]["y"]

    next_day_price_low = processed_prediction[
        processed_prediction["ds"] == processed_prediction["ds"].min()
    ].iloc[0][yhat_label_low]
    next_day_price_mid = processed_prediction[
        processed_prediction["ds"] == processed_prediction["ds"].min()
    ].iloc[0][yhat_label_mid]
    next_day_price_high = processed_prediction[
        processed_prediction["ds"] == processed_prediction["ds"].min()
    ].iloc[0][yhat_label_high]

    next_day_change_low = next_day_price_low - last_day_price
    next_day_change_percentage_low = (next_day_change_low / last_day_price) * 100

    next_day_change_mid = next_day_price_mid - last_day_price
    next_day_change_percentage_mid = (next_day_change_mid / last_day_price) * 100

    next_day_change_high = next_day_price_high - last_day_price
    next_day_change_percentage_high = (next_day_change_high / last_day_price) * 100

    last_future_day_price_low = \
        processed_prediction[processed_prediction["ds"] == processed_prediction["ds"].max()].iloc[0][yhat_label_low]
    last_future_day_price_mid = \
        processed_prediction[processed_prediction["ds"] == processed_prediction["ds"].max()].iloc[0][yhat_label_mid]
    last_future_day_price_high = \
        processed_prediction[processed_prediction["ds"] == processed_prediction["ds"].max()].iloc[0][yhat_label_high]

    future_day_change_low = last_future_day_price_low - last_day_price
    future_day_change_percentage_low = (future_day_change_low / last_day_price) * 100

    future_day_change_mid = last_future_day_price_mid - last_day_price
    future_day_change_percentage_mid = (future_day_change_mid / last_day_price) * 100

    future_day_change_high = last_future_day_price_high - last_day_price
    future_day_change_percentage_high = (future_day_change_high / last_day_price) * 100

    last_day_date = datetime.datetime.date(data["ds"].max())
    next_day_price_date = datetime.datetime.date(processed_prediction["ds"].min())
    last_future_day_price_date = datetime.datetime.date(processed_prediction["ds"].max())

    st.write(f"Базове значення - ({last_day_date}): {last_day_price:,.2f}")

    if settings.model == "fbprophet":
        st.subheader("Завтра")
        st_metric_next_day_low, st_metric_next_day_mid, st_metric_next_day_high = st.columns(3)
        st.subheader("Наступний рік")
        st_metric_next_year_low, st_metric_next_year_mid, st_metric_next_year_high = st.columns(3)

        st_metric_next_day_low.metric(
            label=f"Low {next_day_price_date}",
            value=f"{next_day_price_low:,.4f}",
            delta=f"{next_day_change_low:,.4f} | {next_day_change_percentage_low:,.4f}%"
        )
        st_metric_next_day_mid.metric(
            label=f"Mid {next_day_price_date}",
            value=f"{next_day_price_mid:,.4f}",
            delta=f"{next_day_change_mid:,.4f} | {next_day_change_percentage_mid:,.4f}%"
        )
        st_metric_next_day_high.metric(
            label=f"High {next_day_price_date}",
            value=f"{next_day_price_high:,.4f}",
            delta=f"{next_day_change_high:,.4f} | {next_day_change_percentage_high:,.4f}%"
        )

        st_metric_next_year_low.metric(
            label=f"Low {last_future_day_price_date}",
            value=f"{last_future_day_price_low:,.4f}",
            delta=f"{future_day_change_low:,.4f} | {future_day_change_percentage_low:,.4f}%"
        )
        st_metric_next_year_mid.metric(
            label=f"Mid {last_future_day_price_date}",
            value=f"{last_future_day_price_mid:,.4f}",
            delta=f"{future_day_change_mid:,.4f} | {future_day_change_percentage_mid:,.4f}%"
        )
        st_metric_next_year_high.metric(
            label=f"High {last_future_day_price_date}",
            value=f"{last_future_day_price_high:,.4f}",
            delta=f"{future_day_change_high:,.4f} | {future_day_change_percentage_high:,.4f}%"
        )

    elif settings.model == "neuralprophet":
        st_header_next_day_mid, st_header_next_year_mid = st.columns(2)
        st_header_next_day_mid.subheader("Завтра")
        st_header_next_year_mid.subheader("Наступний рік")

        st_metric_next_day_mid, st_metric_next_year_mid = st.columns(2)
        st_metric_next_day_mid.metric(
            label=f"Mid {next_day_price_date}",
            value=f"{next_day_price_mid:,.4f}",
            delta=f"{next_day_change_mid:,.4f} | {next_day_change_percentage_mid:,.4f}%"
        )
        st_metric_next_year_mid.metric(
            label=f"Mid {last_future_day_price_date}",
            value=f"{last_future_day_price_mid:,.4f}",
            delta=f"{future_day_change_mid:,.4f} | {future_day_change_percentage_mid:,.4f}%"
        )
