import requests
albb_url = 'http://chart.finance.yahoo.com/table.csv?s=BABA&a=7&b=7&c=2016&d=8&e=7&f=2016&g=d&ignore=.csv'

def download_stock_data(csv_url):
	response = requests.get(csv_url)
	csv = response.read()
	csv_str = str(csv)
	lines = csv_str.split("\\n")
	dest_url = r'albb.csv'
	fx = open(dest_url, "w")
	for line in lines:
		fx.write(line + "\n")
	fx.close()

download_stock_data(albb_url)