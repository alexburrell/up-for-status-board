# Add a Jawbone UP panel to your Status Board

This is just a quick script I put together to pull sleep and activity data from my Jawbone UP bracelet and display it as a panel on Panic's Status Board app.

As is, with your user credentials, it can create a JSON object to get a line graph of your steps on Status Board, or a line graph of your sleep and deep sleep.

## Using this script

I created a python file for each person, that looks something like this:

```python
import up

up_data = {
	"email": "EMAIL FOR UP",
	"password": "PASSWORD FOR UP"
}

file_prefix = "MY FIRST NAME"

up.init(file_prefix, up_data["email"], up_data["password"])
up.get_steps()
up.get_sleep()
```

(Now with these files, if we create more Status Board widgets, we can generate the JSON objects for each of us from here too.)

## Generating different graphs

The script gets one block of data back for each day, which it then parses for steps, total sleep, and deep sleep. If you want different information from that day, create get_NEWDATA() and pass a different parsing function to the get_week_data function.

For example:

```python
def get_NEWDATA_data(data):
	return data["PARSE"]["FOR"]["NEW"]["DATA"]

def get_NEWDATA():
	week_data = get_week_data(get_NEWDATA_data)
	data_sequences = get_data_sequences(["NEW DATA"], [week_data])
	json_data = create_status_board_json(data_sequences)
	save_json_data("up_{0}_NEWDATA".format(prefix), json_data)
```

## What data do we get for each day?

Here is roughly (zero'd out) the model for the JSON object that we get back for each day:

```javascript
{
	"meta": {
		"user_xid": "", 
		"message": "", 
		"code": 0, 
		"time": 0
	}, 
	"data": {
		"mood": 0, 
		"move": {
			"distance": 0, 
			"longest_idle": 0, 
			"calories": 0, 
			"bg_steps": 0, 
			"goals": {
				"steps": [0, 0], 
				"workout_time": [0, 0]
			}, 
			"longest_active": 0, 
			"hidden": 0, 
			"bmr_calories_day": 0, 
			"bmr_calories": 0, 
			"active_time": 0
		}, 
		"sleep": {
			"awakenings": 0, 
			"light": 0, 
			"time_to_sleep": 0, 
			"goals": {
				"total": [0, 0], 
				"bedtime": [0, 0], 
				"deep": [0, 0]
			}, 
			"qualities": [0], 
			"awake": 0, 
			"hidden": 0
		}, 
		"insights": {
			"items": [
				{
					"head": "", 
					"timestamp": 0, 
					"liked": 0, 
					"source_url": "", 
					"action_url": "", 
					"group": "", 
					"category": "", 
					"feedback_count": 0, 
					"xid": "", 
					"title": "", 
					"text": ""
				}
			]
		}, 
		"meals": {
			"num_meals": 0, 
			"calories": 0, 
			"num_drinks": 0, 
			"goals": {
				"calcium": [0, 0], 
				"carbs": [0, 0], 
				"fiber": [0, 0], 
				"unsat_fat": [0, 0], 
				"sodium": [0, 0], 
				"cholesterol": [0, 0], 
				"protein": [0, 0], 
				"sugar": [0, 0], 
				"sat_fat": [0, 0]
			}, 
			"hidden": 0, 
			"num_foods": 0
		}, 
		"user_metrics": {
			"dob": 19890619, 
			"gender": 0, 
			"pal": 0, 
			"weight": 0, 
			"height": 0
		}
	}
}

```

# Disclaimer

The (unofficial) Jawborn UP API was documented a while ago [here](http://eric-blue.com/2011/11/28/jawbone-up-api-discovery/), but in my attempt to use that, I found that it's changed quite a bit. Since Jawbone hasn't released any public API, they could change their patterns anytime and this script will need to be updated or break.