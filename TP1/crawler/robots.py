import urllib.parse
import urllib.robotparser

def create_robot_parser(start_url):
    parsed_url = urllib.parse.urlparse(start_url)
    robots_url = "{}://{}/robots.txt".format(parsed_url.scheme, parsed_url.netloc)

    robot_parser = urllib.robotparser.RobotFileParser()
    robot_parser.set_url(robots_url)
    robot_parser.read()

    return robot_parser

def can_fetch_url(robot_parser, url, user_agent="MyCrawler"):
    return robot_parser.can_fetch(user_agent, url)
