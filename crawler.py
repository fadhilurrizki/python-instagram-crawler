import requests
import csv
import os
import sys
import json
import pandas as pd


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
		csv_file = currentPath + "/" + username + "-info.csv"
		normalized = pd.io.json.json_normalize(general_info['data'])
		normalized.to_csv(csv_file)
		print("done.")
		#get recent posts
		print("Getting Recent Posts...")
		url_get = "https://api.instagram.com/v1/users/self/media/recent/?access_token=" + access_token + "&count=1000000"
		posts = requests.get(url_get).json()
		csv_file = currentPath + "/" + username + "-posts.csv"
		normalized = pd.io.json.json_normalize(posts['data'])
		normalized.to_csv(csv_file)
		#get user likes of post
		print("Getting User likes of posts...")
		ids = [x['id'] for x in posts['data']]
		for id in ids:
			url_get = "https://api.instagram.com/v1/media/" + id + "/likes?access_token=" + access_token
			posts = requests.get(url_get).json()
			csv_file = currentPath + "/likes/" + username + "-posts_" + id + ".csv"
			normalized = pd.io.json.json_normalize(posts['data'])
			normalized.to_csv(csv_file)
			url_get = "https://api.instagram.com/v1/media/" + id + "/comments?access_token=" + access_token
			posts = requests.get(url_get).json()
			flat = posts['data']
			if(len(flat) != 0):
				csv_file = currentPath + "/comments/" + username + "-posts_" + id + ".csv"
				normalized = pd.io.json.json_normalize(posts['data'])
				normalized.to_csv(csv_file)	
	else :
		print("access token not found. try again 'python3 crawler.py ACCESS_TOKEN'")

			
if __name__ == "__main__": main()