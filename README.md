# Master's Thesis
## Clinical Prognosis and Risk Prediction of PostoperativeComplications in Cancer Patients

This repository contains all the code and results used in this project.

Postoperative complications of cancer surgery are still hard to predict, although there are risk scores intended to make such predictions. They vary with regards to their outcome, surgical cohort, or type of predictive model. The differences among studies, contribute for the creation of highly specialized tools, with poor reusability in foreign contexts. Adaptability to different surgical domains and populations can add to larger errors, since often these studies are developed in carefully selected surgical cohorts. Today, new techniques have been proposed to create potentially more powerful and accurate predictors, capable of modeling high dimensional data and its inherent complexities. This thesis aims to study and predict postoperative complications risk for cancer patients, offering two major contributions. First, to develop a risk calculator using machine learning models, with 4 outcomes of interest: existence of postoperative complications, severity level of said complications, death probability within 1 year, and number of days spent in the intermediate care unit. Second, to support the study of this disease with relevant findings and improve the interpretability of predictive models, especially associative models by extending tree representations to capture measures of generalization ability. As a result, we provide a set of models with reliable guarantees of predictive performance and offer new perspectives and insights into the decision process. Postoperative complications can be predicted with 68% accuracy, complications' severity can be predicted with MAE = 1.56, the days in the ICU can be predicted with MAE = 1.04, and 1 year death can be predicted with 75% accuracy. The proposed predictive models yield statistically significant improvements against their respective baseline models (p-value < 0.01).

The content found in this repository corresponds to all the initial data processing, which is then fed to a wide set of ML models. These models were improved through different stages, including resampling, normalization, hyperparameter optimization, feature selection, etc. The results were subject to succesive evaluation processes, in order to gather as much insight into models' performance as possible.

Access to the original dataset is restricted due to data privacy concerns. To know more about the dataset used in this study, please contact:
- Daniel Gonçalves, dmateusgoncalves@tecnico.ulisboa.pt
- Rafael Costa, rafael.s.costa@tecnico.ulisboa.pt
- Rui Henriques, rmch@tecnico.ulisboa.pt

