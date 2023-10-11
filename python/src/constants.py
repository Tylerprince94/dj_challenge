"""Simple contants file to hold sql statements in memory"""
##################################### Create Database #########################################
create_weather_db = """
    CREATE DATABASE IF NOT EXISTS Weather
"""
###################################### Create Tables ##########################################
create_pollution_event_table = """
    CREATE TABLE IF NOT EXISTS Weather.PollutionEvent(
        AnalysisDate DATE NOT NULL,
        ForecastTime DATETIME NOT NULL,
        AirQualityIndex INT(1) NOT NULL,
        CarbonMonoxide FLOAT(5) NOT NULL,
        NitrogenMonoxide FLOAT(4) NOT NULL,
        NitrogenDioxide FLOAT(4) NOT NULL,
        Ozone FLOAT(5) NOT NULL,
        SulphurDioxide FLOAT(4) NOT NULL,
        FineParticlesMatter FLOAT(5) NOT NULL,
        CoarseParticulateMatter FLOAT(5) NOT NULL,
        Ammonia FLOAT(4) NOT NULL,
        PRIMARY KEY (AnalysisDate, ForecastTime)
    );
"""
create_avg_four_day_forecast_table = """
    CREATE TABLE IF NOT EXISTS Weather.AVGFourDayForecast(
        AnalysisDate DATE NOT NULL,
        AVGAirQualityIndex INT(1) NOT NULL,
        AVGCarbonMonoxide FLOAT(5) NOT NULL,
        AVGNitrogenMonoxide FLOAT(4) NOT NULL,
        AVGNitrogenDioxide FLOAT(4) NOT NULL,
        AVGOzone FLOAT(5) NOT NULL,
        AVGSulphurDioxide FLOAT(4) NOT NULL,
        AVGFineParticlesMatter FLOAT(5) NOT NULL,
        AVGCoarseParticulateMatter FLOAT(5) NOT NULL,
        AVGAmmonia FLOAT(4) NOT NULL,
        PRIMARY KEY (AnalysisDate)
    );
"""
###################################### Insert Tables ##########################################
pollution_table_insert = """
    insert into Weather.PollutionEvent (AnalysisDate, ForecastTime, AirQualityIndex,
        CarbonMonoxide, NitrogenMonoxide, NitrogenDioxide, Ozone, SulphurDioxide,
        FineParticlesMatter, CoarseParticulateMatter, Ammonia)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
"""
four_day_forecast_insert = """
    insert into Weather.AVGFourDayForecast (AnalysisDate, AVGAirQualityIndex,
        AVGCarbonMonoxide, AVGNitrogenMonoxide, AVGNitrogenDioxide, AVGOzone,
        AVGSulphurDioxide, AVGFineParticlesMatter, AVGCoarseParticulateMatter, AVGAmmonia)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
"""
###################################### Select Tables ##########################################
pollution_date_select = """
    Select * FROM Weather.PollutionEvent WHERE AnalysisDate = %s;
"""
four_day_forecast_date_select = """
    Select * FROM Weather.AVGFourDayForecast WHERE AnalysisDate = %s;
"""