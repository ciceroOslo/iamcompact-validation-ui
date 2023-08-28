# IAM data validation app

## Introduction

This app automates processes for validating the modelling results of Integrated Assessment Models (IAMs) and other types of climate-economy models. Validation routines include automated checks for variable and model names, a duplicates finder, and a series of vetting checks based on the IPCC AR6 vetting rules found in the IPCC AR6 Working Group III report, Annex III, Table 11 ([link](https://www.ipcc.ch/report/ar6/wg3/downloads/report/IPCC_AR6_WGIII_Annex-III.pdf)).

The app is built in Python and Streamlit and will be eventually integrated in I2AM PARIS, an open-access, data exchange platform for modelling results ([link](https://i2am-paris.eu)).

The app is currently deployed in: https://validation.i2am-paris.eu.

## Installation

To run the Streamlit app locally:

    streamlit run 1_Upload_data.py

To run the app in a production server, simply download the data and run the Docker file at the source directory.

## Documentation

Instructions are given directly on the app (see deployed version [here](https://validation.i2am-paris.eu)). More detailed documentation will follow.

## License

GPL-3.0-or-later

