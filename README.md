# Rating Tourniquet for Lichess

Libraries requiring pip install:
python-lichess

# Purpose and Functionalities
## Overview
**Rating Tourniquet** is a Python-based application designed to help online chess players manage their rating effectively on the Lichess platform. The primary purpose of this app is to "stop rating bleeding," which refers to the phenomenon where players experience a decline in their ratings due to consistent losses over a period.
### What is Rating in Online Chess?
In online chess, a player's rating is a numerical representation of their skill level, calculated based on their performance in games against other players. Higher ratings indicate stronger players. When a player loses games, their rating decreases, which can be frustrating and demotivating. Rating Tourniquet aims to mitigate this issue by temporarily blocking access to Lichess during hours when the user is statistically more likely to lose games, thus protecting their rating from significant drops.
## Technical Details
### Development Language
The app is developed in **Python**, utilizing the popular `python-lichess` library to interact with the Lichess API. This enables seamless integration and functionality, allowing users to analyze their chess games effectively.
### Functionality
The application requires the user to input their Lichess username and preferred time control. Based on this information, the app analyzes the user's performance and identifies time periods where they tend to lose rating. Once this analysis is complete, Rating Tourniquet will automatically block access to Lichess during these identified hours, thus preventing the user from playing and losing additional rating points.
### How to Run the Application
Rating Tourniquet is designed to be run in the Linux command line. To execute the application, you must have root privileges. The command to run the app is as follows:
**sudo python3 path/to/rating_tourniquet.py**
Replace path/to/rating_tourniquet.py with the actual path where the script is located. Running the app with sudo is necessary as it may require elevated permissions to execute certain operations, particularly when interfacing with system-level functions or making network requests.
#### User input parameters
The application utilizes argparse to handle user input efficiently. The following command-line arguments can be provided:
    * -u or --username: This is a required parameter where the user must enter their Lichess username. The app will use this to fetch the user's game data.
    * -c or --control: Another required parameter that allows the user to specify their preferred time control. The options are:
            * Bullet: Fast-paced games with a short time limit.
            * Blitz: Slightly longer than bullet but still quick.
            * Rapid: Games with a longer time control.
            * Standard: Traditional time controls that allow for in-depth play.
    * -s or --sample: This optional parameter defines the maximum number of games that will be analyzed. By default, it is set to 1000 games, allowing the app to have a broad dataset for performance analysis.
    * -t or --threshold: This optional parameter specifies the rating loss threshold. If the user loses more than this specified amount of rating during a given hour, the app will block access to Lichess for that hour. The default threshold is set to 0, meaning any rating loss will trigger the block.
## Conclusion
Rating Tourniquet is a powerful tool for online chess players looking to safeguard their ratings on Lichess. By analyzing user performance and preventing play during less favorable hours, it provides a proactive approach to maintaining a healthy chess rating. Whether you’re a casual player or a competitive one, this app can help you keep your rating in check and enhance your overall online chess experience.
## Acknowledgements
Special thanks to ChatGPT for assistance in writing this README file.
