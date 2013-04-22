import requests, json, sys, os
from datetime import date, timedelta


def get_auth_info(email, password):
	request_data = {
		'email': email,
		'pwd': password,
		'service': 'nudge'
	}

	response = requests.post("https://jawbone.com/user/signin/login", request_data)
	content = json.loads(response.content)
	token = content["token"]
	xid = content["user"]["xid"]
	return {
		'xid': xid,
		'token': token
	}


global_data = {}
def get_week_data(data_fn):
	global global_data

	week_data = []
	i = 0
	while i < 7:
		date_str = (date.today() - timedelta(i)).strftime("%Y%m%d")
		if date_str in global_data:
			date_data = global_data[date_str]
		else:
			date_data = get_data(auth_info["xid"], auth_info["token"], date_str)
			global_data[date_str] = date_data
		date_specific = data_fn(date_data)
		date_json = {
			"title": (date.today() - timedelta(i)).strftime("%A"),
			"value": date_specific
		}
		week_data.insert(0, date_json)

		i += 1

	return week_data


def get_data(xid, token, date):
	headers = {
		'x-nudge-token': token
	}

	params = {
		'date': date
	}

	response = requests.get("https://jawbone.com/nudge/api/v.1.31/users/{0}/score".format(xid), headers=headers, params=params)
	content = json.loads(response.content)
	return content


def get_step_data(data):
	return data["data"]["move"]["bg_steps"]


def get_sleep_data(data):
	sleep_time = data["data"]["sleep"]["goals"]["total"][0]
	sleep_time = sleep_time/60/60
	return sleep_time


def get_deep_sleep_data(data):
	deep_sleep = data["data"]["sleep"]["goals"]["deep"][0]
	deep_sleep = deep_sleep/60/60
	return deep_sleep


def get_data_sequences(titles, datapoints):
	json_data = []
	for i,title in enumerate(titles):
		d = {
			"title": title,
			"datapoints": datapoints[i]
		}
		json_data.append(d)
	return json_data


def create_status_board_json(data_sequences):
	json_data = json.dumps({
		"graph": {
			"title": "Jawbone UP",
			"type": "line",
			"datasequences": data_sequences
		}
	})
	return json_data


def save_json_data(filename, data):
	f = open("data/{0}.js".format(filename), "w")
	f.write(data)
	f.close()


def init(pr, em, pa):
	global prefix
	global email
	global password
	prefix = pr
	email = em
	password = pa

	global auth_info
	auth_info = get_auth_info(email, password)


def get_steps():
	week_data = get_week_data(get_step_data)
	data_sequences = get_data_sequences(["Steps"], [week_data])
	json_data = create_status_board_json(data_sequences)
	save_json_data("up_{0}_steps".format(prefix), json_data)


def get_sleep():
	total_sleep_data = get_week_data(get_sleep_data)
	deep_sleep_data = get_week_data(get_deep_sleep_data)
	data_sequences = get_data_sequences(["Sleep", "Deep Sleep"], [total_sleep_data, deep_sleep_data])
	json_data = create_status_board_json(data_sequences)
	save_json_data("up_{0}_sleep".format(prefix), json_data)

