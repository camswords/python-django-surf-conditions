# Python play-app: Manly Surf Conditions

A simple Django application demonstrating database integration, using external rest apis, templating and forms. Shows the latest surf conditions in Manly, NSW.

### Getting Started

1. Check out this code
1. Install Python (tested using Python 3.7.3)
1. Create a virtual environment using virtualenv
1. Install Django `pip install Django==2.2`
1. Install requests `pip install requests=2.21`
1. In the code directory in a terminal, run your database migrations `python manage.py migrate`
1. Run your local server `MAGIC_SEAWEED_API_KEY=[API_KEY] python manage.py runserver`
1. In a browser, navigate to http://localhost:8000. This has been tested using Chrome.

### Prerequisites

You will need an API key for MagicSeaweed. This can be requested at [MagicSeaweed](https://magicseaweed.com/developer/forecast-api), or you may have been provided with one if you have been sent here as a code example.

### License
This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details
