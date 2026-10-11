# GeoModulus AI

## Soil Elastic Modulus Prediction and Engineering Decision Support System

GeoModulus AI is a machine-learning-based web application developed to predict soil elastic modulus using laboratory and field soil parameters.

The system predicts four modulus measurements:

- PLT E
- Geogauge E
- DCP E
- LWD E

It also evaluates different reinforcement conditions and provides an engineering-oriented recommendation.

---

## 1. Project Overview

Soil stiffness is an important factor in pavement and ground engineering.

GeoModulus AI uses machine learning regression models to estimate soil elastic modulus from available soil and field parameters.

The application provides:

1. Soil parameter input
2. Automatic PI calculation
3. Elastic modulus prediction
4. Reinforcement comparison
5. Soil quality assessment
6. Pavement recommendation
7. Engineering decision support

---

## 2. Objectives

The main objectives of GeoModulus AI are:

- Predict soil elastic modulus using machine learning.
- Use laboratory and field soil parameters as model inputs.
- Predict multiple modulus measurements.
- Compare unreinforced and reinforced soil conditions.
- Evaluate 400 GSM and 700 GSM reinforcement.
- Provide an engineering-oriented recommendation.
- Provide an easy-to-use web interface for prediction.

---

## 3. Dataset

The project uses a dataset containing 179 soil samples.

### Dataset Statistics

| Property | Value |
|---|---:|
| Total Samples | 179 |
| Input Features | 9 |
| Prediction Targets | 4 |
| Reinforcement Conditions | 3 |

### Reinforcement Distribution

| Condition | Samples |
|---|---:|
| Unreinforced / UR | 124 |
| 400 GSM | 28 |
| 700 GSM | 27 |

---

## 4. Input Features

The machine learning models use the following features:

| Feature | Description |
|---|---|
| LL | Liquid Limit |
| PL | Plastic Limit |
| PI | Plasticity Index |
| OMC | Optimum Moisture Content |
| MDD (g/cc) | Maximum Dry Density |
| Depth of reinforcement | Reinforcement depth |
| Reinforced/Unreinforced | Reinforcement condition |
| Soaked/Unsoaked | Soil moisture condition |
| CBR (%) | California Bearing Ratio |

### Plasticity Index

PI is automatically calculated using:

```text
PI = LL - PL