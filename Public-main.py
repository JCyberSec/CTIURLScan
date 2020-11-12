#Import Table
import argparse
import json
import requests
import os
import urllib.request
import time



#Global Variables
global APIKey
APIKey = "XXXX-XXXX-XXXXX-XXXX-XXXXX"


## Argparse Arguments
parser = argparse.ArgumentParser(description="Wrapper for urlscan.io's API")
subparsers = parser.add_subparsers(help='commands', dest='command')


# Search Parser
parser_search = subparsers.add_parser('search', help='Search urlscan')
parser_search.add_argument('-t', '--term', help='Search term to search for - page.url:google.com', required='True')
parser_search.add_argument('-s', '--size', help='Number of items to return - Default 96', default=96)
parser_search.add_argument('-d', '--date', help='Date range to search - 24h, 30d, 90d', default="24h")
parser_search.add_argument('-e', '--extract', help='Define key to extract - URL, IP, Domain')


# Retrieve Parser
parser_retrieve = subparsers.add_parser('collect', help='Retrieve scan results')
parser_retrieve.add_argument('-u', '--uuid', help='UUID(s) to retrieve scans for', nargs='+', required='True')
parser_retrieve.add_argument('-d', '--dom', help='Print DOM object to screen', action="store_true")
parser_retrieve.add_argument('-s', '--screenshot', help='Save screenshot as png', action="store_true")
parser_retrieve.add_argument('-v', '--dump', help='Dump full scan result to screen ', action="store_true")

args = parser.parse_args()

def download_dom(target_uuid):
	try:
		response = requests.get('https://urlscan.io/dom/{}'.format(target_uuid))
		result = response.content.decode("utf-8")
		print (result)
	except Exception as e:
		print ("Failed to download DOM for {}".format(target_uuid))
		pass
	

def download_png(target_uuid, target_dir, save_template):
	try:
		os.makedirs(target_dir)
	except FileExistsError:
		pass
	target_png = save_template + '.png'
	try:
		urllib.request.urlretrieve(str('https://urlscan.io/screenshots/{}.png'.format(target_uuid)), str(target_png))
	except Exception as e:
		print ("Unable to download screenshot")
		print (e)


def query(uuid):
	for target_uuid in uuid:

		response = requests.get("https://urlscan.io/api/v1/result/{}".format(target_uuid))
		status = response.status_code
		
		if status != requests.codes.ok:
			if status == 429:
				time.sleep(1)
				response = requests.get("https://urlscan.io/api/v1/result/{}".format(target_uuid))
				status = response.status_code
			else:
				print('Results not processed. Please check again later. Status {} - {}'.format(status,target_uuid))
		if status == requests.codes.ok:		
			r = response.content.decode("utf-8")

			url = response.json().get("task").get("url").split("://")[1]
			submission_time = response.json().get("task").get("time")
			path = os.getcwd()
			save_template = path + '/' + submission_time + '_' + target_uuid
			
			if args.dom:
				download_dom(target_uuid)
			if args.screenshot:
				download_png(target_uuid, path, save_template)
			if args.dump:
				print(r)

		time.sleep(2)


def search(term, size, date, extract):
	if extract:
		extract = extract.lower()
	headers = {'API-Key':APIKey,'Content-Type':'application/json'}
	params = (
		('q', '{} AND date:>now-{}'.format(term, date)),
		('size', '{}'.format(size)),
	)
	response = requests.get('https://urlscan.io/api/v1/search/', params=params, headers=headers)
	result = response.content.decode("utf-8")
	if extract:
		result = json.loads(result)
		for i in range(len(result['results'])):
			success = False
			for key in ("task", "stats", "page"):
				try:
					print(result['results'][i][key][extract])
					success = True
				except:
					pass
			try:
				print(result['results'][i][extract])
				success = True
			except:
				pass
			if not success:
				print ("Unable to find '{}' in results".format(extract))
				break
	else:
		print(result)

def main():
	global APIKey
	if APIKey == "XXXX-XXXX-XXXXX-XXXX-XXXXX":
		print ("Please enter your API key: (The APIKey variable can be modified in the source to bypass this step)")
		APIKey = input ("	[-] ")

	if args.command == 'search':
		search(args.term, args.size, args.date, args.extract)

	if args.command == 'collect':
		query(args.uuid)



if __name__ == '__main__':
	main()