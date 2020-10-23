# Master's Thesis
### Clinical Prognosis and Risk Prediction of PostoperativeComplications in Cancer Patients

This repository contains all the code and results used in this project.

Postoperative complications derived from cancer surgery are still hard to predict, although there are risk scores that intend to predict the risk of such complications. They vary with regards to the prediction target, surgical cohort used for development, or type of predictive model. The differences among them, and in the environments where they are created, make their reusability deficient in foreign contexts. Adaptability to different oncology domains and new cohorts adds to larger errors in predictions, and specific surgical domains need scores obtained from carefully selected surgical cohorts. The outcomes are also a problem since different hospitals and units have different necessities, creating a need for specialized tools. Nowadays there are techniques that can be used to create potentially more powerful and accurate predictors, capable of modeling high dimensional data and its inherent complexities. This thesis aims to develop a risk calculator, using machine learning models, that is able to predict 4 outcomes of interest: existence of postoperative complications, severity level of said complication, death probability within 1 year, and number of days spent in the intermediate care unit.

The content found in this repository corresponds to all the initial data processing, which is then fed to a wide set of ML models. These models were improved through different stages, including resampling, normalization, hyperparameter optimization, feature selection, etc. The results were subject to succesive evaluation processes, in order to gather as much insight into models' performance as possible.

Access to the original dataset is restricted due to data privacy concerns. To know more about the dataset used in this study, please contact:
- Daniel Gonçalves, dmateusgoncalves@tecnico.ulisboa.pt
- Rafael Costa, rafael.s.costa@tecnico.ulisboa.pt
- Rui Henriques, rmch@tecnico.ulisboa.pt

