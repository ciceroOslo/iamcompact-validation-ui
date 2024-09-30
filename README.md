# IAM COMPACT results validation and vetting app

## Introduction

This app is used for performing name-validation and region-mapping on the modelling results of Integrated Assessment Models (IAMs)
in the IAM COMPACT project, as well as vetting using the vetting criteria from IPCC AR6, and comparison with harmonization data
(at the moment only population and GDP). Specification of the vetting criteria for IPCC AR6 vetting rules can be found in the
IPCC AR6 Working Group III report, Annex III, Table 11 ([link](https://www.ipcc.ch/report/ar6/wg3/downloads/report/IPCC_AR6_WGIII_Annex-III.pdf)).

The app is built in Python and Streamlit and will be eventually integrated in I2AM PARIS, an open-access, data exchange platform for modelling results ([link](https://i2am-paris.eu)).

## Installation

To run the Streamlit app locally:

    streamlit run ui/main.py

To run the app in a production server, simply download the data and run the Docker file at the source directory.



## Documentation

Instructions are given directly in the app. More detailed documentation will follow.

## License

GPL-3.0-or-later

