import pandas as pd
import math
import json

with open('back_end_dev/json_6.json', 'r') as f:
    dict_map = json.load(f)

list_all_cases = []
dict_temp_similarity = {}
for s in dict_map[0]['States']:
    state = s['Name']
    dict_temp_similarity['state'] = state
    for c in s['Cities']:
        # print(c)
        for vote in c['Responses']['Vote'].keys():
            # dict_temp_similarity = {}
            dict_temp_similarity['city'] = c['Name']
            dict_temp_similarity['vote'] = vote
            responses_vote = c['Responses']['Vote'][vote]
            for fruit in c['Responses']['Fruit'].keys():
                dict_temp_similarity['fruit'] = fruit
                responses_fruit = c['Responses']['Fruit'][fruit]
                for education in c['Responses']['Education'].keys():
                    dict_temp_similarity['education'] = education
                    responses_education = c['Responses']['Education'][education]
                    # print(education)
                    for park in c['Responses']['Parks'].keys():
                        dict_temp_similarity['park'] = park
                        responses_park = c['Responses']['Parks'][park]
                        for insured in c['Responses']['Insured'].keys():
                            dict_temp_similarity['insured'] = insured
                            responses_insured = c['Responses']['Insured'][insured]

                            ## distance
                            dist = math.sqrt(responses_vote ** 2 +
                                             responses_fruit ** 2 +
                                             responses_education ** 2 +
                                             responses_insured ** 2 +
                                             responses_park ** 2)



                            ## similarity
                            min_max = eval(c['min_max'])
                            metro_dist_min = min_max[0]
                            metro_dist_max = min_max[1]

                            # print('')
                            # print(dist)
                            # print(metro_dist_min)
                            # print(metro_dist_max)

                            similarity = (1 - (dist - metro_dist_min) / (metro_dist_max - metro_dist_min)) * 100

                            # print(similarity)

                            if similarity > 100:
                                similarity = 100
                            if similarity < 0:
                                similarity = 0

                            dict_temp_similarity['similarity'] = round(similarity, 2)

                            ## test test
                            # print(vote)
                            if ("Fayetteville" in c['Name']) and \
                                    (insured == 'No') and \
                                    (park == 'No') and \
                                    (vote == 'YES') and \
                                    (fruit == '2.0') and \
                                    (education == 'ASSOCIATE DEGREE-OCCUPATIONAL/VOCATIONAL'):
                                print(similarity)
                                print(dict_temp_similarity)
                                print(responses_vote,
                                      responses_fruit,
                                      responses_education,
                                      responses_insured,
                                      responses_park)
                                # print(min_max)
                                # print(dist)
                            ##


                            # print(dict_temp_similarity['education'])

                            list_all_cases.append(dict_temp_similarity.copy())

len(list_all_cases)
df_all_similarities = pd.DataFrame(list_all_cases)

df_tests = df_all_similarities.sample(n=100, random_state=198)

df_all_similarities.to_csv('back_end_dev/similarities_all_combinations_2.csv', index=False)
df_tests.to_csv('back_end_dev/similarities_100_combinations_2_1.csv', index=False)
