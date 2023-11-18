
from psychopy import visual, core, event, gui
import os
import random
import glob
from pylsl import StreamInfo, StreamOutlet, StreamInlet

dlg = gui.Dlg(title="Subject Information")
dlg.addField("Subject Number:")
subject_data = dlg.show()
if dlg.OK:
    subject_number = subject_data[0]
else:
    core.quit() 
    
# Define paths
images_folder = r"C:\Users\sccn\Desktop\ai_image\generated_images"
other_folder = r"C:\Users\sccn\Desktop\ai_image"
results_folder = r"C:\Users\sccn\Desktop\ai_image\results"

# Prepare window
win = visual.Window([1600, 900], fullscr=False, monitor="testMonitor", units="pix")

# Create a stream info and outlet for triggers
trigger_info = StreamInfo(name='Triggers', type='Markers', channel_count=1, nominal_srate=0, channel_format='string')
trigger_outlet = StreamOutlet(trigger_info)

# Prepare image stimuli and buttons
left_image_stim = visual.ImageStim(win, pos=(-400, 0), size=(500, 500))
right_image_stim = visual.ImageStim(win, pos=(400, 0), size=(500, 500))
buttons = {
    'left': visual.Rect(win, width=200, height=50, pos=(-400, -300), fillColor='lightgrey'),
    'right': visual.Rect(win, width=200, height=50, pos=(400, -300), fillColor='lightgrey'),
    'center': visual.Rect(win, width=200, height=50, pos=(0, -300), fillColor='lightgrey')
}
text_buttons = {
    'left': visual.TextStim(win, text="Select", pos=(-400, -300)),
    'right': visual.TextStim(win, text="Select", pos=(400, -300)),
    'center': visual.TextStim(win, text="Continue", pos=(0, -300))
}

# Prepare a mouse
mouse = event.Mouse(win=win)

def delay(duration=0.5):
    core.wait(duration)
    
def send_trigger(marker):
    trigger_outlet.push_sample([marker])

# Function to save results
def save_image_selection_results(subject_number, selected_color, selected_image, random_color):
    filename = os.path.join(results_folder, f'image_selection_results_subject_{subject_number}.csv')
    with open(filename, 'a') as file:
        file.write(f"{selected_color},{selected_image},{random_color}\n")

def save_survey_results(subject_number, survey_result):
    filename = os.path.join(results_folder, f'survey_results_subject_{subject_number}.csv')
    with open(filename, 'a') as file:
        file.write(f"{survey_result}\n")

# Function to show survey
# Question text
question_text1 = "How are you feeling right now?"
question_stim1 = visual.TextStim(win, text=question_text1, pos=(0, 300), height=40, wrapWidth=1000)

# Instruction text
instruction_text2 = "Use the sliding bar to indicate your feeling and press 'Enter' to continue."
instruction_stim2 = visual.TextStim(win, text=instruction_text2, pos=(0, 220), height=25)

# Function to show survey
def show_survey(image_path):
    # Load the survey image
    survey_image = visual.ImageStim(win, image=image_path, pos=(5, 0), size=(1200, 270))

    # Create the slider
    slider = visual.Slider(win, ticks=(0, 1, 2, 3, 4, 5, 6, 7, 8, 9), pos=(0, -200), size=(850, 50), granularity=0)

    while True:
        question_stim1.draw()  # Draw question text
        instruction_stim2.draw()  # Draw instruction text
        survey_image.draw()
        slider.draw()
        win.flip()
        if event.getKeys(keyList=['return']):
            return slider.getRating()
        elif event.getKeys(keyList=['escape']):
            return None

# Instruction page
instruction_text1 = "You will see a pair of images on the screen each time. Please choose one that represents your current emotion.\n\nPress 'Enter' to begin."
instruction_stim1 = visual.TextStim(win, text=instruction_text1, pos=(0, 0), height=40, wrapWidth=1000)

round_number = 1




# Run experiment
instruction_text5 = "Press ENTER to start."
instruction_stim5 = visual.TextStim(win, text=instruction_text5, pos=(0, 0), height=40, wrapWidth=1000)
instruction_stim5.draw()
win.flip()
event.waitKeys(keyList=['return'])
trigger_outlet.push_sample(['Start'])

instruction_text4 = "For the next 5 minutes, please sit completely still, without talking, moving, or fidgeting. Please keep your eyes open and fixate at the cross on the screen, try to minimize eye blinks, and just relax your eyes on the screen. Press ENTER to start."
instruction_stim4 = visual.TextStim(win, text=instruction_text4, pos=(0, 0), height=40, wrapWidth=1000)
instruction_stim4.draw()
win.flip()
event.waitKeys(keyList=['return'])
trigger_outlet.push_sample(['StartResting'])

# Fixation cross
fixation_cross = visual.TextStim(win, text='+', pos=(0, 0), height=50, color='black')

# Display the fixation cross for 5 minutes
fixation_duration = 300  # Duration in seconds (5 minutes)
fixation_clock = core.Clock()  # Start a clock to measure the time

while fixation_clock.getTime() < fixation_duration:
    fixation_cross.draw()
    win.flip()

previous_color = None

