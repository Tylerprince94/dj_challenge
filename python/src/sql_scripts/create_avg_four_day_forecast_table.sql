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