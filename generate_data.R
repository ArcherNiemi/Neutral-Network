library("ggplot2")

n <- 1000
spikes <- runif(n)
spots  <- runif(n)

expit <- function(eta) 1/(1+exp(-eta))

# tuning parameter (higher is stricter threshold)
tp <- 100

poisonous <- rbinom(n, size = 1, 
                    prob = expit(tp*spikes - tp*spots))

d <- data.frame(
  spikes = spikes,
  spots  = spots,
  poisonous = poisonous
)

ggplot(d, aes(x = spots, y = spikes, 
              color = poisonous)) + 
  geom_point()

write.csv(d, file = "poisonous.csv", row.names = FALSE)


# m <- glm(poisonous ~ spots + spikes, 
#          family = "binomial")
#
# summary(m)


# Circular data
d <- d |>
  mutate(
    poisonous = ifelse( (spikes-0.5)^2 + (spots-0.5)^2 < 0.3^2, 1, 0)
  )
write_csv(d |> select(spikes, spots, poisonous), "poisonous_circular.csv")
