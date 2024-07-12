from prompts import FELIPACK_PROMPT, MELILOT_PROMPT, PME_PROMPT

# Create a dictionary to map the prompt names to their values
choices = [
    {
        "name":"FELIPACK",
        "var":FELIPACK_PROMPT,
        "choice":1
    },
    {
        "name":"MELILOT",
        "var":MELILOT_PROMPT,
        "choice":2
    },
    {
        "name":"PME",
        "var":PME_PROMPT,
        "choice":3
    },
]

for prompt in choices:
    print(f"{prompt['choice']}.{prompt['name']}")

choice = str(input('Choose Prompt To Edit: '))

chosen_prompt = next((prompt for prompt in choices if str(prompt["choice"]) == choice), None)

edit = print('Do you want to edit? y/n')
if chosen_prompt:
    print(chosen_prompt['var'])
    edit = input('Do you want to edit? y/n: ')
    if edit.lower() == "y":
        new_prompt = input('Please add new prompt: ')
        chosen_prompt['var'] = new_prompt

        # Now, write the changes back to the file
        with open('prompts.py', 'r', encoding='UTF-8') as file:
            lines = file.readlines()

        with open('prompts.py', 'w', encoding='UTF-8') as file:
            for line in lines:
                if line.startswith(chosen_prompt['name']):
                    file.write(f"{chosen_prompt['name']}_PROMPT = '''{new_prompt}'''\n")
                else:
                    file.write(line)

        print(f"{chosen_prompt['name']} has been updated.")
else:
    print('Invalid choice')