for iteration in range(12):
    colors = ['Red', 'Green', 'Yellow', 'Blue']

    # Select a random color different from the previous color
    color = random.choice(colors)
    while color == previous_color:
        color = random.choice(colors)

    previous_color = color  # Update the previous_color for the next iteration

    color_files = glob.glob(os.path.join(images_folder, f"{color}_*.jpg"))
    
    instruction_text3 = "You are participating in a guided imagery task. Please keep your eyes open and stay relaxed. Allow the following scenario to guide your imagination so that you can fully experience the suggested emotions. Press ENTER to start."
    instruction_stim3 = visual.TextStim(win, text=instruction_text3, pos=(0, 0), height=40, wrapWidth=1000)
    instruction_stim3.draw()
    win.flip()
    event.waitKeys(keyList=['return'])
    trigger_outlet.push_sample(['StartImagine'])
    
    # Add a page of text after the instruction of the imagery task
    # Load and display text file content named after the random color
    color_text_file = os.path.join(other_folder, f"{color}.txt")
    if os.path.exists(color_text_file):
        with open(color_text_file, 'r') as file:
            color_text_content = file.read()

        color_text_stim = visual.TextStim(win, text=color_text_content, pos=(0, 0), height=40, wrapWidth=1000)
        color_text_stim.draw()
        win.flip()
        event.waitKeys(keyList=['return'])
    else:
        print(f"No text file found for color: {color}")
    
    
    trigger_outlet.push_sample(['StartPleasureSurveyPostImagine'])
    survey_result1 = show_survey(os.path.join(other_folder, 'happy.png'))
    save_survey_results(subject_number, survey_result1)
    
    trigger_outlet.push_sample(['StartArousalSurveyPostImagine'])
    survey_result2 = show_survey(os.path.join(other_folder, 'calm.png'))
    save_survey_results(subject_number, survey_result2)

    instruction_stim1.draw()
    win.flip()

    # Wait for 'Enter' key press to continue
    event.waitKeys(keyList=['return'])

    for i in range(5):
        if not color_files:
            print(f'No images found for color: {color}')
            continue

        selected_left_image = random.choice(color_files)
        other_colors = [c for c in colors if c != color]
        other_color = random.choice(other_colors)
        image_number = selected_left_image.split('_')[-1].split('.')[0]
        selected_right_image = os.path.join(images_folder, f"{other_color}_{image_number}.jpg")

        left_image_stim.image = selected_left_image
        right_image_stim.image = selected_right_image

        buttons['left'].fillColor = 'lightgrey'
        buttons['right'].fillColor = 'lightgrey'

        while True:
            left_image_stim.draw()
            right_image_stim.draw()
            buttons['left'].draw()
            buttons['right'].draw()
            text_buttons['left'].draw()
            text_buttons['right'].draw()
            win.flip()

            if mouse.isPressedIn(buttons['left']):
                selected = 'left'
                buttons['left'].fillColor = 'darkgrey'
                break
            elif mouse.isPressedIn(buttons['right']):
                selected = 'right'
                buttons['right'].fillColor = 'darkgrey'
                break

        delay()

        # Extracting color from the filename of the selected image
        selected_image_path = selected_left_image if selected == 'left' else selected_right_image
        selected_image_color = os.path.basename(selected_image_path).split('_')[0]

        save_image_selection_results(subject_number, selected_image_color, selected_image_path, color)

        if selected == 'left':
            trigger_outlet.push_sample(['SelectLeft'])
        elif selected == 'right':
            trigger_outlet.push_sample(['SelectRight'])

    trigger_outlet.push_sample(['StartPleasureSurveyPostSelection'])
    survey_result3 = show_survey(os.path.join(other_folder, 'happy.png'))
    save_survey_results(subject_number, survey_result3)
    trigger_outlet.push_sample(['StartArousalSurveyPostSelection'])
    survey_result4 = show_survey(os.path.join(other_folder, 'calm.png'))
    save_survey_results(subject_number, survey_result4)

    # Construct the folder path for the current round
    round_folder = os.path.join(images_folder, f"Round_{round_number}")

    # Get all image files in the round folder
    round_image_files = glob.glob(os.path.join(round_folder, "*.jpg"))

    if round_image_files:
        positive_image_path = random.choice(round_image_files)
        positive_image_stim = visual.ImageStim(win, image=positive_image_path, pos=(0, -10), size=(900, 900))

        # New instruction page
        positive_image_instruction_page = "Next, you will be shown an image for 1 minute.\nTake a moment to enjoy it.\n\nPress 'Enter' to start."
        positive_image_instruction_page_stim = visual.TextStim(win, text=positive_image_instruction_page, pos=(0, 0), height=40, wrapWidth=1000)
        positive_image_instruction_page_stim.draw()
        win.flip()
        event.waitKeys(keyList=['return'])

        positive_image_instruction = "Please take a moment to feel this image."
        positive_image_instruction_stim = visual.TextStim(win, text=positive_image_instruction, pos=(0, 350), height=30)
    
        trigger_outlet.push_sample(['StartPositiveImage'])
    
        # Start a clock for the countdown
        countdown_clock = core.Clock()
        countdown_duration = 60  # 60 seconds

        while True:
            elapsed_time = countdown_clock.getTime()
            if elapsed_time >= countdown_duration:
                break  # Exit the loop after 1 minute

            remaining_time = countdown_duration - int(elapsed_time)

            positive_image_stim.draw()
            win.flip()
    
    trigger_outlet.push_sample(['StartPleasureSurveyPostPositive'])
    survey_result5 = show_survey(os.path.join(other_folder, 'happy.png'))
    save_survey_results(subject_number, survey_result5)
    trigger_outlet.push_sample(['StartArousalSurveyPostPositive'])
    survey_result6 = show_survey(os.path.join(other_folder, 'calm.png'))
    save_survey_results(subject_number, survey_result6)
    
    round_number += 1



end_message = "Thank you for participating in our study!\n\nPlease press any key to exit."
end_text = visual.TextStim(win, text=end_message, pos=(0, 0), height=30, wrapWidth=1000)

# Display the end message
end_text.draw()
win.flip()
trigger_outlet.push_sample(['End'])
event.waitKeys()

# Check for 'escape' key outside the main loop
if 'escape' in event.getKeys():
    win.close()

win.close()
core.quit()
