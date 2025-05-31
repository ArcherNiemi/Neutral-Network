library("tidyverse")
library("randomForest")
library("nnet")
# library("caret") 

# Functions
accuracy <- function(truth, prediction) {
  round(mean(truth * prediction + (1-truth) * (1-prediction)), 2)
}

# Data
d <- read_csv("poisonous_circular.csv")
ii <- sample(c(TRUE,FALSE), nrow(d), replace = TRUE)
train = d[ ii,]
test  = d[!ii,]

ggplot(d, aes(spikes, spots, color = poisonous)) + 
  geom_point() 

# Logistic regression
m_lr <- glm(poisonous ~ spikes * spots, data = train, family = "binomial") 

test$logistic = predict(m_lr, newdata = test, type = "response") > 0.5 
accuracy(test$poisonous, test$logistic)

prediction_map <- expand.grid(
  spikes = seq(0, 1, length=101),
  spots  = seq(0, 1, length = 101)
) 
prediction_map$probability <- predict(m_lr, newdata = prediction_map, type = "response")
ggplot(prediction_map, aes(spikes, spots, fill = probability)) +
  geom_raster() +
  coord_fixed()





# random forest
m_rf <- randomForest(factor(poisonous) ~ spikes + spots, data = train)
test$randomforest <- as.numeric(predict(m_rf, newdata = test))
accuracy(test$poisonous, test$randomforest)

prediction_map$probability <- predict(m_rf, newdata = prediction_map, type = "response")
ggplot(prediction_map, aes(spikes, spots, fill = probability)) +
  geom_raster() +
  coord_fixed()


# neural network
m_nn <- nnet(poisonous ~ spikes + spots, data = train, size = 8, method = "nnet")
test$nnet <- predict(m_nn, newdata = test) > 0.5
accuracy(test$poisonous, test$nnet)

prediction_map$probability <- predict(m_nn, newdata = prediction_map)
ggplot(prediction_map, aes(spikes, spots, fill = probability)) +
  geom_raster() +
  coord_fixed()



