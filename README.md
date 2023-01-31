# IUU-Fishing
IUU fishing detecting using AIS disabling data

## *Documentation*

###### Making the dataset - 
we took the ais_disabling_events dataset from the global fishing watch website which contains the MMSI of the ships which disabled their AIS. It also contains the lat and long of where they disabled their AIS and when they enabled it again, the gap hours during which the AIS was disabled.

We then took datasets from various different RFMOs which contained the vessel identities of all the vessels who have been caught doing IUU activity in their region. 
The datasets were very unorganized and some didn't even contain the identities of the vessels who had been caught.
We used data from the following RFMOs - 
SPRFMO
CCAMLR - http://www.ccamlr.org/en/compliance/illegal-unreported-and-unregulated-iuu-fishing
CCSBT - https://www.ccsbt.org/en/content/iuu-vessel-lists
GFCM - http://www.fao.org/gfcm/data/iuu-vessel-list
IATTC - https://www.iattc.org/VesselRegister/IUU.aspx?Lang=en
IOTC - http://www.iotc.org/vessels#iuu
NAFO - https://www.nafo.int/Fisheries/IUU
NEAFC - http://www.neafc.org/mcs/iuu
NPFC - https://www.npfc.int/npfc-iuu-vessel-list
SEAFO - http://www.seafo.org/Management/IUU
SIOFA - http://www.apsoi.org/mcs/iuu-vessels
WCPFC - http://www.wcpfc.int/wcpfc-iuu-vessel-list

We then combined the datasets into one excel file and then made a python script which used the Global Fishing Watch API to get the MMSI number of the respective IMO number. In the RFMO dataset we only had the IMO number available so we needed the MMSI to correlate that with the AIS disabling dataset we obtained from the Global Fishing Watch.

We then took the unique MMSI we got from the python script and put them together with the AIS disabling dataset. We then found the intersection of the MMSI we found from the python script and the MMSI in the GFW dataset. We got 11 such MMSIs which had been caught in IUU fishing according to various RFMOs and who disabled their MMSI according to the GFW dataset.

We wrote a python script to generate various features from the available attributes. We generated -
1) The distance traveresed during the time AIS was disabled (we used spherical distance since the world is a globe)
2) We got whether or not AIS was disabled in the EEZ by using the distance_from_shore attribute. (EEZ is the 200 nautical mile distance from the shore for each country wherein only they can conduct economic activities).
3) We got in which ocean was the AIS disabled by using the start_lat and start_lon attributes.
We used this because there are studies which show that IUU fishing takes place more in some oceans as compared to others. For this we downloaded a GeoJSON from the FAOs website which contained the Major Fishing Areas as mapped by the FAO. We then wrote a python script for getting the ocean name of each of the coordiante in the GFW dataset (55,368 entries), for this we used the shapely library. But we got a lot of false entries which suggested that the coordinate did not lie in any ocean while it did, it happened due to the fact that the GeoJSON file was very complex and it may contain self-intersecting lines. When the polygon is very complex there are chances for some errors occuring.
So, we went to the IHO website and got the GeoJSON for each ocean individually and then wrote a python script which itereated through each of the ocean JSON and indentified if the coordinate lies in it. Here as well we got a lot of False values but the values we got as False here were True in the previous method where we used the FAO GeoJSON and the values that were False previously were True here.
So, we merged the results of both the datasets and got only 227 entries out of 55,000 whose coordinates we could not identify.

Finally, we made a CSV with all the attributes and features we would use to train the model. We used the features - 
vessel_class
gap_hours
iuu_caught
distance_traversed
eez_chech
ocean_name

Conclusion - 
We made a dataset which contained 55268 values which weren't caught in IUU activites by different RFMOs and 100 values which were caught in IUU activities by different RFMOs.
This is a highly imbalanced dataset.

--------------------------------------------------------------------------------------------

## Machine Learning Part 1 - 

