import os

from dotenv import load_dotenv

load_dotenv()

linear_endpoint = 'https://api.linear.app/graphql'
linear_api_key = os.getenv('LINEAR_API_KEY')
linear_headers = {'Authorization': f'Bearer {linear_api_key}'}

# https://studio.apollographql.com/public/Linear-API/schema/reference/objects/Project?query=Project&variant=current
projects_query = """
query Projects {
    projects {
        nodes {
            id
            name
            description
            members {
                nodes {
                    email
                }
            }
        }
    }
}
"""

# This might vary depending on your configuration on Linear
statuses = {
  "Backlog": {
    "resolved": False,
    "color": "eeeeee"
  },
  "Todo": {
    "resolved": False,
    "color": "444444"
  },
  "In Progress": {
    "resolved": False,
    "color": "eeff44"
  },
  "On Hold": {
    "resolved": False,
    "color": "ef5524"
  },
  "In Review": {
    "resolved": False,
    "color": "069420"
  },
  "Done": {
    "resolved": True,
    "color": "0053e2"
  },
  "Cancelled": {
    "resolved": True,
    "color": "999999"
  }
}