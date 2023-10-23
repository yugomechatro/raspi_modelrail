import openai
import json
import time

# Set GPIO pins for PWM outputs
FORWARD_GPIO = 12
REVERSE_GPIO = 13

# Set constants
PWM_FREQ = 1000
DELAY = 0.05


# Class that expresses the vehicle (train)
class Vehicle:
    # direction will be either "forward" or "reverse"
    direction: str
    # speed will be an integer between 0 and 100. 0 means that the vehicle is stopped.
    speed: int

    def __init__(self):
        self.direction = "forward"
        self.speed = 0

    def command(self, direction, speed):
        print("command accepted, direction: {}, speed: {}".format(direction, speed))
        # If the new direction is the opposite from the current direction
        if self.direction != direction:
            # First decrease speed to zero
            while self.speed:
                print("self.direction {}, self.speed {}".format(self.direction, self.speed))
                self.speed -= 1
                time.sleep(DELAY)
            
            # Then switch direction and increase speed to desired speed
            self.direction = direction
            while self.speed != speed:
                print("self.direction {}, self.speed {}".format(self.direction, self.speed))
                self.speed += 1
                time.sleep(DELAY)

        else:
            # If the direction is the same, then adjust to the speed
            if self.speed > speed:
                while self.speed != speed:
                    print("self.direction {}, self.speed {}".format(self.direction, self.speed))
                    self.speed -= 1
                    time.sleep(DELAY)
            else:
                while self.speed != speed:
                    print("self.direction {}, self.speed {}".format(self.direction, self.speed))
                    self.speed += 1
                    time.sleep(DELAY)

        # Sending signals to raspi here
    

# Function that checks for allowed values (will return True if values are OK)
def check_allowed_values(direction: str, speed: int) -> bool:
    if (direction == "forward" or direction == "reverse") and \
    (type(speed) == int and (0 <= speed <= 100)):
        return True
    return False


# Function that orders the vehicle to operate
def operate_vehicle(vehicle: Vehicle, direction: str, speed: int):
    # Check the values here, stop vehicle and raise error if invalid values
    if not check_allowed_values(direction, speed):
        vehicle.command("forward", 0)
    else:
        vehicle.command(direction, speed)


# Main function that has a conversation with GPT. It will accept user prompts repeatedly.
def run_conversation():
    # Define what the function and its parameters are
    functions = [
        {
            "name": "operate_vehicle",
            "description": "Operates the vehicle with the given direction and speed",
            "parameters": {
                "type": "object",
                "properties": {
                    "direction": {
                        "type": "string",
                        "description": "The direction in which the vehicle moves. The only valid values are 'forward' and 'reverse'.",
                        "enum": ["forward", "reverse"]
                    },
                    "speed": {
                        "type": "integer",
                        "description": "The speed of the vehicle. Allowed values are intergers from 0 to 100. 0 means that the vehicle is stopped."
                    }
                },
                "required": ["direction", "speed"],
            },
        }
    ]

    # Initialize Vehicle object
    VehicleInstance = Vehicle()

    # Execute against ChatGPT in a loop
    while True:
        # Get the user prompt
        user_prompt = input("Insert user prompt (in Japanese):")

        # If user prompt was empty, break out of the loop
        if not user_prompt:
            print("No user prompt. Stopping...")
            VehicleInstance.command("forward", 0)
            break

        # Send the conversation and available functions to GPT
        messages = [
            {
                "role": "system",
                "content": "You are an AI assistant that will give certain orders to operate a vehicle. The order will be supplied in Japanese."
            },
            {
                "role": "user", 
                "content": "{}".format(user_prompt)
            }
        ]

        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo-0613",
            messages=messages,
            functions=functions,
            function_call="auto",  # auto is default, but we'll be explicit
        )
        response_message = response["choices"][0]["message"]

        # Print the returned message
        print(response_message)

        # Check if GPT wanted to call a function (Don't call anything otherwise)
        if response_message.get("function_call"):
            # Call the function
            available_functions = {
                "operate_vehicle": operate_vehicle
            }
            # Get the function to call
            function_name = response_message["function_call"]["name"]
            function_to_call = available_functions[function_name]
            # Parse the function arguments
            function_args = json.loads(response_message["function_call"]["arguments"])
            if function_name == "operate_vehicle":
                # Execute the function
                function_to_call(
                    vehicle=VehicleInstance,
                    direction=function_args.get("direction"),
                    speed=function_args.get("speed")
                )


if __name__ == "__main__":
    run_conversation()