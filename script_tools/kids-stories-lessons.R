library(tidyverse)
library(ggplot2)


stories <- read_csv2("data/ChatGPT-Childrens-stories.csv")

stories %>%
  ggplot(aes(x = Friendship, y = Nationality)) +
  geom_point() +
  labs(x = "Nationality", y = "Friendship") +
  ggtitle("Whisker Plot of Friendship by Nationality")



summary_table <- stories %>%
  group_by(Nationality) %>%
  summarize(across(Friendship:Nature, sum, na.rm = TRUE))

# Melt the summary_table to convert it into long format
melted_table <- tidyr::pivot_longer(summary_table, cols = -Nationality, names_to = "Variable", values_to = "Sum")

# Create the plot
ggplot(melted_table, aes(x = Variable, y = Sum, color = Nationality, group = Nationality)) +
  geom_line() +
  labs(x = "Variable", y = "Sum", color = "Nationality") +
  ggtitle("Sum of Variables by Nationality") +
  coord_flip() 

#---- only big nations

library(ggplot2)

# Filter the summary_table for specific nationalities
filtered_table <- summary_table %>%
  filter(Nationality %in% c("American", "British", "Indian", "Australian"))

# Melt the filtered_table to convert it into long format
melted_table <- tidyr::pivot_longer(filtered_table, cols = -Nationality, names_to = "Variable", values_to = "Sum")

# Create the plot
ggplot(melted_table, aes(x = Variable, y = Sum, color = Nationality, group = Nationality)) +
  geom_line() +
  labs(x = "Variable", y = "Sum", color = "Nationality") +
  ggtitle("Sum of Variables by Nationality") +
  coord_flip()

# HEATMAP

library(ggplot2)

# Create the heatmap
library(ggplot2)

# Get the list of variable names
variable_names <- names(summary_table)[-1]  # Exclude the first column (Nationality)

stories %>% 
  group_by(Nationality) %>% 
  summarise_all()

stories %>% 
  filter(Nationality==c("American", "British", "Indian", "Australian", "Nigerian")) %>% 
  pivot_longer(!Nationality)
  ggplot(aes(x=fct_infreq(Nationality))) +
  geom_bar() +
  labs(fill="", 
       title ="",
       subtitle = "Includes technologies that are involved in more than 200 interactions and verbs used more than 5 times",
       caption = "Based on Rettberg et.al. 2022. A Dataset Documenting Representations of Machine Vision Technologies in Artworks, Games and Narratives. http://doi.org/10.18710/2G0XKN",
       y = "", 
       x = "") +
  theme_minimal() +
  coord_flip() +
  facet_wrap(~fct_infreq(Technology), scales="free_y")





# Calculate total count for each Nationality
total_counts <- stories %>%
  group_by(Nationality) %>%
  summarise(total = n())

# Calculate the sum for each Nationality across specified columns and then join with total_counts
stories %>%
  group_by(Nationality) %>%
  summarise(across(Friendship:Nature, sum, na.rm = TRUE)) %>%
  inner_join(total_counts, by = "Nationality") %>%
  mutate(across(Friendship:Nature, ~ . / total)) %>%
  select(-total)

stories %>% 
  select(Nationality)

df <- stories %>%
  group_by(Nationality) %>%
  summarise(across(Friendship:Nature, sum, na.rm = TRUE)) %>%
  inner_join(total_counts, by = "Nationality") %>%
  mutate(across(Friendship:Nature, ~ . / total)) %>%
  pivot_longer(cols = Friendship:Nature, names_to = "Category", values_to = "Weighted_Count") %>%
  select(-total)

df <- stories %>%
  filter(Nationality %in% c('Australian', 'American', 'Indian', 'Nigerian')) %>%
  select(-Love, -Dreams, -Diversity, -`Self-belief`) %>% 
  group_by(Nationality) %>%
  summarise(across(Friendship:Nature, sum, na.rm = TRUE)) %>%
  inner_join(total_counts, by = "Nationality") %>%
  mutate(across(Friendship:Nature, ~ . / total)) %>%
  pivot_longer(cols = Friendship:Nature, names_to = "Category", values_to = "Weighted_Count") %>%
  select(-total)

df <- stories %>%
  filter(Nationality %in% c('Indigenous Australian', 'African-American')) %>%
  select(-Love, -Dreams, -Diversity, -`Self-belief`) %>% 
  group_by(Nationality) %>%
  summarise(across(Friendship:Nature, sum, na.rm = TRUE)) %>%
  inner_join(total_counts, by = "Nationality") %>%
  mutate(across(Friendship:Nature, ~ . / total)) %>%
  pivot_longer(cols = Friendship:Nature, names_to = "Category", values_to = "Weighted_Count") %>%
  select(-total)

ggplot(df, aes(x = Category, y = Weighted_Count, fill = Nationality)) +
  geom_bar(stat = "identity", position = position_dodge()) +
  facet_wrap(~Nationality, scales = "free") +
  theme(axis.text.x = element_text(angle = 45, hjust = 1)) +
  labs(x = "Lessons learned", y = "Weighted Count", fill = "Nationality")

