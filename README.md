# ChatGPT Blender Addon

This addon allows you to communicate with OpenAI's ChatGPT model to create Geometry Nodes in Blender based on user input.

## Requirements

- Blender 2.80 or higher
- An OpenAI API key (obtained through the [OpenAI website](https://beta.openai.com/signup/))

## Installation

1. Save the provided code as `chatgpt_blender.py` on your computer.
2. Open Blender and go to `Edit > Preferences` (or `File > User Preferences` in older versions).
3. Click on the `Add-ons` tab and then click the `Install...` button in the top right corner.
4. Navigate to where you saved the `chatgpt_blender.py` file, select it, and click `Install Add-on`.
5. Search for "ChatGPT" in the search bar and check the box to enable the addon.
6. Click the arrow next to the addon name to expand its options and paste your OpenAI API key in the `API Key` field.

## Usage

1. Open a scene in Blender and access the "GPT" panel in the right sidebar of the 3D view window (press `N` to display the sidebar if needed).
2. Enter your instruction in the "Input" text box.
3. Click the "Execute" button to send your instruction to ChatGPT and create the corresponding Geometry Nodes.

For example, you can type "Create a node group with a cube and a cylinder" and the addon will create the appropriate Geometry Nodes based on ChatGPT's response.

Keep in mind that this addon is a basic example and may not work perfectly with all types of Geometry Nodes or user commands. Enhance the communication and response interpretation logic of ChatGPT, add support for more node types and properties, and handle potential errors and exceptions to improve the addon's robustness and functionality.

# chatgpt-blender
