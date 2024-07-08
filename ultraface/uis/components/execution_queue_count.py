from typing import Optional
import gradio

import ultraface.globals
import ultraface.choices
from ultraface import wording

EXECUTION_QUEUE_COUNT_SLIDER : Optional[gradio.Slider] = None


def render() -> None:
	global EXECUTION_QUEUE_COUNT_SLIDER

	EXECUTION_QUEUE_COUNT_SLIDER = gradio.Slider(
		label = wording.get('uis.execution_queue_count_slider'),
		value = ultraface.globals.execution_queue_count,
		step =ultraface.choices.execution_queue_count_range[1] - ultraface.choices.execution_queue_count_range[0],
		minimum = ultraface.choices.execution_queue_count_range[0],
		maximum = ultraface.choices.execution_queue_count_range[-1]
	)


def listen() -> None:
	EXECUTION_QUEUE_COUNT_SLIDER.release(update_execution_queue_count, inputs = EXECUTION_QUEUE_COUNT_SLIDER)


def update_execution_queue_count(execution_queue_count : int = 1) -> None:
	ultraface.globals.execution_queue_count = execution_queue_count