We did one hot encoding as 2 of our attributes were categorical (vessel_class and Ocean List New whose false were in OG) to make them usable for machine learning.
After that we split the data intro training and testing set using a 80/20 split with more datapoints in the training dataset.
Since it was a highly imbalanced dataset we used the SMOTE techinque to make it balanced. It is a statistical technique for increasing the number of cases in your dataset in a balanced way. 

###### ANN - 
We then implemented an ANN which has 3 dense layers - 
first layer had 26 neurons with relu activation
second layer had 15 neurons with relu activation
third layer had 1 neuron with sigmoid activation
We used the adam optimizer and fit the model and ran for 50 epochs.

We got a precision of 0.96 and f1-score of 0.97 for the minority class which is really promising for a highly imbalanced dataset.

###### XGboost - 
XBboost is a very good classifier and very popular nowadays, using that we got a precision of 0.95 and f1-score of 0.97 for the minority class which is really promising for a highly imbalanced dataset.

###### Random Forest - 
We also used the random forest algo and got a precision of 0.99 and f1-score of 0.99 for the minority class which is really promising for a highly imbalanced dataset.

So above we had used SMOTE on both the training and testing dataset that's why we were getting such promising results. SMOTE can be use on the both the sets but it isn't considered the best practice and it should only be used on the training dataset.

---------------------------------------------------------------------------------------------

## Machine Learning Part 2 - 

Now we tried applying the same algorithms but use SMOTE only on the training data and not on the testing data.
Here we used a training/testing split of 60/40

###### Random Forest - 
We got a precision of 0.03 and f1-score of 0.04 for the minority class.

###### Ensemble learning - 
We tried ensemble methods as they use multiple learning algorithms to obtain better predictive performance than could be obtained from a single method.
We used an ensemble of xgboost and random forest and we got a precision of 0.03 and f1-score of 0.06 for the minority class.

###### Stacking Classifier - 
A stacking classifier is an ensemble learning method that combines multiple classification models to create one “super” model. This can often lead to improved performance, since the combined model can learn from the strengths of each individual model.
Here we used random forest, xgboost and ANN with the final estimator as MLPClassifier.
MLPClassifier stands for Multi-layer Perceptron classifier which in the name itself connects to a Neural Network. Unlike other classification algorithms such as Support Vectors or Naive Bayes Classifier, MLPClassifier relies on an underlying Neural Network to perform the task of classification.
We used an ensemble of xgboost and random forest and we got a precision of 0.03 and f1-score of 0.05 for the minority class.

###### Neural Network -
Here we used ADASYN which is supposed to be a better oversampling tool than SMOTE.
We then implemented an ANN which has 4 dense layers - 
first layer had 250 neurons with relu activation
second layer had 200 neurons with relu activation
third layer had 150 neurons with relu activation
fourth layer had 1 neuron with sigmoid activation
We used the adam optimizer and fit the model and ran for 50 epochs.
We got a precision of 0.02 and f1-score of 0.04 for the minority class.

---------------------------------------------------------------------------------------------

## Machine Learning Part 3 - 

###### Now we tried undersampling since oversampling was not working.
We only undersampled the training data here because again if we were undersampling both the sets of data we were getting really promising results but it isn't considered the best practice.
We were a bit hesistant to use undersampling because that meant that most of our data would go to waste but we tried anyways and undersampling is not preffered.

###### Random Forest -
We got a precision of 0.01 and f1-score of 0.01 for the minority class.

###### Linear Regression - 
When we undersampled both the sets we got a precision of 0.70 and f1-score of 0.79 for the minority class.
When we undersampled only the training set we got similar results.

###### Cost Sensitive Learning - 
Cost-sensitive learning is a subfield of machine learning that addresses classification problems where the misclassification costs are not equal.
We assigned a weight of 1 to the majority class and a weight of 500 for the minority class.
Here we got a roc_auc_score of 0.76 which is okay. We didn't pursue this further but this was promising and we will try improving it later.

---------------------------------------------------------------------------------------------

## Trying to find new features - 

