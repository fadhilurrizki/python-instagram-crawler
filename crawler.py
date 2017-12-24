import requests
import csv
import os
import sys
import json
import pandas as pd

def flattenjson( b, delim ):
    val = {}
    for i in b.keys():
        if isinstance( b[i], dict ):
            get = flattenjson( b[i], delim )
            for j in get.keys():
                val[ i + delim + j ] = get[j]
        else:
            val[i] = b[i]

    return val

def WriteDictToCSV(csv_file,csv_columns,dict_data):
        with open(csv_file, 'w') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=csv_columns)
            writer.writeheader()
            for data in dict_data:
                writer.writerow(data)

def main():
	if(len(sys.argv) == 3):
		currentPath = os.getcwd()
		# auth
		access_token = str(sys.argv[1])
		username = str(sys.argv[2])
		print("Access Token : " + access_token)
		print("Getting General Info..")
		#get general info
		url_get = "https://api.instagram.com/v1/users/self/?access_token=" + access_token
		general_info = requests.get(url_get).json()
		flat = flattenjson(general_info['data'], "_")
		columns = list(set(flat.keys()))
		csv_file = currentPath + "/" + username + "-info.csv"
		#WriteDictToCSV(csv_file,columns,[flat])
		normalized = pd.io.json.json_normalize(general_info['data'])
		normalized.to_csv(csv_file)
		#with open('user_profile.json', 'w') as outfile:
		#	json.dump(general_info['data'],outfile) 
		print("done.")
		#get recent posts
		print("Getting Recent Posts...")
		url_get = "https://api.instagram.com/v1/users/self/media/recent/?access_token=" + access_token + "&count=1000000"
		posts = requests.get(url_get).json()
		flat = posts['data']
		columns = list(set(flat[0].keys()))
		csv_file = currentPath + "/" + username + "-posts.csv"
		#WriteDictToCSV(csv_file,columns,flat)
		#with open('user_posts.json', 'w') as outfile:
		#	json.dump(posts['data'],outfile) 
		normalized = pd.io.json.json_normalize(posts['data'])
		normalized.to_csv(csv_file)
		#get user likes of post
		print("Getting User likes of posts...")
		ids = [x['id'] for x in flat]
		for id in ids:
			url_get = "https://api.instagram.com/v1/media/" + id + "/likes?access_token=" + access_token
			posts = requests.get(url_get).json()
			flat = posts['data']
			columns = list(set(flat[0].keys()))
			csv_file = currentPath + "/likes/" + username + "-posts_" + id + ".csv"
			#WriteDictToCSV(csv_file, columns, flat)
			#with open(currentPath + '/likes/json/user_post_'+id+'.json', 'w') as outfile:
			#	json.dump(posts['data'],outfile)
			normalized = pd.io.json.json_normalize(posts['data'])
			normalized.to_csv(csv_file)
	else :
		print("access token not found. try again 'python3 crawler.py ACCESS_TOKEN'")

if __name__ == "__main__": main()