from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import random

# Setup the WebDriver (Make sure to have the correct path for your WebDriver)
driver = webdriver.Chrome()

# Replace with the YouTube video URL you want to watch
video_url = "https://www.youtube.com/watch?v=316UZQM3DMg"

# Set the number of times you want to watch the video
num_times = 3

# Function to get the video duration
def get_video_duration():
    # Get the video duration in seconds by finding the 'ytp-time-duration' element
    duration = driver.find_element(By.CLASS_NAME, 'ytp-time-duration').text
    time_parts = duration.split(':')

    # Check if there are 2 or 3 parts (to handle hours)
    if len(time_parts) == 2:
        minutes, seconds = map(int, time_parts)
        total_seconds = minutes * 60 + seconds
    elif len(time_parts) == 3:
        hours, minutes, seconds = map(int, time_parts)
        total_seconds = hours * 3600 + minutes * 60 + seconds
    else:
        raise ValueError(f"Unexpected time format: {duration}")
    
    return total_seconds

# Function to get the current time of the video
def get_current_time():
    try:
        # Find the current time of the video
        current_time = driver.find_element(By.CLASS_NAME, 'ytp-time-current').text
        print(f"Current time: {current_time}")  # Debugging line to see what current_time is
        
        # Check if the current time is empty
        if not current_time:
            raise ValueError("Current time is empty.")

        time_parts = current_time.split(':')

        # Check if there are 2 or 3 parts (to handle hours)
        if len(time_parts) == 2:
            minutes, seconds = map(int, time_parts)
            total_seconds = minutes * 60 + seconds
        elif len(time_parts) == 3:
            hours, minutes, seconds = map(int, time_parts)
            total_seconds = hours * 3600 + minutes * 60 + seconds
        else:
            raise ValueError(f"Unexpected time format: {current_time}")
        
        return total_seconds
    except Exception as e:
        print(f"Error while getting current time: {e}")
        return 0  # Return 0 if there's an error, so the loop can continue
# Function to simulate pressing the forward button
def forward_video():
    # Forward video by 10 seconds using 'L' key
    driver.find_element(By.TAG_NAME, 'body').send_keys('l')
    print("Video forwarded by 10 seconds.")

# Function to simulate pressing the rewind button
def rewind_video():
    # Rewind video by 10 seconds using 'J' key
    driver.find_element(By.TAG_NAME, 'body').send_keys('j')
    print("Video rewinded by 10 seconds.")

def toggle_video():
    # Toggle the video
    pause_button = driver.find_element(By.CLASS_NAME, "ytp-play-button")
    pause_button.click()
    print("Video paused/resumed.")

# Loop to watch the video multiple times
for i in range(num_times):
    driver.get(video_url)
    
    # Wait for the video to load
    time.sleep(5)
    
    # Find the play/pause button and click it to start the video
    pause_button = driver.find_element(By.CLASS_NAME, "ytp-play-button")
    pause_button.click()  # Video starts playing
    print(f"Watching video {i + 1}/{num_times}")
    
    # Get the video duration in seconds
    video_duration = get_video_duration()
    print(f"Video duration: {video_duration} seconds.")
    
    # Loop until the video reaches its duration
    while True:
        current_time = get_current_time()
        
        # Check if the current time has reached the video's total duration
        if current_time >= video_duration:
            print(f"Video {i + 1} finished.")
            break
        # Randomize the next action (forward or rewind)
        action = random.choice(['forward', 'rewind'])
        time.sleep(random.randint(0,10))
        if action == 'forward':
            forward_video()
        else:
            toggle_video()
        
        # Wait for 1 second before checking again
        time.sleep(1)
    
    # Wait before starting the next video
    time.sleep(2)

# Close the browser after the loop
driver.quit()
