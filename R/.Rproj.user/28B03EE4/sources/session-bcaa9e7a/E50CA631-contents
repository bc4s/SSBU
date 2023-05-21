install.packages("ggplot2")
install.packages("dplyr")
install.packages("glmnet")
library(ggplot2)
library(dplyr)
library(glmnet)

data <- read.csv("diabetes.csv")
summary(data)

x_values <- data[, c("Pregnancies", "Glucose", "BloodPressure", "SkinThickness", "Insulin", "BMI", "DiabetesPedigreeFunction", "Age")]
outcome <- data$Outcome
set.seed(123)

train_dataset <- sample(1:nrow(data), nrow(data) * 0.8)
train_values <- x_values[train_dataset, ]
train_outcome <- outcome[train_dataset]
test <- x_values[-train_dataset, ]
test_outcome <- outcome[-train_dataset]
model <- glm(Outcome ~ ., data = data, family = binomial(link = "logit"))
predicted <- predict(model, newdata = test, type = "response")
binary_predictions <- ifelse(predicted > 0.5, 1, 0)

accuracy <- sum(binary_predictions == test_outcome) / length(binary_predictions)

coefficients <- coef(model)[-1]

coefficient_function <- data.frame(variable = names(coefficients), coefficient = coefficients)

ggplot(coefficient_function, aes(x = variable, y = coefficient)) +
  geom_bar(stat = "identity", fill = "steelblue") +
  xlab("Nezávislé premenné") +
  ylab("Koeficienty") +
  ggtitle("Logisticka regresia")
