from typing import Tuple, Optional
from time import sleep
import gradio

import ultraface.globals
from ultraface import process_manager, wording
from ultraface.core import conditional_process
from ultraface.memory import limit_system_memory
from ultraface.normalizer import normalize_output_path
from ultraface.uis.core import get_ui_component
from ultraface.filesystem import clear_temp, is_image, is_video

OUTPUT_IMAGE : Optional[gradio.Image] = None
OUTPUT_VIDEO : Optional[gradio.Video] = None
OUTPUT_START_BUTTON : Optional[gradio.Button] = None
OUTPUT_CLEAR_BUTTON : Optional[gradio.Button] = None
OUTPUT_STOP_BUTTON : Optional[gradio.Button] = None


def render() -> None:
	global OUTPUT_IMAGE
	global OUTPUT_VIDEO
	global OUTPUT_START_BUTTON
	global OUTPUT_STOP_BUTTON
	global OUTPUT_CLEAR_BUTTON

	OUTPUT_IMAGE = gradio.Image(
		label = wording.get('uis.output_image_or_video'),
		visible = False
	)
	OUTPUT_VIDEO = gradio.Video(
		label = wording.get('uis.output_image_or_video')
	)
	OUTPUT_START_BUTTON = gradio.Button(
		value = wording.get('uis.start_button'),
		variant = 'primary',
		size = 'sm'
	)
	OUTPUT_STOP_BUTTON = gradio.Button(
		value = wording.get('uis.stop_button'),
		variant = 'primary',
		size = 'sm',
		visible = False
	)
	OUTPUT_CLEAR_BUTTON = gradio.Button(
		value = wording.get('uis.clear_button'),
		size = 'sm'
	)


def listen() -> None:
	output_path_textbox = get_ui_component('output_path_textbox')
	if output_path_textbox:
		OUTPUT_START_BUTTON.click(start, outputs = [ OUTPUT_START_BUTTON, OUTPUT_STOP_BUTTON ])
		OUTPUT_START_BUTTON.click(process, outputs = [ OUTPUT_IMAGE, OUTPUT_VIDEO, OUTPUT_START_BUTTON, OUTPUT_STOP_BUTTON ])
	OUTPUT_STOP_BUTTON.click(stop, outputs = [ OUTPUT_START_BUTTON, OUTPUT_STOP_BUTTON ])
	OUTPUT_CLEAR_BUTTON.click(clear, outputs = [ OUTPUT_IMAGE, OUTPUT_VIDEO ])


def start() -> Tuple[gradio.Button, gradio.Button]:
	while not process_manager.is_processing():
		sleep(0.5)
	return gradio.Button(visible = False), gradio.Button(visible = True)


def process() -> Tuple[gradio.Image, gradio.Video, gradio.Button, gradio.Button]:
	normed_output_path = normalize_output_path(ultraface.globals.target_path, ultraface.globals.output_path)
	if ultraface.globals.system_memory_limit > 0:
		limit_system_memory(ultraface.globals.system_memory_limit)
	conditional_process()
	if is_image(normed_output_path):
		return gradio.Image(value = normed_output_path, visible = True), gradio.Video(value = None, visible = False), gradio.Button(visible = True), gradio.Button(visible = False)
	if is_video(normed_output_path):
		return gradio.Image(value = None, visible = False), gradio.Video(value = normed_output_path, visible = True), gradio.Button(visible = True), gradio.Button(visible = False)
	return gradio.Image(value = None), gradio.Video(value = None), gradio.Button(visible = True), gradio.Button(visible = False)


def stop() -> Tuple[gradio.Button, gradio.Button]:
	process_manager.stop()
	return gradio.Button(visible = True), gradio.Button(visible = False)


def clear() -> Tuple[gradio.Image, gradio.Video]:
	while process_manager.is_processing():
		sleep(0.5)
	if ultraface.globals.target_path:
		clear_temp(ultraface.globals.target_path)
	return gradio.Image(value = None), gradio.Video(value = None)
