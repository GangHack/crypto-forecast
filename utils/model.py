import pandas as pd

from prophet import Prophet
from neuralprophet import NeuralProphet


def initialize_model(settings, dataset):
    if settings.model == "fbprophet":
        m = Prophet(
            changepoint_range=settings.training_percentage,
            daily_seasonality=settings.daily_seasonality,
            weekly_seasonality=settings.weekly_seasonality,
            yearly_seasonality=settings.yearly_seasonality,
            seasonality_mode=settings.seasonality_mode
        )

        if settings.future_volume > 0:
            m.add_regressor("Volume")
        if settings.holidays is not None:
            m.add_country_holidays(country_name=settings.holidays)

        dataset["ds"] = pd.to_datetime(dataset["ds"]).dt.tz_localize(None)

        m.fit(dataset)
        train_metrics = None
        val_metrics = None

    elif settings.model == "neuralprophet":
        m = NeuralProphet(
            daily_seasonality=settings.daily_seasonality,
            weekly_seasonality=settings.weekly_seasonality,
            yearly_seasonality=settings.yearly_seasonality,
            seasonality_mode=settings.seasonality_mode,
            n_forecasts=settings.future_days,
            num_hidden_layers=5
        )

        if settings.training_percentage < 1.0:
            validation_percentage = 1.0 - settings.training_percentage
            dataset["ds"] = pd.to_datetime(dataset["ds"]).dt.tz_localize(None)
            df_train, df_val = m.split_df(dataset, valid_p=validation_percentage)
        else:
            df_train = dataset
            df_val = None

        train_metrics = m.fit(
            df_train, freq="D"
        )
        if df_val is None:
            val_metrics = None
        else:
            val_metrics = m.test(df_val)

    return m, train_metrics, val_metrics


def prepare_forecast_for_future(settings, trained_model, dataset):
    if settings.model == "fbprophet":
        future = trained_model.make_future_dataframe(periods=settings.future_days)
        if settings.future_volume > 0:
            future["Volume"] = settings.future_volume

    elif settings.model == "neuralprophet":
        future = trained_model.make_future_dataframe(
            dataset,
            periods=settings.future_days,
            n_historic_predictions=len(dataset)
        )
    return future


def execute_prediction(trained_model, future_data):
    forecast = trained_model.predict(future_data)
    return forecast
