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