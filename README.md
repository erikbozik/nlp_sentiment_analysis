# Slovak Sentiment Analysis

## Goal
We would like to train our own model like LSTM as our first attempt. In our second attempt we would use some pre-trained multilingual models like BERT. We would like to get our training data from an already existing dataset published for example on hugging face or similar websites. Our approach involves using a pre-trained multilingual model and fine-tuning it specifically for the Slovak language to perform sentiment analysis. This strategy aims to leverage the comprehensive language understanding capabilities of models like mBERT while adapting them to the nuances of Slovak sentiment expression.

## Update
Our first idea was to do sentiment analysis for the Slovak language. However, there is not enough data for sentiment analysis in the Slovak language. Therefore we came up with an idea to develop three different models each with different data sources. Firstly we would generate synthetic data from generative ai (GPT). Next, we would get a dataset in a foreign language and then translate it to the Slovak language using some other model specialized for translation (T5). The third data source is web-scraping reviews from websites like Heureka. Then we would train the models on three different data sources and also with different types of models. As we mentioned previously the training would be done firstly from scratch and then by fine-tuning some already existing models which are not very robust as we have limited computational power. We plan to come up with 6 differently trained models. Then we would evaluate the performance of each model and compare them to say what was successful and what wasn't. In this approach, we would aim only for the Slovak language. We extended the data sources so the project is bigger in this way when compared to our first thoughts.

## Translating
We used data from http://thinknook.com/twitter-sentiment-analysis-training-corpus-dataset-2012-09-22/. All the information about the dataset can be found on the website.
We created a local FastAPI app that enhances nvidia cuda and translation model from huggingface https://huggingface.co/michaelfeil/ct2fast-m2m100_1.2B.
Running the translation model on the dataset was time and gpu consuming considering the fact that we chose to run locally.
The code crashed multiple times due to cuda runtime error which forced us to create multiple batches of data.
We translated <mark> ADD THE AMOUNT OF LINES IN THE DATA </mark> from the original data. The api crashed multiple times regardless of batching so the final dataframe had to be concatenated together from mutliple translated parts.
