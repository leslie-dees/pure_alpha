
#get already complete dataset
full_dataframe = pd.read_csv('Account_Info.csv', index_col=[0])
print(full_dataframe)

#get screen names of new projects
twitter_handles_list = list_of_rows[1:, 1]
twitter_names_list = []
for twitter_name in twitter_handles_list:
    twitter_names_list.append(twitter_name[20:])

#if project already complete do not run again
screen_and_id_list = []
for screen_name in twitter_names_list:
    if 1:
        print(screen_name + ' already contained')
    else:
        my_screen_and_id = get_user_data(screen_name)
        screen_and_id_list.append(my_screen_and_id)
print(screen_and_id_list)

new_dataframe = pd.DataFrame(screen_and_id_list, columns = ['screen_name', 'id', 'followers_count', 'following_count'])
full_dataframe = pd.concat([full_dataframe, new_dataframe])


full_dataframe.to_csv('Account_Info.csv')

