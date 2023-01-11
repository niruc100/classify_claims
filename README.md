# DKE 2022 Home Project
This repository contains the home project for the Data and Knowledge Engineering class 2022 at Heinrich Heine University.
The project exercise can be completed at home, using the expertise and skill sets acquired in the DKE 2022 lecture.
Use this repository to prepare your solution.


## Folder Structure

- **assignment**: contains a more detailed description of the task and the required output. 
- **src**: add your code here in the suitable subfolder(s) (depending on whether you use Python or Java). 
- **test_data**:  the test data will be added to this folder. Please refer to the task description in the assignment folder for information on the format. The dummy_ids.csv file contains dummy data in the required format. 
- **output_data**: folder that must be populated with the results of the home project. Please refer to the task description in the assignment folder for information on the format. The file dummy_predictions.csv contains dummy data in the required format. 

## 1. Prerequisites
- python >= 3.10.4
- packages in `requirements.txt`
- Active internet connection 

## 2. Data Aquisition

You can obtain the data for training and testing from [ClaimsKG](https://data.gesis.org/claimskg/) by running the jupyter notebook `data_import.ipynb` from start to finish. However, it is not a very efficient implementation so it will take `~12min` to query and process the data. Finally, the data is stored in the `data` folder as `raw_claims.csv` and `raw_test_claims.csv`.

**Notes**:
- For convenience, we uploaded the data already into the `data` folder.
- We ensured that non of the test IDs is present in our data that we queried for train and evaluation of a Machine Learning model.

SPARQL query for the train set:
``` sparql
PREFIX itsrdf:<https://www.w3.org/2005/11/its/rdf#>
    PREFIX schema:<http://schema.org/>
    PREFIX dbr:<http://dbpedia.org/resource/> 
    SELECT ?claim ?text ?date ?ratval 
    WHERE { 
		    {
			    SELECT ?claim ?text ?date ?ratval 
			    WHERE {
			    ?review a schema:ClaimReview .
			    ?review schema:reviewRating ?rating .
			    ?rating schema:alternateName ?ratval .
			    ?review schema:itemReviewed ?claim .
			    ?claim schema:text ?text .
                ?review schema:datePublished ?date .
                FILTER regex(?ratval , "(^FALSE|TRUE|OTHER)") 
			    } ORDER BY ?claim 
		    }
	    }  
	LIMIT 10000 OFFSET
```

SPARQL query for the test set:
``` sparql
	PREFIX itsrdf:<https://www.w3.org/2005/11/its/rdf#>
    PREFIX schema:<http://schema.org/>
    PREFIX dbr:<http://dbpedia.org/resource/> 
    SELECT ?claim ?text 
    WHERE{
		    {
			    SELECT ?claim ?text 
			    WHERE {
			    ?claim a schema:CreativeWork .
                ?claim schema:text ?text .
			    } 
		    } FILTER regex(?claim ,
```

- Both queries are completed during a python loop with the offset integer and the test ID respectively.


## 3. Data Preprocessing

Before preprocessing, ensure that `raw_claims.csv` is located in the `data` folder. If this is not the case run `data_import.ipynb`. To obtain the preprocessed data, run `data_preprocessing.ipynb`. Finally, the preprocessed data is stored in the `data` folder as `preprocessed_claims.csv`.

**Notes**:
- For convenience, we uploaded the preprocessed data already into the `data` folder (since preprocessing will take ~20min)

- In data_preprocessing.ipynb we removed claims with the same id, very short claims and non-english claims that were labeled "FALSE". 

- The other non-englisch claims were translated into englisch using google-translate to account for the underrepresented "OTHER" and "TRUE" claims.

## 4. Augmented data

Before augmenting the data, ensure that `preprocessed_claims.csv` is located in the `data` folder. If this is not the case run `data_preprocessing.ipynb`. To obtain the augmented data, run `data_augmentation.ipynb`. Finally, the augmented data is saved to the `data` folder as `augmented_claims.csv`.

**Notes**:
- For convenience, we uploaded the augmented data already into the `data` folder (since augmenting the data will take ~6h)
- This augmented data is from the 20K claims of the first version, there is currently no augmented data for the 40K "new" claims from after a query update!

## 5. Train Model

Before training the model, ensure that `preprocessed_claims.csv` is located in the `data` folder. By running `train_model.py` you can retrain the current best model on the loaded data which is saved to the `data` folder as `vectorizer_v1.pkl` and `model_v1.pkl`.

**Notes**:
- For convenience, we uploaded the trained model and vectorizer already into the `data` folder, however, retraining is fast.
- The performance is similar (bad) when using `augmented_claims.csv` as training data.

## 6. Evaluation

Before evaluating the model, ensure that `vectorizer_v1.pkl` and `model_v1.pkl` as well as `raw_test_claims.csv` are located in the `data` folder. The `.pkl` files can be obtained by running `train_model.py` while the test data is obtained by running `data_import.ipynb`. Finally, run `eval_model.py` to load the test data and the model and to obtain the predictions as `predictions.csv` in the  `output_data` folder. 

Afterwards, the `eval.py` in the `eval` folder can be executed.

**Notes**:
- For convenience, we uploaded the predictions into the `output_data` folder, however, re-running the `eval_model.py` is fast.


