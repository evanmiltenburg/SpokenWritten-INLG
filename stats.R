library(lme4)
library(lmerTest)

modality_data = read.csv("XXXXXX/Spoken-vs-Written/Analysis/Prepared/overall_stats.csv")

# Manipulate data: replace values higher than 1 with 1, 
modality_data$selfref_capped <- replace(modality_data$self_reference_words, 
                                        modality_data$self_reference_words >= 1,
                                        1)

modality_data$allness_capped <- replace(modality_data$positive_allness, 
                                        modality_data$positive_allness >= 1, 
                                        1)

sink("all_output.txt")

##################################################################
# Standard Lmer models

length.model = lmer(length ~ modality + (1|participant) + (1|image), 
                    data=modality_data)

pid.model = lmer(PID ~ modality + (1|participant) + (1|image), 
                 data=modality_data)

# Did not converge with the default optimizer, but did converge with bobyqa.
syll.model = lmer(syllables ~ modality + (1|participant) + (1|image), 
                  data=modality_data, control=lmerControl(optimizer = "bobyqa"))

chars.model = lmer(chars ~ modality + (1|participant) + (1|image), 
                   data=modality_data)

##################################################################
# Count models - using the poisson distribution

adverbs.model = glmer(adverbs ~ modality + (1|participant) + (1|image), 
                      data=modality_data, family = "poisson")

prepositions.model = glmer(prepositions ~ modality + (1|participant) + (1|image), 
                          data=modality_data, family="poisson")

attributives.model = glmer(attributives ~ modality + (1|participant) + (1|image), 
                           data=modality_data, family = "poisson")

cop.model = glmer(consciousness_of_projection ~ modality + (1|participant) + (1|image), 
                 data=modality_data, family = "poisson")

# Does not converge:
# self_reference.model = glmer(self_reference_words ~ modality + (1|participant) + (1|image), 
#                              data=modality_data, family = "poisson")

selfref_capped.model = glmer(selfref_capped ~ modality + (1|participant) + (1|image), 
                             data=modality_data, family = "binomial")

negations.model = glmer(negations ~ modality + (1|participant) + (1|image), 
                            data=modality_data, family = "poisson")

pq.model = glmer(pseudo_quantifiers ~ modality + (1|participant) + (1|image), 
                       data=modality_data, family = "poisson")

# Does not converge:
# allness.model = glmer(positive_allness ~ modality + (1|participant) + (1|image), 
#                       data=modality_data, family = "poisson")

allness.model = glmer(allness_capped ~ modality + (1|participant) + (1|image), 
                      data=modality_data, family = "binomial")

##################################################################
# Summaries

summary(length.model)

summary(adverbs.model)

summary(allness.model)

summary(attributives.model)

summary(chars.model)

summary(cop.model)

summary(negations.model)

summary(pid.model)

summary(pq.model)

summary(self_reference.model)

summary(syll.model)

sink()

summary(length.model)