During the cost sensitive learning time we tried plotting the graph to visualise the data. We plotted a graph of gap_hours X spherical_distance and saw that the anomalies (vessels that have been caught) weren't really outliers but they lied right in the middle of the normal data. That's why all the algorithms weren't performing well.
That made sense because obviously if someone wanted to do illegal activities they won't disable their AIS for 10,000 hours.
So we tried to come up with more features and improve our existing features - 
###### Improvements -
*vessel_type* - this feature mostly had only 3-4 values and majority of the vessels were classified as others. So we wrote a code to find the gear_type using the MMSI number and inputing it in the Global fishing watch API.
Here, we could not pass all 55,000 values to the API since that would be wasteful and the API only allows only 50,000 values per day per email id and since it we had only 5000 unique MMSI we extracted them from our data and found all the data for them, this was faster and took less time. after that we compiled them in an CSV and then put it for every MMSI in the original data. 

*Ocean* - As stated above we had to merge 2 datasets to get the oceans where the AIS was disabled, but we wanted to get the even more detail here the exact name of the ocean rather than just 3-4 oceans repeating over and over again.
We tried visualising the data using Tableau and found that the vessels that were getting classified as False (meaning their lat and long did not lie any ocean) all belonged to the Pacific ocean because the international date line crosses the pacific ocean and the long of the changes. 
Lat ranges from +90 to -90 and Long ranges from +180 to -180.
Since we were trying to find if the lat and long lies inside a polygon the max and min long were posing a problem that's why all the co-ordinates to the east of the international date line were getting misclassified as False. Then we tried finding the issue and fixed it by finding the JSONs of all the small seas and finding the points that lied in them.
So, now we had all the exact names of the oceans so that's 2 improvements done in existing attributes.

###### New Features - 
Gap hours * spherical distance - we added another feature that multiplied these 2 attributes as it gives a better understanding.
Score - when we were finding the gear type to improve the vessel type by using the GFW API, we saw we were getting a score as a response in the API. So we added that as well. We don't know exactly what that is and we have emailed them asking for clarification on the matter. 

We also tried finding more vessels that have been caught doing IUU activities and searched quite a lot on the internet trying to manually find vessels that have been caught and whose IMO or MMSI is available. If IMO is available then we tried finding the MMSI using the API. If we found the MMSI we checked if it existed in our dataset and changed it's IUU_check to 1.
Zhe Dai Yu (MMSI 900412888) - https://globalfishingwatch.org/wp-content/uploads/GFW-2021-FA-SQUID2020-EN1-4.pdf
Oyang 77, Lu Rong Yuan Yu 668 - https://www.science.org/doi/10.1126/sciadv.abq2109
https://www.reuters.com/article/us-argentina-defense-china-idUSKCN0WH2QL
https://osf.io/preprints/marxiv/juh98/
https://es.mongabay.com/2020/05/oceanos-pesca-ilegal-en-argentina/

There are some countries which don't have RFMOs so finding the vessels that have been caught is very challenging but we got a couple of successes and got about 60-70 more datapoints that we could train on.

---------------------------------------------------------------------------------------------

## Machine Learning Part 4 - 

We used ADASYN to oversample the training data and we used a train/test split of 60/40

###### Random Forest -
We got a precision of 0.18 and f1-score of 0.22 for the minority class, which is a good improvement.

###### Ensemble learning - 
We tried ensemble methods as they use multiple learning algorithms to obtain better predictive performance than could be obtained from a single method.
We used an ensemble of xgboost and random forest and we got a precision of 0.12 and f1-score of 0.19 for the minority class.

###### Stacking Classifier - 
A stacking classifier is an ensemble learning method that combines multiple classification models to create one “super” model. This can often lead to improved performance, since the combined model can learn from the strengths of each individual model.
Here we used random forest, xgboost and ANN with the final estimator as MLPClassifier.
MLPClassifier stands for Multi-layer Perceptron classifier which in the name itself connects to a Neural Network. Unlike other classification algorithms such as Support Vectors or Naive Bayes Classifier, MLPClassifier relies on an underlying Neural Network to perform the task of classification.
We used an ensemble of xgboost and random forest and we got a precision of 0.11 and f1-score of 0.19 for the minority class.

Overall, this was an improvement.
